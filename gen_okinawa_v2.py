#!/usr/bin/env python3
"""Okinawa trip-planner HTML generator v2 — Playfair Display design, CID Maps, Exa enriched data."""
import json, re, sys, os
from pathlib import Path
from collections import defaultdict

_DESC_JUNK = re.compile(
    r'官方消息|已登錄|店家會員'         # 繁体字中国語UIテキスト
    r'|Switch to Tabelog'              # 英語切替UI
    r'|\| ---'                         # Markdown表形式
    r'| \| [A-Za-z]'                   # 英語サイト名（例: | TRAVEL for YOU）
    r'|ログイン|無料会員登録'            # 認証UI
    r'|口コミ\s*写真\s*地図'            # 食べログナビ
    r'|英語環境|HAMONI'                # HAMONI系UIゴミ
    r'|English site is here'           # 英語サイト誘導
    r'|tiktok\.com'                    # TikTok URL
    r'|エキテン\s*by|エキテン\s*GMO'   # エキテンUI
    r'|Retty（レッティ）'              # Rettyページタイトル
    r'|なび沖】|全国なびから'           # なび沖UI
    r'|Yahoo! JAPAN'                   # Yahoo UIテキスト
    r'|TEL:\d{3}'                      # 電話番号混入UI
)

def _clean_desc(desc: str) -> str:
    if not desc:
        return ''
    if _DESC_JUNK.search(desc):
        return ''
    # ｜が2つ以上→ページタイトルかMarkdown表
    if desc.count('｜') >= 2:
        return ''
    # 先頭にページタイトル形式（「名称｜サイト」）→ ｜以降を取る
    if '｜' in desc[:50]:
        after = desc.split('｜', 1)[1].strip()
        # ｜の後も短くなりすぎたら捨てる
        return after if len(after) > 20 else ''
    return desc

SPOTS_FILE = Path(__file__).parent / "okinawa_spots_tmp.json"
ENRICHED_FILE = Path(__file__).parent / "okinawa_enriched.json"
OUT_DIR = Path(__file__).parent

# ── Region config ──────────────────────────────────────────────────
REGIONS = {
    "naha":     {"name": "那覇",      "emoji": "🏯", "page": "naha.html",     "c1": "#3a1055", "c2": "#7745c0", "c3": "#f5eeff", "ck": "#3a1055", "hero_sub": "国際通り · 松山 · 牧志"},
    "hontou":   {"name": "本島中北部","emoji": "🌴", "page": "hontou.html",   "c1": "#0a3020", "c2": "#1a8050", "c3": "#eeffef", "ck": "#0a3020", "hero_sub": "恩納 · 北谷 · 名護 · 読谷"},
    "miyako":   {"name": "宮古島",    "emoji": "🐠", "page": "miyako.html",   "c1": "#00327a", "c2": "#0091c2", "c3": "#e8f6ff", "ck": "#00327a", "hero_sub": "与那覇前浜 · 砂山ビーチ · 来間島"},
    "ishigaki": {"name": "石垣島",    "emoji": "🌺", "page": "ishigaki.html", "c1": "#6e1700", "c2": "#c44830", "c3": "#fff4f0", "ck": "#6e1700", "hero_sub": "川平湾 · 平久保崎 · 白保"},
    "ritou":    {"name": "その他離島","emoji": "⛵", "page": "ritou.html",    "c1": "#4a2a00", "c2": "#a06010", "c3": "#fffaee", "ck": "#4a2a00", "hero_sub": "久米島 · 竹富島 · 慶良間"},
}

REGION_MAP = {
    "宮古島": "miyako",
    "石垣島": "ishigaki",
    "那覇":   "naha",
    "本島":   "hontou",
    "離島":   "ritou",
}

