# HANDOFF

## 最終更新: 2026-03-22 (fukuoka.html全面改修 未完了 — API 502で中断)

## プロジェクト概要
- **リポジトリ**: ymatz28-beep/trip-planner (GitHub Pages)
- **URL**: https://ymatz28-beep.github.io/trip-planner/
- **ローカルパス**: `~/Documents/Projects/trip-planner/`
- **構成**: index.html（ダッシュボード）、taipei.html、taipei-food.html、macau.html、london.html、fukuoka.html（計6ページ）
- **デザイン**: iUMA report-dashboard のデザインシステムに準拠（Inter フォント、共通 gnav）

## 台北旅行の概要
- **日程**: 2026年4月16日〜20日（4泊5日）**確定**
- **フライト**: EVA Air NRT↔TPE ¥54,840/人 **予約済み**
- **ホテル**: 相鉄グランドフレッサ台北西門 **予約済み**
- **空港**: 桃園国際空港（MRT 50分で市内）
- **人数**: 2名（Yuma + 大木くん）
- **テーマ**: 飲茶 × LGBTQ+ × 夜市 × 烏龍茶
- **大木くん**: 酒飲み。クラフトビール、カクテル好き
- **Yuma**: ノンアル。LGBT。食（小籠包、飲茶、夜市B級グルメ）重視
- **注目イベント**: 4/18（土）= WERK! @ Triangle（毎月第3土曜の台北最大級ゲイナイト）

## 完了済み（直近セッション: 2026-03-22）
- **fukuoka.html commit+push完了 (2f24845)**: 福岡ローカルガイド新規作成（885行）。iUMAデザインシステム準拠（ダークテーマ、Inter+Noto Sans JP+JetBrains Mono、アクセント#C47D4E）。5セクション構成: ①温泉・サウナ（ふくの湯3店舗: 春日/花畑/新宮。料金・営業時間・アクセス・設備タグ・Google Mapsリンク付き）②グルメ（ラーメン/水炊き・もつ鍋/屋台/一口餃子/海鮮・ごまさば/カフェの6カテゴリ、エリアタグ付き）③エリアガイド（博多駅/天神/中洲/薬院・白金/太宰府/糸島の6エリア、スポットリスト付き）④アクセス（6ルート料金比較テーブル）⑤Tips（ICカード/ベストシーズン/コンビニ/駐車場/夜の楽しみ方/キャッシュレスの6カード）。セクションナビ+スムーススクロール+スクロール連動アクティブ状態実装
- **index.htmlにFukuokaエントリ追加済み**: TRIPSリストにfukuoka.htmlリンク追加
- （前回）**taipei.html + taipei-food.html コミット&プッシュ完了** (40f9062)
- （前回）**マカオ旅行完了マーク**: 全予約・計画確定済み
- （前回）**Public→Private導線遮断チェック合格** (3/21 kaizen-agent): 全5ファイル安全確認済み

## 進行中 / 未完了
- **fukuoka.html 全面改修（未着手）**: 現状はふくの湯3店舗のみの不完全状態。以下セクションの追加が必要:
  - **サウナ施設拡充**: ヨーガンレーベン（中央区）、ウェルビー福岡（博多区）、Nayuta THE VANISH（久山町 — 2024/12火災→2025/12改修再開予定、2026/3現在は営業再開済みの見込み）、アマンティ（筑紫野）、清流（那珂川）、天拝の湯（筑紫野）、伊都の湯どころ、The Riverside Sauna、らかんの湯（武雄）
  - **温泉セクション**: 二日市温泉 博多湯、脇田温泉、古湯温泉（佐賀）、原鶴温泉、武雄温泉、嬉野温泉、平山温泉（熊本）、湯布院、別府温泉、黒川温泉（熊本）
  - **ドライブコース**: 佐賀（吉野ヶ里+古湯/武雄+御船山/嬉野/唐津・呼子）、糸島（二見ヶ浦/花塩プリン/牡蠣小屋/海沿いカフェ）
  - **モデルプラン**: 半日（太宰府or糸島）/ 1日（佐賀ドライブ）/ 1泊2日 / 2泊3日
  - **市内観光拡充**: 太宰府天満宮（仮殿2026/5まで限定）、志賀島、能古島、櫛田神社、柳川川下り、門司港レトロ、篠栗九大の森
  - **グルメ拡充**: ごぼう天うどん、鉄鍋餃子、呼子イカ、明太子
