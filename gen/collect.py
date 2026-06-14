"""
都市名 → Exa 検索 → 本文取得 → Claude Haiku でスポット抽出 → .cache/spots/{slug}.json

横展開スクレイピングスタック（全PJ共通・自動フォールバック）:
  1. Exa search + 内蔵コンテンツ取得
  2. 薄い(< 300文字)URL → Scrapling Fetcher（CSS、高速）
  3. それでも弾かれたら → StealthyFetcher（Playwright stealth）
  4. 最終手段 → requests + ブラウザヘッダ
"""
import json
import os
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / ".cache" / "spots"

SEARCH_QUERIES = [
    "{city} カフェ おすすめ 2024 2025",
    "{city} ランチ グルメ おすすめ",
    "{city} パン屋 スイーツ",
    "{city} 観光スポット 穴場",
    "{city} 温泉 サウナ",
]

HAIKU_MODEL = "claude-haiku-4-5-20251001"


def _load_keys() -> dict:
    """複数プロジェクトの .env から API キーを収集する"""
    keys = {}
    search_paths = [
        Path(__file__).parent.parent / ".env",
        Path.home() / "Documents/Projects/x-bookmarks/.env",
        Path.home() / "Documents/Projects/sns-auto/.env",
        Path.home() / ".env",
    ]
    for p in search_paths:
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            for k in ("EXA_API_KEY", "ANTHROPIC_API_KEY"):
                if line.startswith(f"{k}=") and k not in keys:
                    keys[k] = line.split("=", 1)[1].strip()
    return keys


_THIN_THRESHOLD = 300  # この文字数以下なら次の手段へ


def _fallback_fetch(url: str) -> str:
    """Exa コンテンツが薄い URL を Scrapling → requests の順でフェッチ"""
    # 1. Scrapling Fetcher（CSS解析・高速）
    try:
        from scrapling.fetchers import Fetcher
        page = Fetcher(auto_match=False).get(url, timeout=10)
        text = " ".join(page.get_all_text(ignore_tags=("script", "style", "nav", "footer", "header")).split())
        if len(text) > _THIN_THRESHOLD:
            print(f"[collect]   Scrapling Fetcher OK: {url[:50]}")
            return text[:4000]
    except Exception as e:
        pass

    # 2. StealthyFetcher（Playwright stealth・tabelog等の強ブロック用）
    try:
        from scrapling.fetchers import StealthyFetcher
        page = StealthyFetcher(auto_match=False).get(url, timeout=25)
        text = " ".join(page.get_all_text(ignore_tags=("script", "style", "nav", "footer", "header")).split())
        if len(text) > _THIN_THRESHOLD:
            print(f"[collect]   StealthyFetcher OK: {url[:50]}")
            return text[:4000]
    except Exception:
        pass

    # 3. requests（最終手段）
    try:
        import requests
        resp = requests.get(
            url, timeout=8,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
        )
        if resp.ok and len(resp.text) > _THIN_THRESHOLD:
            print(f"[collect]   requests OK: {url[:50]}")
            return resp.text[:4000]
    except Exception:
        pass

    return ""


def _search_and_fetch(city_name: str, keys: dict) -> list[str]:
    """Exa で検索し、薄いコンテンツは自動フォールバックで補完して返す"""
    from exa_py import Exa
    exa = Exa(api_key=keys["EXA_API_KEY"])

    all_texts = []
    seen_urls = set()

    for query_tpl in SEARCH_QUERIES:
        query = query_tpl.format(city=city_name)
        try:
            results = exa.search(
                query,
                num_results=4,
                type="neural",
                contents={"text": {"max_characters": 3000}},
                include_domains=[
                    "tabelog.com", "retty.me", "jalan.net", "rurubu.jp",
                    "travel.rakuten.co.jp", "tripadvisor.jp", "hotpepper.jp",
                    "norecle.jp", "fukuoka-now.com", "walkerplus.com",
                ],
            )
            for r in results.results:
                if r.url in seen_urls:
                    continue
                seen_urls.add(r.url)

                text = (r.text or "").strip()

                if len(text) >= _THIN_THRESHOLD:
                    # Exa で十分なコンテンツが取れた
                    all_texts.append(f"--- {r.url} ---\n{text}")
                else:
                    # 薄い or 空 → フォールバック
                    print(f"[collect] 薄いコンテンツ({len(text)}字) → fallback: {r.url[:60]}")
                    fallback_text = _fallback_fetch(r.url)
                    if fallback_text:
                        all_texts.append(f"--- {r.url} ---\n{fallback_text}")

        except Exception as e:
            print(f"[collect] Exa 検索失敗 ({query[:30]}...): {e}")

    return all_texts


