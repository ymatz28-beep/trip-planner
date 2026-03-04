# HANDOFF

## 最終更新: 2026-03-04

## プロジェクト概要
- **リポジトリ**: ymatz28-beep/trip-planner (GitHub Pages)
- **URL**: https://ymatz28-beep.github.io/trip-planner/
- **ローカルパス**: `~/Documents/Projects/trip-planner/`
- **構成**: index.html（ダッシュボード）、london.html、macau.html
- **デザイン**: iUMA report-dashboard のデザインシステムに準拠（Inter フォント、共通 gnav）

## ロンドン旅行の概要
- **日程**: 2026年3月27日〜4月5日（8泊10日）
- **人数**: 2名（ユーザー + 大木くん）
- **テーマ**: ヘレボルス農園見学 × 食の旅 × LGBTQ+ ナイトライフ
- **大木くん**: カリスマ育種家。クリスマスローズ専門。酒豪
- **ユーザー**: 食（カフェ、パン、紅茶、アフタヌーンティー）重視。お酒飲めない。LGBT

## 完了済み
- ダッシュボード（index.html）: iUMA デザインシステムに統一。London + Macau のみ
- **共通 gnav 追加**: 全ページに iUMA サイトヘッダー（Stock/Property/Wealth/Action リンク）。モバイルハンバーガーメニュー対応
- **フォント統一**: Outfit → Inter に変更（iUMA デザインシステム準拠）
- **Back link 追加**: london.html / macau.html に固定位置の「← 戻る」リンク
- **モバイル対応強化**: london.html / macau.html に 640px / 480px ブレークポイント追加。グリッド1カラム化、マップ縮小、フォント clamp 対応、タイムライン簡略化
- フライト検索: Google Flights のみ（Skyscanner, KAYAK, Turkish, ANA リンクは削除済み）
- フライト候補: #1 アシアナ航空（ICN経由・最安最短）、#2 ターキッシュ（IST経由）
- ホテル: 3ティア（Best Value / Smart Choice / Budget）+ エリア別おすすめ（Soho推奨）
- ホテル検索リンク: Google Hotels, Trivago, Agoda, Booking.com, Hotels.com（3/27 & 3/28 の2パターン）
- 日程表: 10日間フル（農園 Day4-5、食 Day2,3,6,7、LGBTQ+ 各夜）
- 農園ハイライト: ページ最上部に大木くん向けセクション（Ashwood, Hazles Cross, Buckland）
- レストラン: カテゴリ別（Afternoon Tea / Bakery / Restaurant / Japanese & Asian / Market / LGBTQ+ Nightlife）
- LGBTQ+: Comptons, Admiral Duncan, Ku Bar, The Yard, The Glory, RVT, Heaven, She Soho
- ノンアル情報: Seedlip, Lucky Saint, mocktail 文化の説明
- マップ: Leaflet.js + CARTO ダークタイル。食・農園・LGBTQ+ スポット全マーカー
- 予算: 農園移動費（列車・Stourbridge 1泊・タクシー）込み。3パターン（62-104万円）
- 予約管理: 農園連絡・列車・レストラン・アフタヌーンティー全項目
- チェックリスト: 農園見学グッズ、事前連絡、Ritz ドレスコード、Trainline アプリ等
- Tips: 農園マナー、苗持ち帰り（植物検疫）、列車、Soho LGBTQ+、サマータイム
- **緊急バナー**: ナビ直下に「出発まで○日 / 全予約未完了」の動的バナー追加
- **フライト価格更新**: 「早期予約」→「今すぐ予約」に変更 + アシアナ・ターキッシュ公式直リンク追加
- **ホテル価格更新**: Z Hotel Soho £90~/泊、citizenM £120~/泊（2026年3月レート）+ 公式直リンク追加
- **予算再計算**: ホテル価格更新に伴い合計を修正（おすすめ: 70〜93万円、快適: 75〜104万円）

## 進行中 / 未完了
- 全予約が pending 状態（航空券・ホテル・レストラン・農園連絡すべて未予約）
- index.html / london.html / macau.html の変更が未コミット・未デプロイ（gnav追加、フォント統一、モバイル強化、back link）

## 次回アクション（優先順）
1. **未コミット変更をコミット＆デプロイ**: gnav追加・Inter フォント・モバイル強化・back link の変更を push → GitHub Pages 反映
2. **航空券が決まったら**: 具体的な便名・時刻・価格を flights セクションに反映
3. **ホテルが決まったら**: 確定ホテルを hotels セクションにハイライト、マップのホテルマーカー更新
4. **Buckland Cottage Gardens**: Instagram DM の返答待ち。訪問可なら Day 8 確定、不可なら代替（RHS Wisley）に
5. **Ashwood / Hazles Cross への電話**: 大木くんが連絡 → 結果を反映
6. **レストラン予約**: Sketch, Ritz/Claridge's, Dishoom, St. JOHN, Brat/Clove Club → 予約状況を reservations に反映（pending → confirmed）
7. **改善アイデア**: gnav を共通 CSS ファイルに分離し、全ページで `<link>` 読み込みに変更 → gnav 更新時の3ファイル同時修正を不要にする

