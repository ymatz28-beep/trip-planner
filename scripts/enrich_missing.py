#!/usr/bin/env python3
"""
未Enrichスポットを1件ずつExa検索してokinawa_enriched.jsonに追記する。
おすすめ度も自動判定（有名・高評価 → tier 2、通常 → tier 3）。

Usage:
  python scripts/enrich_missing.py           # 全件
  python scripts/enrich_missing.py --limit 20  # 最初の20件のみ（テスト用）
"""

import json
import re
import sys
import time
from pathlib import Path

SPOTS_FILE = Path(__file__).parent.parent / 'okinawa_spots_tmp.json'
ENRICHED_FILE = Path(__file__).parent.parent / 'okinawa_enriched.json'


def load_keys():
    keys = {}
    for p in [
        Path(__file__).parent.parent / '.env',
        Path.home() / 'Documents/Projects/x-bookmarks/.env',
        Path.home() / 'Documents/Projects/sns-auto/.env',
        Path.home() / '.env',
    ]:
        if not p.exists():
            continue
        for line in p.read_text().splitlines():
            k = 'EXA_API_KEY'
            if line.startswith(f'{k}=') and k not in keys:
                keys[k] = line.split('=', 1)[1].strip()
    return keys


# 汎用ワード（人気・おすすめ等）は除外し、特異性の高いキーワードのみで判定
# 2つ以上マッチ → tier 2（おすすめ）
STRICT_KEYWORDS = [
    '行列', '地元', '老舗', '元祖', '名店', '名物',
    'テレビ', 'メディア', '雑誌', '受賞', 'ミシュラン', '創業',
]
# 業種キーワードでカテゴリを強制上書き（EXA enrich時の誤分類防止）
# spot["category"] がこれらにマッチしたら正しいカテゴリに修正する
_CAT_OVERRIDES = [
    (re.compile(r'レンタカー|rent.?a.?car', re.I), 'activity'),
    (re.compile(r'サウナ|スパ|温泉(?!料理)|銭湯'), 'health'),
    (re.compile(r'ホテル|旅館|民宿|ゲストハウス|コンドミニアム'), 'lodging'),
    (re.compile(r'離島|島$|クルーズ|ダイビング|シュノーケル|カヤック|マリン'), 'activity'),
    (re.compile(r'カフェ|珈琲|コーヒー|スイーツ|ケーキ|パン屋|ベーカリー'), 'cafe_sweets'),
    (re.compile(r'ショッピング|百貨店|ドラッグストア|スーパー|無印良品|ユニクロ'), 'leisure'),
]

def infer_category(name: str, existing_cat: str) -> str:
    """スポット名から業種を判定し、誤分類なら上書きする。"""
    for pattern, cat in _CAT_OVERRIDES:
        if pattern.search(name):
            return cat
    return existing_cat

ADDR_RE = re.compile(r'沖縄県[^\s\n,、。]+')
HOURS_RE = re.compile(r'(?:営業時間|営業)[^\n]{0,60}(?:\d{1,2}:\d{2})[^\n]{0,60}')
# Googleスコア: 「4.2/5」「3.8 / 5」「Google 4.5」のいずれかにマッチ
GOOGLE_SCORE_RE = re.compile(r'(?:Google[^\d]{0,10})?([3-5]\.\d)(?:\s*/\s*5|\s*(?:点|stars?|star rating))')
# 食べログスコア: 「3.57 食べログ」「食べログ 3.57」
TABELOG_SCORE_RE = re.compile(r'(?:食べログ[^\d]{0,5}(\d\.\d{1,2})|(\d\.\d{1,2})[^\d]{0,5}食べログ)')