CAT_LABEL = {
    "okinawa_food":  ("🥣", "沖縄料理"),
    "izakaya":       ("🍻", "居酒屋"),
    "steak":         ("🥩", "ステーキ"),
    "yakiniku":      ("🔥", "焼肉"),
    "seafood":       ("🐟", "海鮮・寿司"),
    "chinese":       ("🥢", "中華料理"),
    "western":       ("🍝", "洋食"),
    "asian":         ("🌏", "アジア料理"),
    "washoku":       ("🍱", "和食"),
    "bakery":        ("🍞", "パン屋"),
    "food":          ("🍽", "その他の食事"),
    "cafe_sweets":   ("☕", "カフェ・スイーツ"),
    "leisure":       ("🌊", "観光・スポット"),
    "activity":      ("🏄", "観光・体験"),
    "lodging":       ("🏨", "宿泊"),
    "stay":          ("🛏", "ホテル・宿"),
    "health":        ("🛁", "サウナ・スパ"),
    "nightlife":     ("🌙", "ナイトライフ"),
}

TIER_LABEL = {2: "★★ おすすめ", 3: "★ チェック"}
TIER_COLOR = {2: "#b04010", 3: "var(--text-muted)"}

# ── Load data ──────────────────────────────────────────────────────
def load_spots():
    base = json.loads(SPOTS_FILE.read_text())
    enriched_by_region = {}
    enriched_by_name = {}
    if ENRICHED_FILE.exists():
        for s in json.loads(ENRICHED_FILE.read_text()):
            if "region" in s:
                enriched_by_region[(s["name"], s["region"])] = s
            enriched_by_name[s["name"]] = s
    merged = []
    for s in base:
        key = (s["name"], s["region"])
        if key in enriched_by_region:
            merged.append({**s, **enriched_by_region[key]})
        elif s["name"] in enriched_by_name:
            merged.append({**s, **enriched_by_name[s["name"]]})
        else:
            merged.append(s)
    return merged

