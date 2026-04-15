# HANDOFF

## [Constancy] 2026-04-14
- [ERROR] github_actions_health: Trip Planner: 'Update Trip Plan' 2回連続失敗. `gh run view --repo ymatz28-beep/trip-planner --log-failed` で確認

## Last Updated
2026-04-12

## プロジェクト概要
- **リポジトリ**: ymatz28-beep/trip-planner (GitHub Pages)
- **URL**: https://ymatz28-beep.github.io/trip-planner/
- **ローカルパス**: `~/Documents/Projects/trip-planner/`
- **構成**: index.html（ダッシュボード）、taipei.html、taipei-food.html、macau.html、london.html、fukuoka.html、kirishima.html（計7ページ）
- **デザイン**: iUMA report-dashboard のデザインシステムに準拠（Inter フォント、共通 gnav）

## 台北旅行の概要
- **日程**: 2026年4月16日〜20日（4泊5日）**確定**
- **フライト**: EVA Air HND↔TSA（BR191/190）¥55,376/人 **予約済み**（Agoda予約ID 1707813388 / PNR FD79EM）
- **ホテル**: 相鉄グランドフレッサ台北西門 **予約済み**
- **空港**: 台北松山空港 TSA（MRT文湖線+板南線 約20分で西門）
- **人数**: 2名（Yuma + 大木くん）
- **テーマ**: 飲茶 × LGBTQ+ × 夜市 × 烏龍茶
- **大木くん**: 酒飲み。クラフトビール、カクテル好き
- **Yuma**: ノンアル。LGBT。食（小籠包、飲茶、夜市B級グルメ）重視
- **注目イベント**: 4/18（土）= WERK! @ Triangle（毎月第3土曜の台北最大級ゲイナイト）

## Completed (taipei.html 全店舗にGoogle Mapsリンク追加 2026-04-11)
- **Before**: taipei.html の全21店舗（面線町、寧夏夜市、小品雅廚、北北車魯肉飯、朱記餡餅、Ice Monster、饒河夜市、四海豆漿大王、永康牛肉麵、嘟嘟水餃、南機場夜市、富錦台菜香檳、李記豆漿、大稻埕米粉湯 等）がプレーンテキストで、タップしても地図が開かなかった
- **After**: 全21店舗の店名にGoogle Mapsリンク（`<a href="https://maps.google.com/?q=..." target="_blank">`）を付与。CSSに `.meal-name a` スタイル追加（ドット下線+ホバーでピンク色変化）。スマホで店名タップ→即Google Maps遷移が可能に
- **Commits**: 未コミット

## Completed (Constancy警告 デザイントークン残存修正 2026-04-09)
- **Before**: london.html L1180/L1211に `color:#f87171`（2箇所）、taipei-food.html L35に `color:#6366f1`（1箇所）がハードコードで残存。Constancy design_token_complianceが3件WARN検出
- **After**: london.html `#f87171`→`var(--red-light)` 2箇所修正。taipei-food.html `#6366f1`→`var(--accent)` 1箇所修正。Constancy WARN 3件→0件
- **Commits**: 未コミット

## Completed (霧島旅行ガイド kirishima.html Day1行程最適化 2026-04-09)
- **Before**: Day1午後に硫黄谷温泉（霧島ホテル立ち寄り湯）が含まれていたが、界 霧島の露天風呂で十分。温泉ガイドが3湯構成（朝・昼外湯・夜）で冗長。帰着16:30で道の駅が未訪問
- **After**: 硫黄谷温泉を削除し、空いた時間に道の駅 霧島（標高630m展望台・桜島パノラマ）を追加。温泉ガイドを2湯構成（朝湯05:50・夜湯21:00の界露天のみ）に簡素化。帰着16:00に前倒し。PM DRIVEヘッダー「12:30–17:00」→「12:30–16:00」。就寝セクションにチェックアウト11:00の注記追加
- **Commits**: trip-planner `680f7e2`

## Completed (iUMAデザインシステムトークン統一 2026-04-06)
- **Before**: trip-planner全HTMLページのスタイルがiUMAデザインシステムのCSS変数（design_tokens.py由来）と不整合。ハードコードされた色・フォント値が残存
- **After**: 全HTMLページをiUMAデザインシステムトークンに統一。CSS変数準拠に修正
- **Commits**: trip-planner `23b5f9a`