def enrich_spot(spot: dict, keys: dict) -> dict | None:
    from exa_py import Exa

    name = spot['name']
    region = spot.get('region', '沖縄')

    exa = Exa(api_key=keys['EXA_API_KEY'])
    try:
        results = exa.search(
            f'{name} {region} 沖縄',
            num_results=5,
            type='neural',
            contents={
                'text': {'max_characters': 1500},
                'highlights': {'num_sentences': 3, 'highlights_per_url': 2},
            },
        )
    except Exception as e:
        print(f'  Exa失敗: {e}')
        return None

    hits = results.results
    if not hits:
        return None

    all_text = '\n'.join(
        '\n'.join(getattr(r, 'highlights', []) or []) + '\n' + (r.text or '')
        for r in hits
    )

    addr_m = ADDR_RE.search(all_text)
    addr = addr_m.group(0)[:40] if addr_m else ''

    hours_m = HOURS_RE.search(all_text)
    hours = hours_m.group(0).strip() if hours_m else ''

    gsc_m = GOOGLE_SCORE_RE.search(all_text)
    score_google = gsc_m.group(1) if gsc_m else ''

    tab_m = TABELOG_SCORE_RE.search(all_text)
    score_tabelog = (tab_m.group(1) or tab_m.group(2)) if tab_m else ''

    # highlightsのみ使用。raw textはUIゴミが混入するので使わない
    # ゴミパターン: #ヘッダー・多言語切り替え・ページタイトル区切り・ハングル・中国語切替
    _junk_line = re.compile(
        r'^#|^\d{3}-\d{4}|Switch to|Click here|English page'
        r'|[가-힣]'                       # ハングル
        r'|切[换換]到|简体中文|繁體中文|전환'   # 多言語切替
        r'|\d\s*/\s*\d{1,2}\s*(?:外観|写真|口コミ)'  # 写真ナビ「1/10 外観」
        r'|官方消息|已登錄|店家會員|本店相關'   # 繁体字中国語UIテキスト
        r'|ONLINE SHOP|Online Shop'        # 物販UI
        r'|\| ---|\| -'                    # Markdown表ヘッダー
    )
    def _clean_hl(hl: str, spot_name: str = name) -> str:
        lines = [l for l in hl.splitlines() if l.strip() and not _junk_line.search(l)]
        text = ' '.join(lines).strip()
        # ページタイトル「店名 - カテゴリ | サイト名」の先頭を除去
        if '｜' in text[:40] or ' | ' in text[:40]:
            text = re.split(r'｜| \| ', text, maxsplit=1)[-1].strip()
        # 先頭がスポット名の場合は「スポット名 - 」部分を除去
        if spot_name and text.startswith(spot_name):
            text = text[len(spot_name):].lstrip(' ‐－―-｜|・ ').strip()
        return text

    highlights = []
    for r in hits[:5]:
        for hl in (getattr(r, 'highlights', []) or [])[:3]:
            cleaned = _clean_hl(hl)
            if cleaned and len(cleaned) > 15:
                highlights.append(cleaned)
    desc = ' '.join(highlights[:5])[:200] if highlights else ''

    # ナビUI・ログインページ・繁体字UIテキスト等は空に落とす（gen_okinawa_v2.py の _DESC_JUNK と同期）
    _desc_junk = re.compile(
        r'ログイン|無料会員登録|Yahoo! JAPAN'
        r'|ストーリーを見る|口コミ\s*写真\s*地図|地図\s*お客様アンケート'
        r'|官方消息|已登錄|店家會員|本店相關'    # 繁体字中国語UIテキスト
        r'|Switch to Tabelog'                  # 英語切替
        r'|\| ---'                             # Markdown表形式
        r'|英語環境|HAMONI|English site is here'  # HAMONI系UIゴミ
        r'|tiktok\.com'                        # TikTok URL
        r'|エキテン\s*by|エキテン\s*GMO'        # エキテンUI
        r'|Retty（レッティ）'                   # Rettyページタイトル
        r'|なび沖】|全国なびから'               # なび沖UI
        r'|TEL:\d{3}'                          # 電話番号混入UI
    )
    # ｜が2つ以上→ページタイトルか表形式
    if _desc_junk.search(desc) or desc.count(' - ') + desc.count(' / ') > 4 or desc.count('｜') >= 2:
        desc = ''

    # クロス名汚染チェック: descの冒頭が「--」で始まる場合は別業者のハイライトが混入している
    if desc.startswith('--'):
        desc = ''

    # クロス名汚染チェック: desc内でスポット名と全く異なる固有名詞（『〇〇』形式）が先頭に出る場合はクリア
    _cross_contamination = re.compile(r"^(?:--|『[^』]{3,}』)")
    if _cross_contamination.search(desc):
        desc = ''

    # addrがページタイトル形式（「--」や「『』」で始まる）の場合もクリア
    addr = re.sub(r'^(?:--|『[^』]*』[^\d]*)', '', addr).strip()
    if not re.search(r'\d', addr):  # 番地数字がなければ住所として無効
        addr = ''

    strict_count = sum(1 for kw in STRICT_KEYWORDS if kw in all_text)
    # Googleスコアが有効範囲（3.5〜5.0）の場合もtier 2
    valid_google = gsc_m and 3.5 <= float(gsc_m.group(1)) <= 5.0
    tier = 2 if (strict_count >= 2 or valid_google) else 3

    corrected_cat = infer_category(name, spot.get('category', 'food'))

    return {
        'addr': addr,
        'desc': desc,
        'hours': hours,
        'score_google': score_google,
        'score_tabelog': score_tabelog,
        'tier': tier,
        'source_url': hits[0].url if hits else '',
        'category': corrected_cat,
    }


