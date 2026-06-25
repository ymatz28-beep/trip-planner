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
import urllib.parse
import urllib.request
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
            for k in ('EXA_API_KEY', 'GOOGLE_KG_API_KEY'):
                if line.startswith(f'{k}=') and k not in keys:
                    keys[k] = line.split('=', 1)[1].strip()
    return keys


_WIKIPEDIA_JUNK_RE = re.compile(
    r'のメジャー通算\d+作目のシングル|のシングル.*発売|アルバム.*収録曲'
    r'|アニメ主題歌.*歌声|声優.*アーティスト'
    r'|歌手|楽曲|シングル|ミュージシャン|バンド'
    r'|映画|ドラマ|テレビ番組|アニメ|漫画'
    r'|サッカー選手|野球選手|プロレスラー|芸人'
)


def wikipedia_desc(name: str) -> str:
    """Wikipedia REST APIで日本語記事のexcerptを取得。観光地に有効。"""
    try:
        url = f'https://ja.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(name)}'
        req = urllib.request.Request(url, headers={'User-Agent': 'trip-planner-enrich/1.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            extract = data.get('extract', '')
            if extract and len(extract) > 20 and data.get('type') != 'disambiguation':
                if _WIKIPEDIA_JUNK_RE.search(extract[:100]):
                    return ''
                return extract[:200]
    except Exception:
        pass
    return ''


def kg_desc(name: str, api_key: str) -> str:
    """Google Knowledge Graph APIでエンティティの説明文を取得。"""
    try:
        params = urllib.parse.urlencode({'query': name, 'key': api_key, 'limit': 1, 'languages': 'ja'})
        url = f'https://kgsearch.googleapis.com/v1/entities:search?{params}'
        req = urllib.request.Request(url, headers={'User-Agent': 'trip-planner-enrich/1.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            items = data.get('itemListElement', [])
            if not items:
                return ''
            entity = items[0]['result']
            detail = entity.get('detailedDescription', {}).get('articleBody', '')
            desc = entity.get('description', '')
            text = detail if detail else desc
            return text[:200] if text and len(text) > 10 else ''
    except Exception:
        pass
    return ''


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


_TABELOG_SCORE_OG_RE = re.compile(r'[★☆]{5}(\d\.\d{1,2})')
_DESC_JUNK_SCRAPLING = re.compile(
    r'ログイン|無料会員登録|Yahoo! JAPAN'
    r'|ストーリーを見る|口コミ\s*写真\s*地図'
    r'|官方消息|已登錄|Switch to Tabelog'
    r'|店舗情報は食べログで|口コミや評価、写真など'
    r'|HAMONIでチェック'                              # HAMONIテンプレート
    r'|店舗情報（アクセス情報、口コミ\d+件）を掲載中'  # エキテンテンプレート
    r'|お店ページです。実名でのオススメが\d+件'        # Rettyテンプレート
    r'|リニューアル工事の為現在休業中'                 # 休業案内
    r'|のすべての客室タイプ'                           # ホテル予約サイトゴミ
    r'|テキストで学ぶことができます'                   # eラーニングサイト誤マッチ
)
_MOJIBAKE_RE = re.compile(r'[\x80-\xff]{3}|[^\x00-\x7f　-鿿＀-￯一-鿿]{4,}')


def scrape_desc_fallback(url: str) -> dict:
    """URLのmeta descriptionからdescを取得するフォールバック。tabelog URLはスコアも抽出。"""
    try:
        from scrapling.fetchers import Fetcher
        r = Fetcher().get(url, follow_redirects=True, timeout=15)
    except Exception as e:
        print(f'    Scrapling失敗: {e}')
        return {}

    desc = ''
    score_tabelog = ''

    meta = r.find('meta[name="description"]')
    meta_content = meta.attrib.get('content', '') if meta else ''
    og = r.find('meta[property="og:description"]')
    og_content = og.attrib.get('content', '') if og else ''

    if 'tabelog.com' in url:
        score_m = _TABELOG_SCORE_OG_RE.search(og_content)
        if score_m:
            score_tabelog = score_m.group(1)

        # metaから「チェック！」以降の実内容を抽出
        if '食べログでチェック！' in meta_content:
            after = meta_content.split('食べログでチェック！', 1)[1].strip()
            feat_m = re.search(r'【([^】]+)】', after)
            features = f'【{feat_m.group(1)}】' if feat_m else ''
            before = re.split(r'【|口コミ', after, maxsplit=1)[0].strip()
            # featureタグのみ（実質コンテンツなし）は捨てる
            if before and len(before) > 5:
                parts = [p for p in [before, features] if p]
                desc = ' '.join(parts)[:200]
    else:
        raw = og_content if len(og_content) > 20 else meta_content
        desc = raw[:200] if len(raw) > 20 else ''

    if _DESC_JUNK_SCRAPLING.search(desc):
        desc = ''
    if desc and _MOJIBAKE_RE.search(desc):
        desc = ''
    # 住所のみ（実質コンテンツなし）
    if desc and re.match(r'^住所[:：]', desc):
        desc = ''

    return {'desc': desc, 'score_tabelog': score_tabelog}


def main():
    limit = None
    refill = '--refill' in sys.argv   # descが空のスポットを再Enrich
    retier = '--retier' in sys.argv   # 全件再Enrich（tier + desc + score 全更新）
    scraping_only = '--scraping-only' in sys.argv  # EXAスキップ・Scraplingのみ
    if '--limit' in sys.argv:
        idx = sys.argv.index('--limit')
        limit = int(sys.argv[idx + 1])

    spots = json.loads(SPOTS_FILE.read_text())
    enriched_list = json.loads(ENRICHED_FILE.read_text()) if ENRICHED_FILE.exists() else []

    enriched_map = {s['name']: s for s in enriched_list}

    if retier:
        targets = spots
        mode = '全件retier'
    elif refill or scraping_only:
        targets = [s for s in spots if not enriched_map.get(s['name'], {}).get('desc')]
        mode = 'scraping-only（desc空）' if scraping_only else 'refill（desc空）'
    else:
        enriched_names = {s['name'] for s in enriched_list}
        targets = [s for s in spots if s['name'] not in enriched_names]
        mode = '新規'

    if limit:
        targets = targets[:limit]

    print(f'{mode}: {len(targets)}件')

    keys = {}
    if not scraping_only:
        keys = load_keys()
        if 'EXA_API_KEY' not in keys and not refill:
            print('EXA_API_KEY が未設定')
            sys.exit(1)

    for i, spot in enumerate(targets, 1):
        print(f'[{i}/{len(targets)}] {spot["name"]}...')
        existing = enriched_map.get(spot['name'], spot)

        if refill:
            # --refill: Wikipedia → KG → EXA の3段フォールバック
            merged = {**existing, 'desc': existing.get('desc', ''), 'tier': existing.get('tier', 3)}

            # 1. Wikipedia（無料・観光地特化）
            d = wikipedia_desc(spot['name'])
            if d:
                merged['desc'] = d
                print(f'  Wikipedia: {d[:60]}...')

            # 2. Google Knowledge Graph（無料・有名店）
            if not merged.get('desc') and keys.get('GOOGLE_KG_API_KEY'):
                d = kg_desc(spot['name'], keys['GOOGLE_KG_API_KEY'])
                if d:
                    merged['desc'] = d
                    print(f'  KG: {d[:60]}...')

            # 3. EXA（課金・全ジャンル）
            if not merged.get('desc') and keys.get('EXA_API_KEY'):
                info = enrich_spot(spot, keys)
                if info:
                    merged = {
                        **merged,
                        'addr':          info.get('addr') or existing.get('addr', ''),
                        'desc':          info.get('desc', ''),
                        'hours':         info.get('hours') or existing.get('hours', ''),
                        'score_google':  info.get('score_google', ''),
                        'score_tabelog': info.get('score_tabelog', ''),
                        'tier':          info.get('tier', existing.get('tier', 3)),
                        'source_url':    info.get('source_url', ''),
                    }
                    score_str = f" G:{merged['score_google']}" if merged['score_google'] else ""
                    print(f'  EXA: tier={merged["tier"]}{score_str} | {merged.get("addr","")[:30]}')
                else:
                    print('  EXA取得失敗')

            # 4. Scrapling（URL有りの場合）
            if not merged.get('desc') and merged.get('source_url'):
                print(f'  Scrapling: {merged["source_url"][:60]}...')
                fb = scrape_desc_fallback(merged['source_url'])
                if fb.get('desc'):
                    merged['desc'] = fb['desc']
                    if fb.get('score_tabelog') and not merged.get('score_tabelog'):
                        merged['score_tabelog'] = fb['score_tabelog']
                    print(f'  → desc取得: {merged["desc"][:60]}...')
                else:
                    print('  → 全フォールバック失敗')

        elif scraping_only:
            merged = {**existing, 'desc': existing.get('desc', ''), 'tier': existing.get('tier', 3)}
            info = None
        else:
            info = enrich_spot(spot, keys)
            if info:
                merged = {
                    **existing,
                    'addr':          info.get('addr') or existing.get('addr', ''),
                    'desc':          info.get('desc', ''),
                    'hours':         info.get('hours') or existing.get('hours', ''),
                    'score_google':  info.get('score_google', ''),
                    'score_tabelog': info.get('score_tabelog', ''),
                    'tier':          info.get('tier', existing.get('tier', 3)),
                    'source_url':    info.get('source_url', ''),
                }
                score_str = f" G:{merged['score_google']}" if merged['score_google'] else ""
                print(f'  EXA: tier={merged["tier"]}{score_str} | {merged.get("addr","")[:30]}')
            else:
                merged = {**existing, 'desc': existing.get('desc', ''), 'tier': existing.get('tier', 3)}
                print('  EXA取得失敗')

            # descが空でsource_urlがある場合はScraplingフォールバック
            if not merged.get('desc') and merged.get('source_url'):
                print(f'  Scraplingフォールバック: {merged["source_url"][:60]}...')
                fb = scrape_desc_fallback(merged['source_url'])
                if fb.get('desc'):
                    merged['desc'] = fb['desc']
                    if fb.get('score_tabelog') and not merged.get('score_tabelog'):
                        merged['score_tabelog'] = fb['score_tabelog']
                    print(f'  → desc取得: {merged["desc"][:60]}...')
                else:
                    print('  → フォールバックも失敗')

        enriched_map[spot['name']] = merged
        # 元の順番を保持して書き出し
        out = [enriched_map.get(s['name'], s) for s in spots if s['name'] in enriched_map]
        ENRICHED_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2))
        time.sleep(0.4)

    print(f'\n完了: {len(enriched_map)}件 → {ENRICHED_FILE}')


if __name__ == '__main__':
    main()