- **fukuoka.html アクセント色ずれ**: 指定#FF8C42(warm amber)に対し実装は#C47D4E。要確認・修正判断
- 台北: 基本計画確定（フライト・ホテル予約済み）。詳細スケジュール微調整の余地あり

## 次回アクション（優先順）
1. **fukuoka.html 全面改修実行**: 上記「進行中」の全セクションを一括追加。macau.htmlのデザインパターンを参考に同品質で構築。前セッションでリサーチ済みの情報をそのまま実装に移す
2. **fukuoka.html アクセント色修正判断**: #C47D4E→#FF8C42に修正するか、現行色で良しとするか（全面改修と同時対応推奨）
3. **台北 詳細プラン仕上げ**: 日程表の各スポット時間配分、移動ルート最適化
4. **改善: gnav共通化テンプレート検討**: 現在6ファイルにsite-navをコピペ管理。renderer.pyの`_public_nav`と同期は取れているが手動更新のため乖離リスクあり。ビルドステップ or include snippet で一元化できる余地

## Key Decisions
- 2026-03-22: **fukuoka.htmlデザイン方針** — 福岡ホスティングガイド（友人向けスポット案内）。iUMAデザインシステム準拠、アクセント#FF8C42（warm amber）。旅行日程型ではなくスポットガイド形式
- 2026-03-20: **デプロイ基盤2層化** — Public(GitHub Pages: zero-auth, auto-deploy on push) + Private(Cloudflare Pages + Access: email OTP)。trip-plannerはPublic側。infra-manifest.yamlで全ターゲットをSSoT管理
- 2026-03-16: **Booked = Cleanルール制定** — 予約確定したら即座に他候補・比較タブ・検索リンクを削除し確定情報のみ残す運用ルール。コンテンツ品質ルール#11
- 2026-03-16: フライト確定 — ANA HND↔TSA案からEVA Air NRT↔TPEに変更。空港は松山→桃園に。ホテルは相鉄グランドフレッサ台北西門に確定
- 2026-03-10: Self-hosted Runnerは3S不適合で撤去。Simple: GitHub hosted runnerで十分、Sustainable: メンテコスト増大。遠回りの原因になった
- 2026-03-10: Private側(stock/wealth/intel)のスマホ更新はROI低い（自動パイプライン生成のため手動更新ニーズなし）。リモートリポもない。需要時に個別対応
- 2026-03-10: `github-actions`用APIキーのクレジット問題は解消。3リポ(trip-planner/property-report/report-dashboard)にシークレット設定完了。Issue #10で動作実証済み
- 2026-03-10: claude CLIの認証は`--api-key`フラグではなく`ANTHROPIC_API_KEY`環境変数。GitHub Actionsではsecretsから環境変数として渡す
- 2026-03-09: macau Day 5夕食を誠昌飯店→Kapok六棉酒家(Bib Gourmand)に変更。品質重視（TripAdvisor 3/5→4.1/5）。広東料理で胸焼け対策も容易
- 2026-03-09: GitHub Actions用Anthropic APIキー(`github-actions`)設定。クレジット反映待ちで一時保留。スマホ更新はIssue経由で次ローカルセッション対応の暫定運用
- 2026-03-09: iuma-private全ページのgnav統一。nav順序: Stock → Market Intel → Intel → Wealth → Action → Property → Travel。trip-plannerは "Travel" として全ページからリンク
- 2026-03-07: Day3夕食をZi Yat Heen→フィッシャーマンズ・ワーフに変更。アウターハーバーターミナル経由でナイトバス集合に直結する導線に最適化
- 2026-03-07: ナイトバス Klook予約済み（20:30 アウターハーバーターミナル発）
- 2026-03-07: iUMAデザインシステム統一。全ページにType A gnav、コンパクトhero、Inter/JetBrains Monoフォント
- 2026-03-07: セクションナビにモバイルハンバーガー追加。640px以下でドロップダウン化
- 2026-03-06: ロンドン → 台北に変更（中東リスク）
- 2026-03-06: 4泊/5泊の両プラン並行準備（タブ切り替えUI）
- 2026-03-06: 2名旅行（Yuma + 大木くん）。大木くん=酒飲み、Yuma=ノンアル
- 2026-03-06: カラーテーマ: pink(#E8577A), teal(#00897B), gold(#D4A055)
- 2026-03-06: 4/18(土)=WERK!第3土曜パーティーをDay 4に組み込み

## コンテンツ品質ルール（trip-planner 固有）
旅行ページを新規作成・更新する際は、以下を**初回から**漏れなく含めること。追加指示は不要。

1. **日程の全スポットにGoogle Mapsリンク**: `<a href="https://maps.google.com/?q=..." target="_blank" style="color:var(--pink);">📍 Map</a>` を activity-desc 末尾に必ず付与
2. **空港ラウンジ情報**: PP / スタアラGold / SFC の利用可否を空港ごとに明記
3. **通貨・両替セクション**: 現地通貨の基本、両替レート比較（場所別）、おすすめ戦略
4. **ジム情報**: 宿泊ホテルのジム名・場所・営業時間・設備をホテルカードに記載
5. **マイレージ情報**: 利用航空会社の提携マイレージ積算可否
6. **時系列の整合性**: 日程表のタイムラインは必ず時刻順
7. **リンク生存確認**: Google Mapsリンクは `https://maps.google.com/?q=スポット名+地域名` 形式で統一
8. **空港アクセス比較**: 交通手段別の料金比較と結論
9. **お土産・税関ルール**: 持ち込み可否・罰則情報
10. **飲酒/ノンアル両対応**: 同行者に酒飲みがいる場合は両方のオプションを記載
11. **確定即クリーンアップ（Booked = Clean）**: 予約確定した項目は即座に以下を実行（指示不要）:
    - 他の候補・比較タブ・検索リンクを**削除**。確定情報のみ残す
    - ステータスを「予約済み」に変更。タブUIは不要になったら削除
    - 予算セクションを実コストで更新
    - チェックリストの該当項目を完了済みに
    - 日程表のタイムライン（出発時刻・到着時刻・移動時間）を確定便に合わせて調整
    - 未確定の選択肢（4泊/5泊タブ等）が確定で不要になったら削除

## ブロッカー / 注意事項
- 台北出発まで約25日（4/16出発、本日3/22時点）
- GitHub Pages はキャッシュが強い: Cmd+Shift+R でハードリロード
- property-report, report-dashboardのGitHub Actions未テスト（キー設定のみ完了）

## 環境構築メモ
- 全て単一 HTML ファイル（CSS/JS 埋め込み）
- Leaflet.js（CDN）で地図。CARTO ダークタイル
- チェックリストは localStorage で状態保持
- 予算: 4泊確定。5泊タブ・switchPlan()/switchBudgetTab()は削除済み
- 共通 gnav: チェックボックスハックでハンバーガーメニュー（JS不要）
- デプロイ: `git push` → GitHub Pages 自動デプロイ

## History
| 日付 | サマリー |
|------|----------|
| 2026-03-22 | fukuoka.html全面改修セッション: 不足セクション洗い出し（サウナ9施設/温泉10箇所/ドライブ2コース/モデルプラン追加要）→Nayuta調査完了→API 502×3で中断。コード変更なし |
| 2026-03-22 | API障害継続: 「続き」「続きは」で再開試行→502×6回+ConnectionRefused。06:10〜08:22の約2時間ロスト。後続作業（アクセント色修正等）未着手 |
| 2026-03-22 | fukuoka.html完了後にAPI 502+ConnectionRefused連続発生（リトライ10回超、計47分）。セッション実質停止 |
| 2026-03-22 | fukuoka.html作成完了+commit+push (2f24845)。初回502エラーで中断→再試行で成功。index.htmlにFukuoka追加済み |
| 2026-03-22 | taipei.html+taipei-food.html commit+push (40f9062)。マカオ完了マーク |
| 2026-03-21 | kaizen-agent QA巡回: Public→Private導線遮断チェック。trip-planner全5ファイル合格。renderer.py _public_nav正常 |
| 2026-03-20 | infra-manifest.yaml deployments新設: trip-plannerをGitHub Pagesターゲット登録 + deploy-private.sh SSoT整理 + constancy monitoring対象化 |
| 2026-03-20 | taipei.html フライトセクション圧縮（4ブロック→1カード、面積1/3）+ taipei-food.html新規作成。未コミット |
| 2026-03-20 | [Projects #51] root .gitignoreにsubproject登録（trip-planner独立管理化）。HANDOFF日付・カウントダウン更新 |
| 2026-03-17 | kaizen-agent GHA監視にtrip-planner追加 (99b48b8)。ワークフロー単位検出で pages-build / Update Trip Plan 両方🟢確認 |
| 2026-03-16 | Booked=Cleanクリーンアップ: 未予約候補全削除(-177行)、ambaタブ・5泊タブ・検索リンク除去。ルール#11制定 (9454601) |
| 2026-03-16 | 台北フライト＆ホテル確定: EVA Air NRT↔TPE(¥54,840/人)+相鉄グランドフレッサ西門。空港アクセス・予算・チェックリスト更新 (5f9f3e0) |
| 2026-03-10 | GitHub Actions完全復旧: APIキー再設定→Issue #10成功(36秒)。3リポにシークレット設定。Private側スマホ更新はROI低で見送り |
| 2026-03-10 | GitHub Actions CI修正: --api-keyフラグ追加→無効→削除(12cbaf7)。環境変数認証に統一 |
| 2026-03-10 | taipei.html ホテル比較タブに朝食リンクボタン追加・push済み (71eed7a) |
| 2026-03-09 | macau.html Day 5夕食→Kapok六棉酒家(Bib Gourmand)に変更・push済み (08f9174) |
| 2026-03-09 | 台北ホテル4軒追加+push。GitHub Actionsワークフロー修正・APIキー設定。クレジット反映待ちで一時保留 (act-011) |
| 2026-03-09 | iuma-private gnav統一（全7ページ）→ Travel=trip-planner。Cloudflareデプロイ完了 |
| 2026-03-08 | HANDOFF.md整理: macau push完了反映、進行中/次回アクション/ブロッカー更新 |
| 2026-03-07 | macau.html Day3夕食→フィッシャーマンズ・ワーフ（金悅軒/RIO Grill 2候補）+ ナイトバス20:30 Klook予約済み。push済み (fb210f5) |
| 2026-03-07 | macau.html Day3ブランチ→Common Table + Ho's Cafe。ルーレット攻略法追加。push済み (3a05c1e, c3f84d7) |
| 2026-03-07 | iUMAデザインシステム統一（全3ページ）。セクションナビにモバイルハンバーガー追加。design-system.md作成 |
| 2026-03-06 | taipei.html 新規作成（飲茶×LGBTQ+×夜市×烏龍茶）。4泊/5泊デュアルプラン、2名旅行対応 |
| 2026-03-06 | index.html更新（London→Cancelled, Taipei→Upcoming） |
