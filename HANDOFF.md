# HANDOFF

## 最終更新: 2026-03-13

## プロジェクト概要
- **リポジトリ**: ymatz28-beep/trip-planner (GitHub Pages)
- **URL**: https://ymatz28-beep.github.io/trip-planner/
- **ローカルパス**: `~/Documents/Projects/trip-planner/`
- **構成**: index.html（ダッシュボード）、taipei.html、macau.html、london.html
- **デザイン**: iUMA report-dashboard のデザインシステムに準拠（Inter フォント、共通 gnav）

## 台北旅行の概要
- **日程**: 2026年4月15日〜19日（4泊5日）or 20日（5泊6日）— 未確定
- **人数**: 2名（Yuma + 大木くん）
- **テーマ**: 飲茶 × LGBTQ+ × 夜市 × 烏龍茶
- **大木くん**: 酒飲み。クラフトビール、カクテル好き
- **Yuma**: ノンアル。LGBT。食（小籠包、飲茶、夜市B級グルメ）重視
- **注目イベント**: 4/18（土）= WERK! @ Triangle（毎月第3土曜の台北最大級ゲイナイト）

## 完了済み（直近セッション）
- **GitHub Actions完全復旧**: `--api-key`フラグ削除(12cbaf7) + `github-actions`用APIキー再設定 → Issue #10 テスト成功（36秒で完了）
- **3リポ全てにANTHROPIC_API_KEY設定**: trip-planner, property-report, report-dashboard
- **Private側スマホ更新は見送り**: stock-analyzer/wealth-strategy/intelはリモートリポなし＆自動パイプライン生成のためROI低い。需要時に個別対応

## 前セッション完了
- GitHub Actions CI修正: `--api-key`フラグ追加(a211dda)→無効と判明→削除(12cbaf7)
- taipei.html ホテル比較タブに朝食リンクボタン追加・push済み (71eed7a)
- macau.html Day 5 夕食変更・push済み (08f9174): 誠昌飯店→Kapok六棉酒家(Bib Gourmand)
- 台北ホテル4軒追加 → taipei.html に push済み・GitHub Pages デプロイ済み
- iuma-private gnav統一（全privateページ）→ Cloudflareデプロイ完了

## 過去セッション完了
- taipei.html 新規作成（全セクション搭載）
- index.html 更新（Taipei=Upcoming, Macau=Completed, London=Cancelled）
- iUMAデザインシステム統一（全3ページ）
- macau.html gnav拡張+Day選択+過去日程移動 (9291d75)
- london.html: キャンセル（中東リスク）→ Cancelled表示

## 進行中 / 未完了
- macau.html: レストラン予約 pending（Wing Lei, Chef Tam's, Antonio, House of Dancing Water）
- macau.html: Studio City 後半2泊が「検討中→予約へ」ステータス

## 次回アクション（優先順）
1. **マカオ予約確定**: Studio City 後半2泊 + ミシュランレストラン（Wing Lei, Chef Tam's, Antonio）+ House of Dancing Water チケット
2. **taipei-food.html の処理**: 内容は taipei.html に統合済み。削除するか確認
3. **航空券予約（台北）**: HND→TSA 推奨（EVA Air or China Airlines）。2名分
4. **ホテル予約（台北）**: amba Ximending or citizenM 推奨。4泊 or 5泊 確定後
5. **改善アイデア: property-report/report-dashboardのGitHub Actions動作テスト** — trip-plannerはIssue #10で確認済みだが、他2リポはキー設定のみで未テスト。各リポにテストIssueを投げて確認

## Key Decisions
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

## ブロッカー / 注意事項
- 台北出発まで約33日（4/15出発、本日3/13時点）
- **taipei-food.html が未追跡**: git status で `??` 状態。統合済みなら削除、残すならコミット
- GitHub Pages はキャッシュが強い: Cmd+Shift+R でハードリロード
- property-report, report-dashboardのGitHub Actions未テスト（キー設定のみ完了）

## 技術メモ
- 全て単一 HTML ファイル（CSS/JS 埋め込み）
- Leaflet.js（CDN）で地図。CARTO ダークタイル
- チェックリストは localStorage で状態保持
- 4泊/5泊切り替え: `switchPlan()` JS関数でDOM表示切り替え
- 予算タブ: `switchBudgetTab()` で4泊/5泊の予算切り替え
- 共通 gnav: チェックボックスハックでハンバーガーメニュー（JS不要）

## History
| 日付 | サマリー |
|------|----------|
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
| 2026-03-05 | macau.html — Day 1 ラウンジにゲート近接情報+制限エリア内カフェ6店追加 (7398ae6) |
| 2026-03-04 | macau.html — クレカラウンジ金剛のゴールドカード入場条件+同伴者料金追加 (806c2c3) |
| 2026-03-04 | iUMA 共通 gnav 追加 + Inter フォント統一 + london/macau モバイル強化 |
| 2026-03-03 | 緊急バナー追加 + フライト/ホテル価格更新 + 予算再計算 |
| 2026-02-26 | ロンドン旅行ページ完成（農園・食・LGBTQ+・予算・チェックリスト・マップ全搭載） |
