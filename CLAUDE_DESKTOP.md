# Trip Planner — Claude Desktop 連携指示

## あなたの役割
ユーザー（Yuma）から旅行プランの変更・追加・改善指示を受け、trip-plannerのHTMLファイルを直接編集し、デプロイまで行う。

## プロジェクト情報
- **ローカルパス**: `/Users/yumatejima/Documents/Projects/trip-planner/`
- **公開URL**: https://ymatz28-beep.github.io/trip-planner/
- **ファイル構成**: index.html（ハブ）、taipei.html、macau.html、london.html
- **デプロイ**: `git add → commit → push origin main` で GitHub Pages に自動反映

## ワークフロー
1. ユーザーが変更内容を伝える（テキスト、スクショ、URL等）
2. `HANDOFF.md` を読んで現状を把握
3. 該当HTMLファイルを編集
4. commit & push してデプロイ
5. 公開URLを返す

## 変更パターン例
- 「Day 3のランチをRAWに変更」→ taipei.html の日程セクションを編集
- 「ホテル予約した。amba Ximending、4泊」→ ホテルセクションに予約済みマーク追加、日程確定
- 「フライト取った。EVA BR189、4/15 10:50発」→ フライト情報を確定表示に更新
- 「このレストラン追加して」+ URL → WebFetchで情報取得、グルメセクションに追加
- 「予算更新。航空券¥42,000だった」→ 予算セクションの実績値を更新
- 「チェックリストの航空券予約を完了にして」→ チェックリスト更新
- スクショ貼り付け → UIの問題を特定して修正

## デザインルール
- **フォント**: Inter + Noto Sans JP + JetBrains Mono。Playfair Display禁止
- **ヒーロー**: コンパクトカード型。min-height:100vh禁止
- **カラー**: iUMAトークン（--bg:#050507, --text:#f5f5f7, --muted:#71717a）+ ページアクセント
- **詳細**: `memory/design-system.md` を参照

## 注意
- push後はGitHub Pagesキャッシュ(10分)がある。Cmd+Shift+Rでハードリロードを案内
- センシティブ情報（LGBTQ+等）はヒーローに入れない
- HANDOFF.md も変更に合わせて更新する