# ── Shared CSS ─────────────────────────────────────────────────────
def shared_css(c1, c2, c3, ck):
    return f"""
  :root{{
    --bg:#faf7f2; --surface:#fff; --surface2:#f5f0e8;
    --ink:#1a1510; --ink2:#4a4035; --ink3:#8a7a6a;
    --line:#e8dfd0; --line2:#f0e8da;
    --c1:{c1}; --c2:{c2}; --c3:{c3}; --ck:{ck};
    --r:12px; --r-sm:8px; --r-pill:999px;
    --shadow:0 1px 3px rgba(26,21,16,.05),0 8px 24px rgba(26,21,16,.08);
  }}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%;}}
  body{{
    font-family:'Noto Sans JP','Hiragino Kaku Gothic ProN','Yu Gothic',sans-serif;
    background:var(--bg);color:var(--ink);font-size:15px;line-height:1.75;
    -webkit-font-smoothing:antialiased;overflow-x:hidden;
  }}
  a{{color:inherit;text-decoration:none;}}
  h1,h2,h3,.display{{font-family:'Playfair Display',Georgia,serif;}}

  /* Topbar */
  .topbar{{position:sticky;top:0;z-index:60;background:rgba(250,247,242,.9);
    backdrop-filter:saturate(160%) blur(12px);border-bottom:1px solid var(--line);}}
  .topbar .wrap{{display:flex;align-items:center;justify-content:space-between;height:50px;}}
  .brand{{font-size:11px;font-weight:700;letter-spacing:.18em;color:var(--c2);text-transform:uppercase;}}
  .topnav{{display:flex;gap:2px;}}
  .topnav a{{font-size:13px;font-weight:600;color:var(--ink3);
    padding:8px 11px;border-radius:9px;min-height:38px;display:flex;align-items:center;}}
  .topnav a.back{{font-weight:700;color:var(--c1);}}
  .topnav a.back::before{{content:"‹ ";}}
  .topnav a[aria-current="page"]{{color:var(--c1);background:var(--c3);}}

  /* Hero */
  .hero{{position:relative;overflow:hidden;color:#fff;
    background:radial-gradient(120% 90% at 85% 0%,rgba(255,220,180,.18),transparent 55%),
    linear-gradient(150deg,var(--c1) 0%,var(--c2) 55%,{c2}bb 100%);}}
  .hero .wrap{{padding:32px 18px 68px;position:relative;z-index:2;}}
  .eyebrow{{display:inline-flex;align-items:center;gap:7px;
    font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
    color:rgba(255,255,255,.62);margin-bottom:14px;}}
  .eyebrow::before{{content:"";width:18px;height:1.5px;background:rgba(255,255,255,.5);display:inline-block;}}
  .hero h1{{font-size:clamp(28px,7.5vw,40px);font-weight:700;line-height:1.2;margin-bottom:8px;}}
  .hero h1 small{{display:block;font-family:'Noto Sans JP',sans-serif;
    font-size:clamp(13px,3.5vw,16px);font-weight:500;color:rgba(255,255,255,.72);margin-top:6px;}}
  .hero .lede{{font-size:14px;color:rgba(255,255,255,.78);line-height:1.72;max-width:42ch;}}
  .hero-meta{{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px;}}
  .hpill{{display:inline-flex;align-items:center;gap:5px;
    background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
    padding:5px 11px;border-radius:var(--r-pill);font-size:12px;font-weight:600;color:#fff;}}

  .wrap{{max-width:720px;margin:0 auto;padding:0 18px;}}

  /* Stats bar */
  .stats{{margin-top:-44px;position:relative;z-index:5;
    background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
    box-shadow:var(--shadow);display:grid;grid-template-columns:repeat(2,1fr);}}
  @media(min-width:560px){{.stats{{grid-template-columns:repeat(4,1fr);}}}}
  .stat{{padding:15px;border-right:1px solid var(--line2);border-bottom:1px solid var(--line2);}}
  .stat:nth-child(2n){{border-right:0;}}.stat:nth-last-child(-n+2){{border-bottom:0;}}
  @media(min-width:560px){{
    .stat{{border-bottom:0;}}.stat:nth-child(2n){{border-right:1px solid var(--line2);}}.stat:last-child{{border-right:0;}}
  }}
  .stat .k{{font-size:10px;font-weight:700;letter-spacing:.05em;color:var(--ink3);text-transform:uppercase;margin-bottom:4px;}}
  .stat .v{{font-family:'Noto Sans JP','Hiragino Kaku Gothic ProN',sans-serif;font-size:clamp(22px,5.5vw,28px);
    font-weight:700;color:var(--c1);line-height:1;letter-spacing:-.02em;}}
  .stat .u{{font-size:13px;font-weight:600;color:var(--ink2);margin-left:1px;}}
  .stat .s{{font-size:11px;color:var(--ink3);margin-top:4px;}}

  /* Secnav */
  .secnav-wrap{{position:sticky;top:50px;z-index:55;background:rgba(250,247,242,.92);
    backdrop-filter:blur(10px);border-bottom:1px solid var(--line);}}
  .secnav{{display:flex;gap:6px;overflow-x:auto;padding:10px 18px;scrollbar-width:none;
    max-width:720px;margin:0 auto;}}
  .secnav::-webkit-scrollbar{{display:none;}}
  .secnav a{{flex:0 0 auto;font-size:12px;font-weight:600;color:var(--ink2);
    padding:6px 12px;border-radius:var(--r-pill);background:var(--surface);
    border:1px solid var(--line);min-height:34px;display:flex;align-items:center;
    white-space:nowrap;transition:.15s;}}
  .secnav a.active{{color:#fff;background:var(--c1);border-color:var(--c1);}}

  /* Category sections */
  section{{padding:28px 0 4px;scroll-margin-top:108px;}}
  .sec-head{{display:flex;align-items:baseline;gap:10px;margin-bottom:16px;
    padding-bottom:10px;border-bottom:2px solid var(--c1);}}
  .sec-head h2{{font-size:clamp(17px,4.5vw,20px);font-weight:700;color:var(--c1);}}
  .sec-count{{font-size:11px;font-weight:700;color:var(--ink3);background:var(--surface2);
    border:1px solid var(--line2);padding:2px 8px;border-radius:var(--r-pill);}}

  /* Spot list — editorial, not round cards */
  .spot-list{{display:flex;flex-direction:column;gap:0;}}
  .spot-item{{
    display:grid;grid-template-columns:1fr auto;
    gap:4px 12px;padding:14px 0;border-bottom:1px solid var(--line2);
  }}
  .spot-item:last-child{{border-bottom:0;}}
  .spot-name{{font-size:15px;font-weight:700;color:var(--ink);line-height:1.4;}}
  .spot-name a{{color:var(--c1);}}
  .spot-name a:hover{{text-decoration:underline;}}
  .spot-meta{{font-size:11.5px;color:var(--ink3);margin-top:3px;line-height:1.5;}}
  .spot-desc{{font-size:12.5px;color:var(--ink2);margin-top:4px;line-height:1.6;grid-column:1/-1;}}
  .spot-links{{display:flex;gap:6px;align-items:flex-start;flex-wrap:wrap;grid-column:2;grid-row:1/3;justify-content:flex-end;}}
  .slink{{
    display:inline-flex;align-items:center;gap:4px;
    font-size:11px;font-weight:600;padding:4px 9px;border-radius:6px;
    white-space:nowrap;transition:.12s;
  }}
  .slink-map{{background:var(--c3);color:var(--c1);border:1px solid var(--c2)33;}}
  .slink-map:hover{{background:var(--c2);color:#fff;}}
  .slink-tab{{background:#f5f0e8;color:#8a5010;border:1px solid #d4a86033;}}
  .slink-tab:hover{{background:#e09828;color:#fff;}}
  .slink-web{{background:#f0f0f0;color:#404040;border:1px solid #ccc;}}
  .slink-web:hover{{background:#444;color:#fff;}}
  .tier-badge{{
    display:inline-block;font-size:10px;font-weight:700;
    padding:2px 6px;border-radius:4px;margin-left:6px;vertical-align:middle;
  }}
  .tier2{{background:#fff4f0;color:#b04010;border:1px solid #e8843a44;}}
  .tier3{{background:var(--surface2);color:var(--ink3);border:1px solid var(--line);}}

  /* Hub-specific */
  .rgrid{{display:grid;gap:14px;margin-top:28px;}}
  @media(min-width:480px){{.rgrid{{grid-template-columns:1fr 1fr;}}}}
  .rcard{{
    background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
    box-shadow:var(--shadow);overflow:hidden;display:block;transition:.18s;
  }}
  .rcard:hover{{box-shadow:0 4px 20px rgba(26,21,16,.14);transform:translateY(-2px);}}
  .rcard-top{{height:6px;}}
  .rcard-body{{padding:18px;}}
  .rcard-flag{{font-size:24px;margin-bottom:8px;display:block;}}
  .rcard-name{{font-size:17px;font-weight:700;color:var(--ink);margin-bottom:4px;}}
  .rcard-sub{{font-size:12px;color:var(--ink3);margin-bottom:10px;}}
  .rcard-tags{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:12px;}}
  .rtag{{font-size:11px;font-weight:600;color:var(--ink2);background:var(--surface2);
    border:1px solid var(--line);padding:3px 8px;border-radius:var(--r-pill);}}
  .rcard-foot{{display:flex;align-items:center;justify-content:space-between;
    font-size:12.5px;font-weight:600;color:var(--ink3);}}
  .rcard-count{{font-size:11px;}}
  .rcard-arrow{{color:var(--c2);font-size:16px;}}

  /* Footer / ToTop */
  footer{{margin-top:36px;border-top:1px solid var(--line);padding:24px 0 44px;color:var(--ink3);}}
  footer .ft-1{{font-size:12px;font-weight:700;letter-spacing:.1em;color:var(--c2);text-transform:uppercase;}}
  footer .ft-2{{font-size:11.5px;margin-top:4px;}}
  .totop{{position:fixed;right:16px;bottom:16px;z-index:70;width:46px;height:46px;
    border-radius:50%;background:var(--c1);color:#fff;border:none;cursor:pointer;
    display:flex;align-items:center;justify-content:center;font-size:18px;
    box-shadow:0 8px 22px {c1}55;opacity:0;pointer-events:none;
    transform:translateY(8px);transition:.25s;}}
  .totop.show{{opacity:1;pointer-events:auto;transform:none;}}
  @media print{{.topbar,.totop{{display:none!important;}}body{{background:#fff;}}}}
  .search-row{{display:flex;align-items:center;gap:8px;padding:8px 18px;max-width:720px;margin:0 auto;border-bottom:1px solid var(--line2);}}
  .search-box{{flex:1;display:flex;align-items:center;gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-pill);padding:5px 12px;}}
  .search-box input{{flex:1;border:none;outline:none;background:transparent;font-size:13px;color:var(--ink);font-family:'Noto Sans JP','Hiragino Kaku Gothic ProN',sans-serif;}}
  .search-box input::placeholder{{color:var(--ink3);font-size:12px;}}
  .tier-filter-btn{{flex:0 0 auto;font-size:11px;font-weight:700;padding:5px 12px;border-radius:var(--r-pill);border:1px solid var(--line2);background:var(--surface2);color:var(--ink3);cursor:pointer;white-space:nowrap;transition:.15s;min-height:34px;}}
  .tier-filter-btn.on{{background:#fff4f0;color:#b04010;border-color:#e8843a44;}}
  .no-results{{padding:32px 18px;text-align:center;color:var(--ink3);font-size:13px;display:none;}}
"""