## Completed (gnav Pattern B導入 + Cisco昇格 2026-04-06)
- **Before**: gnavが全13項目フラット表示で横スクロール発生。HealthがprimaryでCiscoがoverflow（⋯）に格下げされていた
- **After**: Pattern B gnav実装（primary 5項目常時表示 + ⋯ドロップダウン8項目）。Primary: Stock/Market Intel/Cisco/Action/Property。Overflow: Wealth/Insight/Health/Travel/Newsletter/Bookmarks/SNS/Self-Insight。モバイル640px以下はハンバーガー→全13項目フラットリスト。`lib/renderer.py` get_nav_html() + `nav.html` テンプレート両方対応
- **Commits**: lib renderer.py（uncommitted、trip-planner外）

## Completed (Projects CLAUDE.md Skill Routing追加 2026-03-27)
- **Before**: Projects/CLAUDE.mdにスキル自動発火ルールがなく、ユーザーがコマンド名を覚えて明示的に呼ぶ必要があった。story-intakeの発火トリガーに「インタビューして」が含まれていなかった
- **After**: Skill Routing表をCLAUDE.mdに追加（8スキルの自動発火ルール定義）。story-intakeトリガーに「インタビューして」追加。trip-planner自体のコード変更なし
- **Commits**: Projects CLAUDE.md（uncommitted、trip-planner外）

## Completed (ゾロ推薦グルメ全日程組込み 2026-03-23)
- **Before**: taipei.htmlにゾロ推薦のレストランが未統合。推薦元タグなし。航空券・ホテル金額が仮値
- **After**: 全5日にゾロ推薦グルメ組込み（Day1=港都熱炒+王福芋圓〜Day5=大稻埕米粉湯+李記豆漿）。全レストランに推薦元タグ付与。正式金額反映（航空券¥55,376・ホテル¥72,814・1人精算¥128,190）。銘水善樂→朱記餡餅に差替え
- **Commits**: trip-planner e81dca8, 5f39105, 22053d7

## Completed (fukuoka.html新規作成 2026-03-22)
- **Before**: 福岡ガイドページが存在しなかった
- **After**: fukuoka.html作成（ふくの湯3店舗のローカルガイド）。iUMAデザインシステム準拠。index.htmlにFukuokaリンク追加
- **Commits**: trip-planner 2f24845, 40f9062

## 進行中 / 未完了
- **fukuoka.html 全面改修（未着手）**: 現状はふくの湯3店舗のみの不完全状態。以下セクションの追加が必要:
  - **サウナ施設拡充**: ヨーガンレーベン（中央区）、ウェルビー福岡（博多区）、Nayuta THE VANISH（久山町 — 2024/12火災→2025/12改修再開予定、2026/3現在は営業再開済みの見込み）、アマンティ（筑紫野）、清流（那珂川）、天拝の湯（筑紫野）、伊都の湯どころ、The Riverside Sauna、らかんの湯（武雄）
  - **温泉セクション**: 二日市温泉 博多湯、脇田温泉、古湯温泉（佐賀）、原鶴温泉、武雄温泉、嬉野温泉、平山温泉（熊本）、湯布院、別府温泉、黒川温泉（熊本）
  - **ドライブコース**: 佐賀（吉野ヶ里+古湯/武雄+御船山/嬉野/唐津・呼子）、糸島（二見ヶ浦/花塩プリン/牡蠣小屋/海沿いカフェ）
  - **モデルプラン**: 半日（太宰府or糸島）/ 1日（佐賀ドライブ）/ 1泊2日 / 2泊3日
  - **市内観光拡充**: 太宰府天満宮（仮殿2026/5まで限定）、志賀島、能古島、櫛田神社、柳川川下り、門司港レトロ、篠栗九大の森
  - **グルメ拡充**: ごぼう天うどん、鉄鍋餃子、呼子イカ、明太子
- **fukuoka.html アクセント色ずれ**: 指定#FF8C42(warm amber)に対し実装は#C47D4E。要確認・修正判断

## 次回アクション（優先順）
1. **fukuoka.html 全面改修実行**: サウナ9施設/温泉10箇所/ドライブ2コース/モデルプラン/市内観光・グルメ拡充。macau.htmlのデザインパターンを参考に同品質で構築
2. **fukuoka.html アクセント色修正判断**: #C47D4E→#FF8C42に修正するか（全面改修と同時対応推奨）
3. **台北 最終調整**: 日程表の各スポット時間配分、移動ルート最適化（出発まで約23日）
4. **改善: taipei-food.htmlとtaipei.htmlのグルメ情報重複整理**: ゾロ推薦追加でtaipei.html内のグルメ密度が上がった。taipei-food.htmlとの役割分担・情報重複を整理する余地あり