def _extract_spots(city_name: str, texts: list[str], keys: dict) -> list[dict]:
    """Claude Haiku でスポット情報を JSON として抽出する"""
    import anthropic
    client = anthropic.Anthropic(api_key=keys["ANTHROPIC_API_KEY"])

    combined = "\n\n".join(texts[:12])[:12000]

    prompt = f"""以下は「{city_name}」の旅行・グルメ情報ページの本文テキストです。
このテキストから観光スポット・カフェ・レストラン・パン屋・温泉・体験施設などを抽出してください。

# テキスト
{combined}

# 出力形式（JSON のみ・他テキスト不要）
{{
  "spots": [
    {{
      "name": "店舗・スポット名",
      "category": "カフェ|ランチ|パン|スイーツ|温泉|観光|夜ごはん|その他",
      "desc": "特徴・おすすめポイント（1-2文）",
      "hours": "営業時間・定休日（わかれば）",
      "address": "住所・エリア（わかれば）",
      "source_url": "情報元URL"
    }}
  ]
}}

重複は除いてください。架空の情報は書かないでください。"""

    msg = client.messages.create(
        model=HAIKU_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw.strip()).get("spots", [])
    except Exception:
        return []


def collect_spots(city: dict, force_refresh: bool = False) -> list[dict]:
    """
    都市情報を受け取ってスポットリストを返す。
    キャッシュがあれば再利用（force_refresh=True で再取得）。
    """
    slug = city["slug"]
    city_name = city["name"]
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{slug}.json"

    if cache_path.exists() and not force_refresh:
        spots = json.loads(cache_path.read_text(encoding="utf-8"))
        print(f"[collect] キャッシュ使用: {city_name} {len(spots)}件")
        return spots

    keys = _load_keys()

    if "EXA_API_KEY" not in keys:
        print("[collect] EXA_API_KEY 未設定 → スキップ")
        return []

    print(f"[collect] {city_name} のスポット検索中（Exa）...")
    texts = _search_and_fetch(city_name, keys)
    print(f"[collect] {len(texts)}ページ取得")

    if not texts:
        print("[collect] 取得ゼロ → スキップ")
        return []

    if "ANTHROPIC_API_KEY" not in keys:
        print("[collect] ANTHROPIC_API_KEY 未設定 → スキップ")
        return []

    print(f"[collect] Haiku でスポット抽出中...")
    spots = _extract_spots(city_name, texts, keys)
    print(f"[collect] {len(spots)}件抽出 → {cache_path}")
    cache_path.write_text(
        json.dumps(spots, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return spots


if __name__ == "__main__":
    import sys
    import yaml
    data_path = Path(__file__).parent.parent / "data" / "cities.yaml"
    with open(data_path, encoding="utf-8") as f:
        cities = yaml.safe_load(f)["cities"]
    slug = sys.argv[1] if len(sys.argv) > 1 else "itoshima"
    city = next((c for c in cities if c["slug"] == slug or slug in c["name"]), None)
    if not city:
        print(f"都市 '{slug}' が見つかりません")
        sys.exit(1)
    spots = collect_spots(city, force_refresh=True)
    print(json.dumps(spots[:3], ensure_ascii=False, indent=2))
