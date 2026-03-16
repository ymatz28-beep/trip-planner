# HANDOFF

## 最終更新: 2026-03-16

## プロジェクト概要
- **リポジトリ**: ymatz28-beep/trip-planner (GitHub Pages)
- **URL**: https://ymatz28-beep.github.io/trip-planner/
- **ローカルパス**: `~/Documents/Projects/trip-planner/`
- **構成**: index.html（ダッシュボード）、taipei.html、macau.html、london.html
- **デザイン**: iUMA report-dashboard のデザインシステムに準拠（Inter フォント、共通 gnav）

## 台北旅行の概要
- **日程**: 2026年4月15日〜19日（4泊5日）**確定**
- **フライト**: EVA Air NRT↔TPE ¥54,840/人 **予約済み**
- **ホテル**: 相鉄グランドフレッサ台北西門 **予約済み**
- **空港**: 桃園国際空港（MRT 50分で市内）
- **人数**: 2名（Yuma + 大木くん）
- **テーマ**: 飲茶 × LGBTQ+ × 夜市 × 烏龍茶
- **大木くん**: 酒飲み。クラフトビール、カクテル好き
- **Yuma**: ノンアル。LGBT。食（小籠包、飲茶、夜市B級グルメ）重視
- **注目イベント**: 4/18（土）= WERK! @ Triangle（毎月第3土曜の台北最大級ゲイナイト）

## 完了済み（直近セッション）
- **Booked = Cleanクリーンアップ** (9454601): 予約確定に伴い未予約候補を全削除（-177行）
  - ホテル: ambaタブ・比較タブ・Google Hotels/Booking.com/Agoda検索リンク削除（相鉄確定）
  - 予算: 5泊タブ削除（4泊確定）
  - 日程サブタイトル調整
- **Booked = Cleanルール制定**: HANDOFF.mdコンテンツ品質ルール#11 + auto memory記録

## 前セッション完了
- **台北フライト＆ホテル確定** (5f9f3e0): EVA Air NRT↔TPE (¥54,840/人) + 相鉄グランドフレッサ台北西門。予算実コスト反映 (¥296k)
- GitHub Actions完全復旧: APIキー再設定 → Issue #10成功。3リポにシークレット設定
- taipei.html ホテル比較タブに朝食リンクボタン追加 (71eed7a)
- macau.html Day 5 夕食→Kapok六棉酒家(Bib Gourmand) (08f9174)

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
1. **taipei-food.html の処理**: git未追跡のまま放置。taipei.htmlに統合済みなら削除、残すならコミット
2. **マカオ予約確定**: Studio City 後半2泊 + ミシュランレストラン（Wing Lei, Chef Tam's, Antonio）+ House of Dancing Water チケット
3. **💡改善: taipei.html 桃園空港MRTの詳細ガイド追加** — 桃園MRT時刻表・悠遊卡購入場所・乗り換え案内を充実させる

## Key Decisions
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
- 台北出発まで約30日（4/15出発、本日3/16時点）
- **taipei-food.html が未追跡**: git status で `??` 状態。統合済みなら削除、残すならコミット
- GitHub Pages はキャッシュが強い: Cmd+Shift+R でハードリロード
- property-report, report-dashboardのGitHub Actions未テスト（キー設定のみ完了）

## 技術メモ
- 全て単一 HTML ファイル（CSS/JS 埋め込み）
- Leaflet.js（CDN）で地図。CARTO ダークタイル
- チェックリストは localStorage で状態保持
- 予算: 4泊確定。5泊タブ・switchPlan()/switchBudgetTab()は削除済み
- 共通 gnav: チェックボックスハックでハンバーガーメニュー（JS不要）

## History
| 日付 | サマリー |
|------|----------|
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
| 2026-03-05 | macau.html — Day 1 ラウンジにゲート近接情報+制限エリア内カフェ6店追加 (7398ae6) |
| 2026-03-04 | macau.html — クレカラウンジ金剛のゴールドカード入場条件+同伴者料金追加 (806c2c3) |
| 2026-03-04 | iUMA 共通 gnav 追加 + Inter フォント統一 + london/macau モバイル強化 |
| 2026-03-03 | 緊急バナー追加 + フライト/ホテル価格更新 + 予算再計算 |
| 2026-02-26 | ロンドン旅行ページ完成（農園・食・LGBTQ+・予算・チェックリスト・マップ全搭載） |
