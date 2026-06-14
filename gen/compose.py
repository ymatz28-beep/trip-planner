"""
spots.json + 都市情報 → Claude API → plan.json
plan.json schema:
{
  "slug": "ukiha",
  "title": "うきは市 — 白壁と果物の一日",
  "subtitle": "日帰り · 薬院から車40分",
  "date": "2026-07-12",
  "accent": "#c9590e",
  "accent2": "#fdf0e8",
  "hero_gradient": "linear-gradient(150deg,#8b4513 0%,#c9590e 42%,#d97a3f 100%)",
  "lede": "...",
  "facts": [{k, v, u, s}, ...],
  "timeline": [{time, emoji, title, tag, meta, desc, why, map_q, color_var}, ...],
  "options_groups": [{title, picks: [{name, label, desc, map_url, rec}]}, ...],
  "budget_rows": [{label, note, amount}, ...],
  "budget_total": 5200,
  "prep_items": ["...", ...],
  "weather_note": "..."
}
"""
import json
import os
from pathlib import Path

import anthropic
from pathlib import Path as _Path

# .env から ANTHROPIC_API_KEY を読む（未設定時のフォールバック）
def _load_env():
    for p in [_Path(".env"), _Path.home() / ".anthropic_api_key", _Path.home() / ".env"]:
        if p.exists():
            for line in p.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    import os
                    os.environ.setdefault("ANTHROPIC_API_KEY", line.split("=", 1)[1].strip())
                    return
_load_env()

MODEL = "claude-sonnet-4-6"
CACHE_DIR = Path(__file__).parent.parent / ".cache" / "spots"


SYSTEM_PROMPT = """あなたは旅行プランナーです。
提供された都市情報とスポットデータをもとに、日帰り or 1泊の旅行プランを JSON で生成してください。
出力は必ず有効な JSON のみにしてください（マークダウンコードブロック不要）。"""


