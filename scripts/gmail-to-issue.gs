/**
 * Gmail +ai宛メール → GitHub Issue 自動作成
 *
 * セットアップ:
 * 1. https://script.google.com で新規プロジェクト作成
 * 2. このコードを貼り付け
 * 3. GITHUB_TOKEN を「プロジェクトの設定 → スクリプトプロパティ」に追加
 *    (値: GitHub Personal Access Token, scope: repo)
 * 4. トリガー設定: checkAiEmails を「時間主導型 → 1分ごと」で設定
 *
 * v2 (2026-04-17): subject限定判定・-in:drafts除外・Message-ID dedup・
 *   元スレッドReply通知（受付/作成完了）
 * v3 (2026-04-17): close-poll 追加。Issue が close されたら元 Gmail スレッドに
 *   `反映完了 ✅` を Reply（GitHub 通知メール分断の解消）
 */

const PROCESSED_LABEL = "routines-done";
const PROCESSED_IDS_PROP = "processed_msg_ids";
const PENDING_ISSUES_PROP = "pending_issue_notifications";
const MAX_PROCESSED_IDS = 200;
const MAX_PENDING_ISSUES = 100;

// PJごとのルーティング設定
const ROUTES = [
  {
    repo: "trip-planner",
    keywords: ["旅行", "trip", "台北", "taipei", "london", "macau", "霧島", "kirishima", "福岡", "fukuoka", "プラン更新"]
  },
  {
    repo: "property-report",
    keywords: ["物件", "不動産", "問い合わせ", "内見", "マンション", "property", "inquiry", "融資"]
  }
];

// メイントリガーエントリ（1分ごと）
function checkAiEmails() {
  routeNewEmails();
  pollClosedIssues();
}

// ── Phase 1: 新着メール → Issue 作成 ─────────────────────────
function routeNewEmails() {
  const baseQuery = 'to:yma.tz.28+ai@gmail.com -label:' + PROCESSED_LABEL + ' -in:drafts newer_than:1d';
  const threads = GmailApp.search(baseQuery, 0, 10);

  if (threads.length === 0) return;

  let label = GmailApp.getUserLabelByName(PROCESSED_LABEL);
  if (!label) {
    label = GmailApp.createLabel(PROCESSED_LABEL);
  }

  const processedIds = loadProcessedIds();
  const pending = loadPending();

  for (const thread of threads) {
    const messages = thread.getMessages();
    const latest = messages[messages.length - 1];
    const msgId = latest.getId();

    if (processedIds.indexOf(msgId) !== -1) {
      thread.addLabel(label);
      continue;
    }

    const rawSubject = latest.getSubject() || "";
    const subject = rawSubject.replace(/^(Re:\s*|Fwd:\s*)+/gi, '');
    const subjectLower = subject.toLowerCase();

    // subject のみで判定
    const route = ROUTES.find(r => r.keywords.some(kw => subjectLower.includes(kw.toLowerCase())));
    if (!route) {
      thread.addLabel(label);
      markProcessed(processedIds, msgId);
      continue;
    }

    const body = latest.getPlainBody();
    const trimmedBody = (body || "").replace(/よろしくお願い致します[\s\S]*$/, "").trim();
    if (trimmedBody.length < 5) {
      thread.addLabel(label);
      markProcessed(processedIds, msgId);
      safeReply(thread, "本文が空のため Issue 化をスキップしました。内容を書いて再送してください。");
      continue;
    }

    safeReply(thread, "受付けました ⏳ GitHub Issue を作成します（" + route.repo + "）");

    try {
      const result = createGitHubIssue(route.repo, subject, body);
      thread.addLabel(label);
      markProcessed(processedIds, msgId);
      safeReply(
        thread,
        "Issue 作成完了 ✅\n" +
        route.repo + " #" + result.number + " " + result.title + "\n" +
        result.html_url + "\n\n" +
        "自動反映ワークフローが走ります。完了時に再度このスレッドに通知します。"
      );
      // close-poll 対象として登録
      pending[route.repo + "#" + result.number] = {
        repo: route.repo,
        issue_number: result.number,
        issue_url: result.html_url,
        thread_id: thread.getId(),
        created_at: Date.now(),
      };
    } catch (e) {
      safeReply(thread, "Issue 作成失敗 ❌ " + e.message + "\n次の1分サイクルで再試行します。");
      Logger.log("createGitHubIssue error: " + e.message);
    }
  }

  saveProcessedIds(processedIds);
  savePending(pending);
}