FONT_LINK = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">'

TOTOP_JS = """
<script>
const btn=document.querySelector('.totop');
window.addEventListener('scroll',()=>{btn.classList.toggle('show',scrollY>320);});
btn.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));
// secnav active tracking
const secs=document.querySelectorAll('section[id]');
const navlinks=document.querySelectorAll('.secnav a');
const obs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){
    navlinks.forEach(l=>l.classList.toggle('active',l.getAttribute('href')==='#'+e.target.id));
  }});
},{rootMargin:'-40% 0px -55% 0px'});
secs.forEach(s=>obs.observe(s));
(function(){
  const inp=document.getElementById('search-inp');
  const btn=document.getElementById('tier2-toggle');
  if(!inp&&!btn) return;
  let tier2only=false;
  function applyFilter(){
    const q=inp?inp.value.trim().toLowerCase():'';
    let any=false;
    document.querySelectorAll('.spot-item').forEach(el=>{
      const ok=(!q||(el.dataset.name||'').toLowerCase().includes(q))&&(!tier2only||+el.dataset.tier===2);
      el.style.display=ok?'':'none';
      if(ok) any=true;
    });
    document.querySelectorAll('section[id]').forEach(sec=>{
      const vis=[...sec.querySelectorAll('.spot-item')].some(e=>e.style.display!=='none');
      sec.style.display=vis?'':'none';
    });
    const nr=document.getElementById('no-results');
    if(nr) nr.style.display=any?'none':'block';
  }
  if(inp) inp.addEventListener('input',applyFilter);
  if(btn) btn.addEventListener('click',()=>{
    tier2only=!tier2only;
    btn.classList.toggle('on',tier2only);
    btn.textContent=tier2only?'★ 全件表示':'★ おすすめのみ';
    applyFilter();
  });
})();
</script>
"""

