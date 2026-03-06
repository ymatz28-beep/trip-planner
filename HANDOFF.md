# HANDOFF

## 最終更新: 2026-03-06

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

## 完了済み
- **taipei.html 新規作成**: 全セクション搭載
  - Hero（カウントダウン、4泊/5泊表示）
  - フライト（HND→TSA / NRT→TPE 比較、空港アクセス、マイレージ情報）
  - ホテル（3ティア7軒、ツイン/ダブル1室、Ximendingエリア）
  - 日程（4泊5日/5泊6日の切り替えタブ。Day 1-4共通、Day 5以降分岐）
    - 曜日修正済み: 4/15=水、4/16=木、4/17=金、4/18=土、4/19=日
    - Day 4(土): WERK! @ Triangle パーティー組み込み
    - 5泊Day 5: 猫空ゴンドラ＆茶藝体験、大稻埕茶葉ショッピング、紫藤廬
    - 大木くん飲酒/Yumaノンアル メモを各所に追加
  - グルメ（タブ: 飲茶&XLB / ファインダイニング / 夜市 / 朝食&カフェ）
  - 烏龍茶セクション（茶葉ショップ4店、茶館2軒、茶葉ガイド4品種、購入戦略）
  - お土産セクション（パイナップルケーキTOP3、その他お土産、買い物スポット、税関ルール）
  - LGBTQ+（紅樓バー4軒、クラブ3軒、サウナ4軒 含Soi 13in/Hans/XL/I/O詳細、ゲイナイトイベントカレンダー、アプリ&SNS、クルージングスポット）
  - 通貨&実用情報
  - 予算（2人合計×3ティア×4泊/5泊の6パターン。タブ切り替え）
  - Leaflet.jsマップ（18スポット: 食、LGBTQ+、茶、お土産）
  - チェックリスト（13項目、2名旅行対応、localStorage保存）
- **index.html 更新**: Taipei=Upcoming, Macau=Completed, London=Cancelled(bottom)。ヒーロー削除。TRIPS記述更新
- **london.html**: キャンセル（中東リスク）→ index上でCancelled表示
- **taipei-food.html**: 食リサーチエージェントが生成。taipei.htmlに統合済みのため削除検討

## 進行中 / 未完了
- 全変更が**未コミット・未デプロイ**（taipei.html, index.html, macau.html, london.html, HANDOFF.md）
- macau.html: レストラン予約多数 pending

## 次回アクション（優先順）
1. **コミット＆デプロイ**: 全ファイルを push → GitHub Pages 反映
2. **taipei-food.html の処理**: 内容は taipei.html に統合済み。削除するか確認
3. **航空券予約**: HND→TSA 推奨（EVA Air or China Airlines）。2名分
4. **ホテル予約**: amba Ximending or citizenM 推奨。4泊 or 5泊 確定後
5. **レストラン予約**: Din Tai Fung（永康街 or 信義A4）、銘水善 樂（要予約）

## Key Decisions
- 2026-03-06: ロンドン → 台北に変更（中東リスク）
- 2026-03-06: 4泊/5泊の両プラン並行準備（タブ切り替えUI）
- 2026-03-06: 2名旅行（Yuma + 大木くん）。大木くん=酒飲み、Yuma=ノンアル
- 2026-03-06: カラーテーマ: pink(#E8577A), teal(#00897B), gold(#D4A055)
- 2026-03-06: 4/18(土)=WERK!第3土曜パーティーをDay 4に組み込み
- 2026-03-07: iUMAデザインシステム統一。全ページ（taipei/macau/london）にType A gnav、コンパクトhero、Inter/JetBrains Monoフォント、統一トークン適用
- 2026-03-07: セクションナビにモバイルハンバーガー追加。640px以下でドロップダウン化
- 過去のDecisions → History参照

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
- **taipei.html 未デプロイ**: 変更をpushすれば即公開
- 台北出発まで約40日（4/15出発、本日3/6時点）
- GitHub Pages はキャッシュが強い: Cmd+Shift+R でハードリロード

## 技術メモ
- 全て単一 HTML ファイル（CSS/JS 埋め込み）
- Leaflet.js（CDN）で地図。CARTO ダークタイル
- チェックリストは localStorage で状態保持
- 4泊/5泊切り替え: `switchPlan()` JS関数でDOM表示切り替え
- 予算タブ: `switchBudgetTab()` で4泊/5泊の予算切り替え
- 共通 gnav: チェックボックスハックでハンバーガーメニュー（JS不要）

## History
- 2026-03-07: iUMAデザインシステム統一（全3ページ）。Playfair Display→Inter/JetBrains Mono、100vhヒーロー→コンパクトカード、旧トークン→iUMA標準、セクションナビにモバイルハンバーガー追加。design-system.md作成
- 2026-03-06: taipei.html 新規作成（飲茶×LGBTQ+×夜市×烏龍茶）。4泊/5泊デュアルプラン、2名旅行対応、茶・お土産・ゲイナイトイベント・ハッテン場 全セクション搭載。index.html 更新（London→Cancelled, Taipei→Upcoming）
- 2026-03-05: macau.html — Day 1 ラウンジにゲート近接情報+制限エリア内カフェ6店追加 (7398ae6)
- 2026-03-04: macau.html — クレカラウンジ金剛のゴールドカード入場条件+同伴者料金追加 (806c2c3)
- 2026-03-04: iUMA 共通 gnav 追加 + Inter フォント統一 + london/macau モバイル強化
- 2026-03-03: 緊急バナー追加 + フライト/ホテル価格更新 + 予算再計算
- 2026-02-26: ロンドン旅行ページ完成（農園・食・LGBTQ+・予算・チェックリスト・マップ全搭載）