// ── Phase 2: close-poll → Gmail スレッドへ反映完了 Reply ──────
function pollClosedIssues() {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) return;

  const pending = loadPending();
  const keys = Object.keys(pending);
  if (keys.length === 0) return;

  const stillPending = {};
  const now = Date.now();
  const MAX_AGE_MS = 24 * 60 * 60 * 1000; // 24h で打ち切り（タイムアウトしたワークフローの残骸を掃除）

  for (const key of keys) {
    const entry = pending[key];
    if (now - entry.created_at > MAX_AGE_MS) {
      // 24h 超 → 諦める（エラー通知してクリア）
      try {
        const thread = GmailApp.getThreadById(entry.thread_id);
        if (thread) {
          thread.reply(
            "⚠️ 24h 経っても " + entry.repo + " #" + entry.issue_number + " がクローズされません\n" +
            entry.issue_url + "\n\n手動で状態確認してください。"
          );
        }
      } catch (e) {
        Logger.log("stale notify failed: " + e.message);
      }
      continue;
    }

    try {
      const url = 'https://api.github.com/repos/ymatz28-beep/' + entry.repo + '/issues/' + entry.issue_number;
      const response = UrlFetchApp.fetch(url, {
        method: 'get',
        headers: {
          'Authorization': 'token ' + token,
          'Accept': 'application/vnd.github.v3+json',
        },
        muteHttpExceptions: true,
      });

      if (response.getResponseCode() !== 200) {
        stillPending[key] = entry;
        continue;
      }

      const data = JSON.parse(response.getContentText());

      if (data.state !== 'closed') {
        stillPending[key] = entry;
        continue;
      }

      // closed 検知 → 元スレッドに Reply
      try {
        const thread = GmailApp.getThreadById(entry.thread_id);
        if (thread) {
          const pageUrl = entry.repo === 'trip-planner'
            ? 'https://ymatz28-beep.github.io/trip-planner/'
            : (entry.repo === 'property-report'
                ? 'https://ymatz28-beep.github.io/property-report/'
                : entry.issue_url);
          thread.reply(
            "反映完了 ✅\n" +
            entry.repo + " #" + entry.issue_number + " が処理されました\n" +
            pageUrl + "\n" +
            entry.issue_url + "\n\n" +
            "キャッシュ(10分)のためハードリロード推奨。"
          );
        }
      } catch (e) {
        Logger.log("reply on close failed: " + e.message);
      }
      // stillPending に入れない = 削除
    } catch (e) {
      Logger.log("issue poll failed (" + key + "): " + e.message);
      stillPending[key] = entry;
    }
  }

  savePending(stillPending);
}

// ── GitHub Issue 作成 ────────────────────────────────────────
function createGitHubIssue(repo, title, body) {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) {
    throw new Error('GITHUB_TOKEN が設定されていません');
  }

  const url = 'https://api.github.com/repos/ymatz28-beep/' + repo + '/issues';
  const payload = {
    title: title,
    body: body,
    labels: ["update"]
  };
  const response = UrlFetchApp.fetch(url, {
    method: 'post',
    headers: {
      'Authorization': 'token ' + token,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  const code = response.getResponseCode();
  if (code !== 201) {
    throw new Error('GitHub Issue 作成失敗: ' + code + ' ' + response.getContentText());
  }

  const data = JSON.parse(response.getContentText());
  Logger.log('Issue 作成成功: ' + data.html_url);
  return data;
}

// ── Script Properties helpers ───────────────────────────────
function loadProcessedIds() {
  const raw = PropertiesService.getScriptProperties().getProperty(PROCESSED_IDS_PROP);
  if (!raw) return [];
  try { return JSON.parse(raw); } catch (e) { return []; }
}

function markProcessed(ids, msgId) {
  ids.push(msgId);
  if (ids.length > MAX_PROCESSED_IDS) {
    ids.splice(0, ids.length - MAX_PROCESSED_IDS);
  }
}

function saveProcessedIds(ids) {
  PropertiesService.getScriptProperties().setProperty(PROCESSED_IDS_PROP, JSON.stringify(ids));
}

function loadPending() {
  const raw = PropertiesService.getScriptProperties().getProperty(PENDING_ISSUES_PROP);
  if (!raw) return {};
  try { return JSON.parse(raw); } catch (e) { return {}; }
}

function savePending(map) {
  const keys = Object.keys(map);
  if (keys.length > MAX_PENDING_ISSUES) {
    const sorted = keys.sort((a, b) => (map[b].created_at || 0) - (map[a].created_at || 0));
    const trimmed = {};
    for (let i = 0; i < MAX_PENDING_ISSUES; i++) trimmed[sorted[i]] = map[sorted[i]];
    map = trimmed;
  }
  PropertiesService.getScriptProperties().setProperty(PENDING_ISSUES_PROP, JSON.stringify(map));
}

function safeReply(thread, text) {
  try {
    thread.reply(text);
  } catch (e) {
    Logger.log("reply failed: " + e.message);
  }
}