def render_spot(s):
    name = s["name"]
    maps_url = s.get("maps_url", "")
    tabelog_url = s.get("tabelog_url", "")
    official_url = s.get("official_url", "")
    source_url = s.get("source_url", "")
    desc = _clean_desc(s.get("description", "") or s.get("desc", ""))
    price = s.get("price_range", "")
    addr = s.get("addr", "")
    tier = s.get("tier", 3)
    score_google = s.get("score_google", "")
    score_tabelog = s.get("score_tabelog", "")

    tier_badge = '<span class="tier-badge tier2">おすすめ</span>' if tier == 2 else ''

    # Name — link to Maps if available
    if maps_url:
        name_html = f'<a href="{maps_url}" target="_blank" rel="noopener">{name}</a>{tier_badge}'
    else:
        name_html = f'{name}{tier_badge}'

    # Meta line
    meta_parts = []
    if price:
        meta_parts.append(price)
    if score_google:
        meta_parts.append(f'Google ⭐{score_google}')
    if score_tabelog:
        meta_parts.append(f'食べログ {score_tabelog}')
    meta_html = " · ".join(meta_parts) if meta_parts else ""

    # Link buttons
    links = []
    if maps_url:
        links.append(f'<a class="slink slink-map" href="{maps_url}" target="_blank" rel="noopener">📍 地図</a>')
    if tabelog_url and "tabelog.com" in tabelog_url:
        links.append(f'<a class="slink slink-tab" href="{tabelog_url}" target="_blank" rel="noopener">食べログ</a>')
    if official_url and official_url not in (tabelog_url, maps_url, ""):
        if "tabelog" not in official_url and "google" not in official_url:
            links.append(f'<a class="slink slink-web" href="{official_url}" target="_blank" rel="noopener">公式</a>')
    if source_url and "tabelog.com" in source_url and not tabelog_url:
        links.append(f'<a class="slink slink-tab" href="{source_url}" target="_blank" rel="noopener">食べログ</a>')
    elif source_url and source_url not in (maps_url, tabelog_url, official_url, ""):
        if "google" not in source_url and "tabelog" not in source_url:
            links.append(f'<a class="slink slink-web" href="{source_url}" target="_blank" rel="noopener">情報元</a>')
    links_html = "".join(links)

    desc_html = f'<p class="spot-desc">{desc}</p>' if desc else ""

    name_esc = name.replace('"', '&quot;')
    return f"""<div class="spot-item" data-tier="{tier}" data-name="{name_esc}">
  <div>
    <div class="spot-name">{name_html}</div>
    {f'<div class="spot-meta">{meta_html}</div>' if meta_html else ''}
    {desc_html}
  </div>
  <div class="spot-links">{links_html}</div>
</div>"""