## Key Decisions
- 2026-04-06: **gnav Pattern B採用（primary+overflow）** — 13項目を5 primary + 8 overflow(⋯ドロップダウン)に分割。Ciscoをprimaryに昇格、Healthをoverflowに降格（ユーザー指示）。モバイルはハンバーガーで全項目フラット表示
- 2026-03-23: **銘水善樂→朱記餡餅差替え** — 推薦元不明&高額の銘水善樂をゾロ推薦の朱記餡餅に差替え。Day3昼食
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
- 2026-04-06: **gnav Pattern B + Cisco昇格** — Primary: Stock/Market Intel/Cisco/Action/Property、Overflow(⋯): 8項目。Travelはoverflow側
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
- 台北出発まであと4日（4/16出発）— 未コミット変更あり（taipei.html Mapsリンク追加）
- GitHub Pages はキャッシュが強い: Cmd+Shift+R でハードリロード
- property-report, report-dashboardのGitHub Actions未テスト（キー設定のみ完了）

## 環境構築メモ
- 全て単一 HTML ファイル（CSS/JS 埋め込み）
- Leaflet.js（CDN）で地図。CARTO ダークタイル
- チェックリストは localStorage で状態保持
- 予算: 4泊確定。5泊タブ・switchPlan()/switchBudgetTab()は削除済み
- 共通 gnav: チェックボックスハックでハンバーガーメニュー（JS不要）
- デプロイ: `git push` → GitHub Pages 自動デプロイ

## History（最新20件）
- 2026-04-11: Before: taipei.html全21店舗がプレーンテキスト → After: 全店にGoogle Mapsリンク+CSSスタイル追加
- 2026-04-09: Before: london/taipei-foodに#f87171/#6366f1ハードコード3箇所 → After: var(--red-light)/var(--accent)に修正、Constancy WARN 0件
- 2026-04-09: Before: Day1に硫黄谷温泉(外湯)+温泉3湯構成 → After: 外湯削除+道の駅追加+界露天2湯に簡素化(680f7e2)
- 2026-04-06: Before: HTMLがiUMAデザインシステムトークン非準拠 → After: 全ページCSS変数統一(23b5f9a)
- 2026-04-06: Before: gnav13項目フラット表示 → After: Pattern B(primary5+overflow8⋯)+Cisco昇格
- 2026-03-27: Before: スキル自動発火ルールがCLAUDE.mdになかった → After: Skill Routing表追加+story-intake「インタビューして」トリガー追加（trip-planner変更なし）
- 2026-03-24: Before: gnav SSoTが未整備でfalse positive発生 → After: lib/renderer.py更新、kaizen patrol検証パス（trip-planner影響なし）
- 2026-03-23: Before: ゾロ推薦グルメ未統合・推薦元タグなし・金額仮値 → After: 全5日にゾロ推薦組込み+全店タグ付与+正式金額反映(e81dca8)
- 2026-03-22: Before: fukuoka.html改修の不足セクション未定義 → After: サウナ9施設/温泉10箇所/ドライブ2コース洗い出し完了。API 502で実装中断
- 2026-03-22: Before: fukuoka.htmlが存在しなかった → After: 作成+commit+push(2f24845)。index.htmlにFukuokaリンク追加
- 2026-03-22: Before: taipei.html+taipei-food.html未push → After: commit+push(40f9062)。マカオ完了マーク
- 2026-03-21: Before: QA巡回未実施 → After: trip-planner全5ファイルPublic→Private導線遮断チェック合格
- 2026-03-20: Before: trip-plannerがinfra-manifest未登録 → After: GitHub Pagesターゲット登録+constancy monitoring対象化
- 2026-03-20: Before: フライトセクションが冗長(4ブロック) → After: 1カードに圧縮(面積1/3)+taipei-food.html新規作成
- 2026-03-20: Before: trip-plannerがProjects root gitに混在 → After: .gitignoreにsubproject登録で独立管理化
- 2026-03-17: Before: kaizen-agentがtrip-plannerのGHAを未監視 → After: 監視追加、pages-build+Update Trip Plan両方確認(99b48b8)
- 2026-03-16: Before: 未予約候補・比較タブが残存(+177行) → After: Booked=Cleanで全削除。ルール#11制定(9454601)
- 2026-03-16: Before: フライト・ホテル未確定 → After: EVA Air NRT↔TPE+相鉄グランドフレッサ西門確定(5f9f3e0)
- 2026-03-10: Before: GitHub Actions APIキー認証が壊れていた → After: 環境変数認証に統一、Issue#10成功(36秒)
- 2026-03-10: Before: ホテル比較タブに朝食リンクなし → After: 朝食リンクボタン追加+push(71eed7a)
- 2026-03-09: Before: macau Day5夕食=誠昌飯店(3/5評価) → After: Kapok六棉酒家(Bib Gourmand, 4.1/5)に変更(08f9174)
- 2026-03-09: Before: 台北ホテル候補不足 → After: 4軒追加+push。GHA APIキー設定(クレジット待ち)