## Key Decisions
- 2026-02-26: デザインシステムは iUMA report-dashboard に統一
- 2026-02-26: 全て単一 HTML ファイル（CSS/JS 埋め込み）で構成
- 2026-02-26: 地図は Leaflet.js + CARTO ダークタイル
- 2026-03-03: プロジェクトを `~/trip-planner/` → `~/Documents/Projects/trip-planner/` に移動（ディレクトリ整理の一環）
- 2026-03-03: 緊急バナー導入 — 出発24日前で全予約未完了のため、ページ上部に動的カウントダウン+未予約数を常時表示
- 2026-03-03: ホテル価格を公式2026年3月レートに更新（Z Hotel £90~/泊、citizenM £120~/泊）
- 2026-03-04: フォントを Outfit → Inter に統一（iUMA 共通デザインシステム準拠）
- 2026-03-04: 全ページに iUMA 共通 gnav（サイトヘッダー）を追加。report-dashboard ハブとの統一
- 2026-03-04: Trip Planner が iUMA 公開ハブ（report-dashboard）のカテゴリに掲載
- 2026-03-04: london.html / macau.html にモバイル 640px / 480px ブレークポイント追加
- 2026-03-04: macau.html — 通貨・両替セクション新設、PPラウンジ+スタアラGold情報、ジム情報、ショー情報、全日程Mapsリンク追加

## コンテンツ品質ルール（trip-planner 固有）
旅行ページを新規作成・更新する際は、以下を**初回から**漏れなく含めること。追加指示は不要。

1. **日程の全スポットにGoogle Mapsリンク**: `<a href="https://maps.google.com/?q=..." target="_blank" style="color:var(--gold);">📍 Map</a>` を activity-desc 末尾に必ず付与
2. **空港ラウンジ情報**: PP / スタアラGold / SFC の利用可否を空港ごとに明記。人数別の最適戦略（ゲスト料金等）も記載
3. **ショー・エンタメ情報**: 有名ショー（有料/無料）のスケジュール・価格・予約リンクを日程に組み込む
4. **通貨・両替セクション**: 現地通貨の基本、両替レート比較（場所別）、おすすめ戦略
5. **ジム情報**: 宿泊ホテルのジム名・場所・営業時間・設備をホテルカードに記載
6. **マイレージ情報**: 利用航空会社の提携マイレージ積算可否・予約クラス別積算率
7. **時系列の整合性**: 日程表のタイムラインは必ず時刻順。空港到着→ラウンジ→搭乗の流れを守る
8. **リンク生存確認**: Google Mapsリンクは `https://maps.google.com/?q=スポット名+地域名` 形式で統一。固有ID依存のリンクは避ける

## ブロッカー / 注意事項
- **出発まで23日（3/27出発、本日3/4時点）** — 航空券・ホテル・レストラン全て未予約。即行動が必要
- Google Flights の protobuf URL: `tfs` パラメータに base64url エンコードされた protobuf。東京 `/m/07dfk`、ロンドン `/m/04jpl`
- GitHub Pages はキャッシュが強い: 更新が反映されない場合は Cmd+Shift+R でハードリロード
- イースター（4/5）: 4/3〜4/4 はホテルが高くなる傾向。早期予約推奨
- サマータイム（3/29）: Day 3 の朝に1時間ロス
- macau.html は別の旅行（家族4人、3/5-10）で、ロンドン旅行とは無関係

## 技術メモ
- 全て単一 HTML ファイル（CSS/JS 埋め込み）
- Leaflet.js（CDN）で地図。CARTO ダークタイル
- チェックリストは localStorage で状態保持
- ホテル予約リンクの URL パラメータ: Booking.com (`ss=London&checkin=...`), Agoda (`city=15465`), Trivago (`search=200-17680`)
- 共通 gnav: チェックボックスハックでハンバーガーメニュー実装（JS不要）

## History
- 2026-03-04: iUMA 共通 gnav 追加 + Inter フォント統一 + london/macau モバイル強化（640px/480px BP）+ back link 追加 + 公開ハブ掲載。未デプロイ
- 2026-03-03: 緊急バナー追加 + フライト/ホテル価格を2026年3月レートに更新 + 予算再計算 + 公式直リンク追加。デプロイ済み
- 2026-03-03: ファイル整理で `~/` → `~/Documents/Projects/` に移動
- 2026-02-26: ロンドン旅行ページ完成（農園・食・LGBTQ+・予算・チェックリスト・マップ全搭載）