# ── Generate regional page ─────────────────────────────────────────
def gen_region_page(region_key, spots, hub_page="okinawa-general.html"):
    rc = REGIONS[region_key]
    name = rc["name"]
    emoji = rc["emoji"]
    c1, c2, c3, ck = rc["c1"], rc["c2"], rc["c3"], rc["ck"]
    hero_sub = rc["hero_sub"]

    # Group by category
    by_cat = defaultdict(list)
    for s in spots:
        by_cat[s["category"]].append(s)
    # Sort: tier2 first within each cat
    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: (x.get("tier", 3), x["name"]))

    cat_order = ["food", "cafe_sweets", "leisure", "activity", "lodging", "stay", "health", "nightlife"]
    present_cats = [c for c in cat_order if c in by_cat]

    # Secnav
    secnav_items = "".join(
        f'<a href="#{c}">{CAT_LABEL[c][0]} {CAT_LABEL[c][1]}</a>'
        for c in present_cats
    )

    # Stats
    food_n = len(by_cat.get("food", [])) + len(by_cat.get("cafe_sweets", []))
    leisure_n = len(by_cat.get("leisure", [])) + len(by_cat.get("activity", []))
    lodging_n = len(by_cat.get("lodging", [])) + len(by_cat.get("stay", []))
    total_n = len(spots)
    tier2_n = sum(1 for s in spots if s.get("tier") == 2)

    stats_html = f"""<div class="stats wrap">
  <div class="stat"><div class="k">グルメ</div><div class="v">{food_n}<span class="u">件</span></div><div class="s">食事・カフェ</div></div>
  <div class="stat"><div class="k">観光</div><div class="v">{leisure_n}<span class="u">件</span></div><div class="s">スポット・体験</div></div>
  <div class="stat"><div class="k">宿泊</div><div class="v">{lodging_n}<span class="u">件</span></div><div class="s">ホテル・宿</div></div>
  <div class="stat"><div class="k">おすすめ</div><div class="v">{tier2_n}<span class="u">件</span></div><div class="s">厳選スポット</div></div>
</div>"""

    # Section bodies
    sections_html = ""
    for cat in present_cats:
        cat_spots = by_cat[cat]
        cat_icon, cat_name = CAT_LABEL[cat]
        spots_html = "\n".join(render_spot(s) for s in cat_spots)
        sections_html += f"""
<section id="{cat}">
  <div class="sec-head">
    <h2>{cat_icon} {cat_name}</h2>
    <span class="sec-count">{len(cat_spots)}件</span>
  </div>
  <div class="spot-list">{spots_html}</div>
</section>"""

    title = f"{emoji} {name} ガイド | iUMA Travel"
    theme = c1

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="theme-color" content="{theme}">
{FONT_LINK}
<style>{shared_css(c1, c2, c3, ck)}</style>
</head>
<body>

