#!/usr/bin/env python3
"""汎用カテゴリ分類スクリプト。スポットJSONのcategoryフィールドを名前+descのキーワードマッチで再分類する。
Usage: python3 scripts/classify_categories.py [json_path] [--target food]
"""
import json, re, sys
from collections import Counter
from pathlib import Path

# 優先度順（先にマッチしたものが勝つ）
RULES = [
    ('steak',        re.compile(r'ステーキ|STEAK|steak', re.I)),
    ('yakiniku',     re.compile(r'焼肉|石垣牛|アグー(?:とんかつ|豚)?|七輪焼|豚七輪')),
    ('izakaya',      re.compile(r'居酒屋|酒場|酒ト|ひらら.*バル')),
    ('chinese',      re.compile(r'中華|飯店|萬珍|燕郷')),
    ('seafood',      re.compile(r'寿司|すし|寿し|鮮魚|今いゆ|漁港.*食堂|魚(?:まる|屋)')),
    ('western',      re.compile(r'トラットリア|ビストロ|BISTRO|BURGER|バーガー|洋食|Cucina|Italiana', re.I)),
    ('asian',        re.compile(r'スリランカ|ネパール|タイ料理|ベトナム|パッタイ|ガパオ|バインミー|韓国料理|韓食堂')),
    ('washoku',      re.compile(r'天ぷら|とんかつ|カツ丼|大戸屋|鳥と卵|とりたまご|素麺')),
    ('bakery',       re.compile(r'パン(?!フ)|ベーカリー|製パン|BAKERY', re.I)),
    ('okinawa_food', re.compile(r'食堂|沖縄料理|沖縄そば|OKINAWA SOBA|そば(?!.*屋外)|島(?:料理|豚|おでん)|てびち|琉球|チャンプル|番所亭|百年古家|台所', re.I)),
]


def classify(name: str, desc: str, current: str, target: str = 'food') -> str:
    if current != target:
        return current
    text = name + ' ' + (desc or '')
    for cat, pat in RULES:
        if pat.search(text):
            return cat
    return current


def main():
    json_path = 'okinawa_enriched.json'
    target = 'food'
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == '--target' and i < len(sys.argv) - 1:
            target = sys.argv[i + 1]
        elif not arg.startswith('--'):
            json_path = arg

    data = json.loads(Path(json_path).read_text())
    changed = 0
    for s in data:
        new_cat = classify(s.get('name', ''), s.get('desc', ''), s.get('category', ''), target)
        if new_cat != s.get('category'):
            print(f'{new_cat}: {s["name"]}')
            s['category'] = new_cat
            changed += 1

    Path(json_path).write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f'---\n変更: {changed}件')
    cats = Counter(s.get('category', '') for s in data)
    for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f'  {cat}: {n}件')


if __name__ == '__main__':
    main()
