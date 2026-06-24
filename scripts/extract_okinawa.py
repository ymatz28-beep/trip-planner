#!/usr/bin/env python3
"""
Google Takeout ZIP から沖縄スポットを抽出して okinawa_spots_tmp.json に追記する。

Usage:
  python scripts/extract_okinawa.py ~/Downloads/takeout-*.zip
  python scripts/extract_okinawa.py ~/Downloads/takeout-20260413T025228Z-3-001.zip
"""

import csv
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote

# ======================= 沖縄HexID地域コード =======================
# Google Maps Place ID の ftid に含まれる上位プレフィックスで地域判定。
# 住所フィールドがないCSVでも店名に地名がなくても正確にフィルタできる。
OKINAWA_PREFIXES = ['0x34e5', '0x34f4', '0x345f', '0x3460']
# 0x34e5 = 那覇・本島
# 0x34f4 = 宮古島
# 0x345f = 石垣島  (※0x3546は大分別府、別物)
# 0x3460 = 久米島等その他離島
# ==================================================================

PRIORITY_FILES = [
    'グルメ.csv', 'カフェ.csv', '行ってみたい.csv',
    'パン・ケーキ.csv', 'ホテル.csv', 'デフォルト リスト.csv', 'お気に入りの場所.csv',
]

LIST_CATEGORY = {
    'グルメ':         ('food',        None),
    'カフェ':         ('cafe_sweets', 'cafe'),
    'パン・ケーキ':   ('cafe_sweets', 'bakery'),
    'ホテル':         ('stay',        'hotel'),
    '行ってみたい':   ('activity',    None),
    'デフォルト リスト': ('food',     None),
    'お気に入りの場所':  ('food',     None),
}

OUT_FILE = Path(__file__).parent.parent / 'okinawa_spots_tmp.json'


def is_okinawa_hex(url: str) -> bool:
    m = re.search(r'1s(0x[0-9a-f]+)', unquote(url))
    if not m:
        return False
    return any(m.group(1).startswith(p) for p in OKINAWA_PREFIXES)


def get_cid_url(url: str) -> str:
    m = re.search(r':0x([0-9a-f]+)', unquote(url))
    if m:
        return f'http://maps.google.com/?cid={int(m.group(1), 16)}'
    return url


def guess_region(url: str) -> str:
    m = re.search(r'1s(0x[0-9a-f]+)', unquote(url))
    if not m:
        return '那覇'
    p = m.group(1)
    if p.startswith('0x34f4'):
        return '宮古島'
    if p.startswith('0x345f'):
        return '石垣島'
    if p.startswith('0x3460'):
        return '離島'
    return '那覇'


def extract_csvs_from_zip(zpath: str) -> dict:
    """Takeout ZIP から保存済みリストのCSVを {basename: bytes} で返す。"""
    results = {}
    with zipfile.ZipFile(zpath) as zf:
        for info in zf.infolist():
            try:
                fname = info.filename.encode('cp437').decode('utf-8')
            except Exception:
                fname = info.filename
            if '.csv' not in fname.lower():
                continue
            if '保存済み' not in fname and 'saved' not in fname.lower():
                continue
            results[Path(fname).name] = zf.read(info.filename)
    return results


def parse_csv(data_bytes: bytes, list_name: str) -> list:
    text = data_bytes.decode('utf-8', errors='replace')
    category, sub = LIST_CATEGORY.get(list_name, ('food', None))
    spots = []
    for row in csv.DictReader(text.splitlines()):
        url = (row.get('URL') or row.get('url') or '').strip()
        title = (row.get('タイトル') or row.get('Title') or '').strip()
        if not url or not is_okinawa_hex(url):
            continue
        spot = {
            'name': title,
            'region': guess_region(url),
            'category': category,
            'maps_url': get_cid_url(url),
            'source_list': list_name,
        }
        if sub:
            spot['sub_category'] = sub
        spots.append(spot)
    return spots


def main(zip_paths: list):
    existing = json.loads(OUT_FILE.read_text()) if OUT_FILE.exists() else []
    seen_names = {s['name'] for s in existing}

    new_spots = []
    for zpath in zip_paths:
        print(f'ZIP: {zpath}')
        csv_files = extract_csvs_from_zip(zpath)
        ordered = sorted(
            csv_files.keys(),
            key=lambda k: PRIORITY_FILES.index(k) if k in PRIORITY_FILES else 999
        )
        for basename in ordered:
            list_name = Path(basename).stem
            spots = parse_csv(csv_files[basename], list_name)
            added = [s for s in spots if s['name'] not in seen_names]
            for s in added:
                seen_names.add(s['name'])
            new_spots.extend(added)
            print(f'  {basename}: {len(spots)} hits, {len(added)} new')

    all_spots = existing + new_spots
    OUT_FILE.write_text(json.dumps(all_spots, ensure_ascii=False, indent=2))
    print(f'\n{len(new_spots)} new spots added → total {len(all_spots)}')
    print(f'Output: {OUT_FILE}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/extract_okinawa.py <takeout.zip> [...]')
        sys.exit(1)
    main(sys.argv[1:])