<header class="topbar">
  <div class="wrap">
    <span class="brand">iUMA Travel</span>
    <nav class="topnav">
      <a href="{hub_page}" class="back">沖縄</a>
      <a href="#" aria-current="page">{name}</a>
    </nav>
  </div>
</header>

<div class="hero">
  <div class="wrap">
    <div class="eyebrow">Okinawa · {name}</div>
    <h1>{emoji} {name}<small>{hero_sub}</small></h1>
    <p class="lede">Mapplyに保存した{total_n}件のスポットを収録。食事・カフェ・観光・宿泊をカテゴリで確認できます。</p>
    <div class="hero-meta">
      <span class="hpill">📍 {total_n}スポット</span>
      <span class="hpill">★★ おすすめ {tier2_n}件</span>
    </div>
  </div>
</div>

{stats_html}

<div class="secnav-wrap">
  <div class="search-row">
    <div class="search-box"><span style="font-size:14px;color:var(--ink3)">🔍</span><input id="search-inp" type="search" placeholder="{name}内を検索..." autocomplete="off"></div>
    <button class="tier-filter-btn" id="tier2-toggle">★ おすすめのみ</button>
  </div>
  <div class="secnav">{secnav_items}</div>
</div>

<main class="wrap">
<p id="no-results" class="no-results">検索結果がありません</p>
{sections_html}
</main>

<footer>
  <div class="wrap">
    <div class="ft-1">iUMA Travel · {name}</div>
    <div class="ft-2">Mapplyデータ + Exaリサーチ · {total_n}スポット · <a href="travel-master.html" style="color:{c1};opacity:.08;text-decoration:none;user-select:none;">Travel</a> · <a href="index.html" style="color:{c1};opacity:.08;text-decoration:none;user-select:none;">·</a></div>
  </div>
</footer>

<button class="totop" aria-label="トップへ戻る">↑</button>
{TOTOP_JS}
</body>
</html>"""

# ── Generate hub page ──────────────────────────────────────────────
def gen_hub_page(all_spots):
    total = len(all_spots)
    by_region = defaultdict(list)
    for s in all_spots:
        rk = REGION_MAP.get(s["region"])
        if rk:
            by_region[rk].append(s)

    c1, c2, c3, ck = "#023e5e", "#0a7abf", "#e8f6ff", "#023e5e"

    cards_html = ""
    for rk, rc in REGIONS.items():
        spots = by_region[rk]
        n = len(spots)
        t2 = sum(1 for s in spots if s.get("tier") == 2)
        food_n = sum(1 for s in spots if s["category"] in ("food", "cafe_sweets"))
        leisure_n = sum(1 for s in spots if s["category"] == "leisure")
        cards_html += f"""
<a class="rcard" href="{rc['page']}">
  <div class="rcard-top" style="background:{rc['c2']};"></div>
  <div class="rcard-body">
    <span class="rcard-flag">{rc['emoji']}</span>
    <div class="rcard-name">{rc['name']}</div>
    <div class="rcard-sub">{rc['hero_sub']}</div>
    <div class="rcard-tags">
      <span class="rtag">🍽 {food_n}件</span>
      <span class="rtag">🌊 {leisure_n}件</span>
      <span class="rtag">★★ {t2}件</span>
    </div>
    <div class="rcard-foot">
      <span class="rcard-count">全{n}スポット →</span>
      <span class="rcard-arrow">→</span>
    </div>
  </div>
