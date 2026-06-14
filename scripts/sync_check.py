#!/usr/bin/env python3
"""
trip-planner link sync checker.
Verifies: Trips → 九州 → [city] topnav on all city pages,
kyushu.html links to all cities, index.html links to kyushu.html.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CITIES = {
    "kurume": "久留米",
    "aya": "綾町",
    "hita": "日田",
    "itoshima": "糸島・二丈",
    "kirishima": "霧島",
    "minamiaso": "南阿蘇",
    "ukiha": "うきは",
    "yame": "八女",
}

errors = []

# 1. City pages: must have Trips → 九州 → [city] topnav
for slug, name in CITIES.items():
    path = ROOT / f"{slug}.html"
    if not path.exists():
        errors.append(f"MISSING: {slug}.html")
        continue
    html = path.read_text()
    if 'href="kyushu.html"' not in html:
        errors.append(f"{slug}.html: missing kyushu.html link in topnav")
    if f'href="{slug}.html" aria-current="page"' not in html:
        errors.append(f"{slug}.html: missing aria-current on self-link")

# 2. kyushu.html: must link to all cities
kyushu = (ROOT / "kyushu.html").read_text()
for slug in CITIES:
    if f'href="{slug}.html"' not in kyushu:
        errors.append(f"kyushu.html: missing link to {slug}.html")

# 3. index.html: must link to kyushu.html
index = (ROOT / "index.html").read_text()
if 'href="kyushu.html"' not in index and '"kyushu.html"' not in index:
    errors.append("index.html: missing link to kyushu.html")

# 4. Check kyushu.html has its own correct topnav
if 'href="kyushu.html" aria-current="page"' not in kyushu:
    errors.append("kyushu.html: missing aria-current on self-link")

if errors:
    print("SYNC ERRORS:")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("OK — all links are in sync")
    for slug in CITIES:
        print(f"  ✓ {slug}.html")
    print("  ✓ kyushu.html")
    print("  ✓ index.html")