def compose_plan(city: dict, spots: list[dict], date: str, answers: dict) -> dict:
    """
    Claude API を呼んで plan.json を生成する
    """
    client = anthropic.Anthropic()

    overnight = answers.get("q1_value") == "overnight"
    pace = answers.get("q5_density", "medium")
    companion = answers.get("q3_value", "friends")
    must_kws = answers.get("q4_must_keywords", [])

    spots_summary = json.dumps(spots[:20], ensure_ascii=False, indent=2) if spots else "[]"

    user_prompt = f"""以下の情報から旅行プランの JSON を生成してください。

# 都市情報
- 都市名: {city['name']} ({city['prefecture']})
- 特徴: {city['vibe']}
- タグ: {', '.join(city.get('tags', []))}
- 旬: {city.get('season_note', '')}
- アクセス: 薬院から車{city.get('drive_min', '?')}分

# 旅行条件
- 日程: {date} / {"1泊" if overnight else "日帰り"}
- 旅のペース: {"詰め込む" if pace == "high" else "のんびり"}
- 同行者: {companion}
- 外せない要素: {', '.join(must_kws) if must_kws else 'なし'}

# 収集したスポット候補
{spots_summary}

# 出力 JSON スキーマ（全フィールド必須）
{{
  "slug": "{city['slug']}",
  "title": "都市名 — キャッチコピー（例: 糸島 — 海と朝焼けパンの一日）",
  "subtitle": "Day Trip · 薬院から車X分",
  "date": "{date}",
  "accent": "#HEX（その都市のイメージカラー）",
  "accent2": "#HEX（accent の薄い背景色・accent に白を混ぜた感じ）",
  "hero_gradient": "radial-gradient(120% 90% at 85% 0%, rgba(255,210,150,.22), transparent 55%), linear-gradient(150deg,#HEX1 0%,#HEX2 42%,#HEX3 100%)",
  "lede": "プランの説明文（2-3文・体験が伝わるように）",
  "hero_pills": ["📅 {date}", "🚗 カーシェア・薬院発", "☀️ 天気コメント"],
  "facts": [
    {{"k": "距離", "v": "{city.get('drive_min', '?')}", "u": "分", "s": "薬院から高速", "jp": false}},
    {{"k": "行程", "v": "日帰り", "u": "", "s": "約8時間", "jp": true}},
    {{"k": "予算", "v": "5,200", "u": "円〜", "s": "1人あたりの目安", "jp": false}},
    {{"k": "ベストシーズン", "v": "通年", "u": "", "s": "季節コメント", "jp": true}}
  ],
  "keynote": {{
    "emoji": "🌊",
    "title": "このプランの肝（1行）",
    "desc": "補足説明（2-3文）"
  }},
  "timeline": [
    {{
      "time": "8:30",
      "emoji": "🚗",
      "title": "スポット名",
      "tag": "カテゴリ・人数など",
      "meta": "住所・料金・営業時間など",
      "desc": "説明文（<b>タグで強調可</b>）",
      "why": "なぜここ？（空文字でも可）",
      "map_q": "Google Maps 検索クエリ（日本語可）",
      "color_var": "--food",
      "leg": "🚗 次のスポットへ XX分（最後のストップは空文字）"
    }}
  ],
  "options_groups": [
    {{
      "title": "☕ カフェ・コーヒー",
      "picks": [
        {{
          "name": "店名",
          "label": "今回 or 候補・エリア",
          "desc": "詳細（営業時間・定休日・おすすめ）",
          "map_url": "https://maps.google.com/?q=店名+地域名",
          "rec": true
        }}
      ]
    }}
  ],
  "budget_rows": [
    {{"label": "カーシェア", "note": "12時間パック", "amount": 1830}},
    {{"label": "高速代", "note": "往復", "amount": 600}},
    {{"label": "ランチ", "note": "1人", "amount": 2000}}
  ],
  "budget_total": 5200,
  "budget_note": "内訳の補足（省略可・空文字可）",
  "prep_items": [
    "!要予約: ○○を電話予約（TEL XXXX-XXXX）",
    "!カーシェア9:00から予約済みを確認",
    "折りたたみ傘（梅雨・夏の夕立対策）",
    "現金少々（駐車場・露店用）"
  ],
  "weather_note": "天候への一言コメント（例: 6月は梅雨。屋内比率を上げると安心）"
}}

ルール:
- タイムラインは{4 if pace == "low" else 6}〜{6 if pace == "low" else 8}スポット
- color_var は食事=--food、文化・観光=--culture、温泉/サウナ=--onsen、移動=--move
- prep_items は「!」で始まると「必須事項」扱い（予約・事前確認）
- facts の jp=true は日本語フォント（数字でない値に使う）
- JSON のみ出力（マークダウン不要）"""

    msg = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw = msg.content[0].text.strip()

    # マークダウンブロックを除去
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


if __name__ == "__main__":
    import sys
    import yaml

    data_path = Path(__file__).parent.parent / "data" / "cities.yaml"
    with open(data_path) as f:
        cities = yaml.safe_load(f)["cities"]

    slug = sys.argv[1] if len(sys.argv) > 1 else "itoshima"
    city = next((c for c in cities if c["slug"] == slug), None)
    if not city:
        print(f"都市 '{slug}' が見つかりません")
        sys.exit(1)

    cache_path = CACHE_DIR / f"{slug}.json"
    spots = json.loads(cache_path.read_text()) if cache_path.exists() else []

    date = sys.argv[2] if len(sys.argv) > 2 else "2026-07-12"
    answers = {"q1_value": "day_trip", "q5_density": "medium", "q3_value": "friends"}

    print(f"[compose] {city['name']} のプラン生成中...")
    plan = compose_plan(city, spots, date, answers)

    out = Path(__file__).parent.parent / ".cache" / f"{slug}_plan.json"
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    print(f"[compose] → {out}")