</a>"""

    hub_css = shared_css(c1, c2, c3, ck) + f"""
  .hub-hero{{
    background:
      radial-gradient(120% 90% at 85% 0%,rgba(10,180,220,.2),transparent 55%),
      radial-gradient(80% 70% at 10% 80%,rgba(200,80,50,.15),transparent 50%),
      linear-gradient(150deg,{c1} 0%,#0a5a8a 55%,{c2}bb 100%);
  }}
  .hub-intro{{margin-top:28px;font-size:14.5px;color:var(--ink2);line-height:1.78;max-width:52ch;}}
"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>沖縄 エリアガイド | iUMA Travel</title>
<meta name="theme-color" content="{c1}">
{FONT_LINK}
<style>{hub_css}</style>
</head>
<body>

<header class="topbar">
  <div class="wrap">
    <span class="brand">iUMA Travel</span>
    <nav class="topnav">
      <a href="#" aria-current="page">沖縄 エリアガイド</a>
    </nav>
  </div>
</header>

<div class="hero hub-hero">
  <div class="wrap">
    <div class="eyebrow">Japan · Okinawa</div>
    <h1>🌺 沖縄 エリアガイド<small>宮古島 · 石垣島 · 那覇 · 本島 · 離島</small></h1>
    <p class="lede">Mapplyに保存した{total}件のスポットを5エリアで収録。エリアを選んでグルメ・観光・宿泊を確認。</p>
    <div class="hero-meta">
      <span class="hpill">📍 {total}スポット</span>
      <span class="hpill">5エリア</span>
      <span class="hpill">★★ おすすめ厳選あり</span>
    </div>
  </div>
</div>

<div class="wrap" style="margin-top:-44px;position:relative;z-index:5;">
  <div style="background:#fff;border:1px solid #e8dfd0;border-radius:12px;box-shadow:0 1px 3px rgba(26,21,16,.05),0 8px 24px rgba(26,21,16,.08);padding:16px 20px;">
    <div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#8a7a6a;text-transform:uppercase;margin-bottom:4px;">エリア別スポット数</div>
    <div style="font-size:14px;color:#4a4035;">
      {"　".join(f"{rc['emoji']} {rc['name']} {len(by_region[rk])}件" for rk, rc in REGIONS.items())}
    </div>
  </div>
</div>

<main class="wrap">
  <p class="hub-intro">沖縄の離島・本島に分散した厳選スポットをエリア別に整理。食事・カフェ・観光・宿泊をワンタップで地図確認できます。</p>
  <div class="rgrid">
    {cards_html}
  </div>
</main>

<footer>
  <div class="wrap">
    <div class="ft-1">iUMA Travel · 沖縄</div>
    <div class="ft-2">Mapplyデータ + Exaリサーチ · 全{total}スポット · <a href="travel-master.html" style="color:#023e5e;opacity:.08;text-decoration:none;user-select:none;">Travel</a> · <a href="kyushu.html" style="color:#023e5e;opacity:.08;text-decoration:none;user-select:none;">·</a> · <a href="index.html" style="color:#023e5e;opacity:.08;text-decoration:none;user-select:none;">·</a></div>
  </div>
</footer>

<button class="totop" aria-label="トップへ戻る">↑</button>
<script>
const btn=document.querySelector('.totop');
window.addEventListener('scroll',()=>{{btn.classList.toggle('show',scrollY>320);}});
btn.addEventListener('click',()=>window.scrollTo({{top:0,behavior:'smooth'}}));
</script>
</body>
</html>"""

# ── Main ───────────────────────────────────────────────────────────
def main():
    spots = load_spots()
    by_region = defaultdict(list)
    for s in spots:
        rk = REGION_MAP.get(s["region"])
        if rk:
            by_region[rk].append(s)

    # Generate regional pages
    for rk, rc in REGIONS.items():
        html = gen_region_page(rk, by_region[rk])
        out = OUT_DIR / rc["page"]
        out.write_text(html, encoding="utf-8")
        print(f"✓ {rc['page']} ({len(by_region[rk])}件)")

    # Generate hub
    html = gen_hub_page(spots)
    out = OUT_DIR / "okinawa-general.html"
    out.write_text(html, encoding="utf-8")
    print(f"✓ okinawa-general.html ({len(spots)}件)")

    print(f"\n完了: 6ページ生成 — {OUT_DIR}")

if __name__ == "__main__":
    main()