def main():
    limit = None
    refill = '--refill' in sys.argv   # descが空のスポットを再Enrich
    retier = '--retier' in sys.argv   # 全件再Enrich（tier + desc + score 全更新）
    if '--limit' in sys.argv:
        idx = sys.argv.index('--limit')
        limit = int(sys.argv[idx + 1])

    spots = json.loads(SPOTS_FILE.read_text())
    enriched_list = json.loads(ENRICHED_FILE.read_text()) if ENRICHED_FILE.exists() else []

    enriched_map = {s['name']: s for s in enriched_list}

    if retier:
        # 全件対象（tier + desc + score を全部更新）
        targets = spots
        mode = '全件retier'
    elif refill:
        # descが空のスポットのみ
        targets = [s for s in spots if not enriched_map.get(s['name'], {}).get('desc')]
        mode = 'refill（desc空）'
    else:
        enriched_names = {s['name'] for s in enriched_list}
        targets = [s for s in spots if s['name'] not in enriched_names]
        mode = '新規'

    if limit:
        targets = targets[:limit]

    print(f'{mode}: {len(targets)}件')
    keys = load_keys()
    if 'EXA_API_KEY' not in keys:
        print('EXA_API_KEY が未設定')
        sys.exit(1)

    for i, spot in enumerate(targets, 1):
        print(f'[{i}/{len(targets)}] {spot["name"]}...')
        info = enrich_spot(spot, keys)
        existing = enriched_map.get(spot['name'], spot)

        if info:
            merged = {
                **existing,
                'addr':         info.get('addr') or existing.get('addr', ''),
                'desc':         info.get('desc', ''),
                'hours':        info.get('hours') or existing.get('hours', ''),
                'score_google': info.get('score_google', ''),
                'score_tabelog':info.get('score_tabelog', ''),
                'tier':         info.get('tier', existing.get('tier', 3)),
                'source_url':   info.get('source_url', ''),
            }
            score_str = f" G:{merged['score_google']}" if merged['score_google'] else ""
            print(f'  tier={merged["tier"]}{score_str} | {merged.get("addr","")[:30]}')
        else:
            merged = {**existing, 'desc': existing.get('desc', ''), 'tier': existing.get('tier', 3)}
            print('  情報取得失敗→スキップ')

        enriched_map[spot['name']] = merged
        # 元の順番を保持して書き出し
        out = [enriched_map.get(s['name'], s) for s in spots if s['name'] in enriched_map]
        ENRICHED_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2))
        time.sleep(0.4)

    print(f'\n完了: {len(enriched_map)}件 → {ENRICHED_FILE}')


if __name__ == '__main__':
    main()
