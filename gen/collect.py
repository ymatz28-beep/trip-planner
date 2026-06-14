"""
スポット収集パイプライン
1. YouTube Data API v3 → 旅行vlogから地名・スポット抽出
2. Google Places API (新 Places API) → 各スポットの構造化データ
3. 観光公式サイト（ukihalove.jp型）→ curated 情報補強
結果は .cache/spots/{slug}.json にキャッシュして再課金を防ぐ
"""
import json
import os
import time
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / ".cache" / "spots"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")


# ---------------------------------------------------------------------------
# YouTube Data API v3
# ---------------------------------------------------------------------------

def search_youtube_vlogs(city_name: str, max_results: int = 8) -> list[dict]:
    """
    YouTube で旅行 vlog を検索して video ID + タイトル + description を返す
    API key が未設定の場合はスキップ（キャッシュを使う）
    """
    if not YOUTUBE_API_KEY:
        print(f"  [YouTube] YOUTUBE_API_KEY 未設定 → スキップ")
        return []

    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("  [YouTube] google-api-python-client 未インストール: pip install google-api-python-client")
        return []

    query = f"{city_name} 旅行 観光 vlog おすすめ"
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    search_resp = youtube.search().list(
        q=query,
        part="id,snippet",
        type="video",
        regionCode="JP",
        relevanceLanguage="ja",
        maxResults=max_results,
        videoDuration="medium",  # 4-20分 (短すぎず長すぎず)
    ).execute()

    videos = []
    for item in search_resp.get("items", []):
        vid_id = item["id"]["videoId"]
        snippet = item["snippet"]
        videos.append({
            "video_id": vid_id,
            "title": snippet["title"],
            "description": snippet["description"][:500],
            "channel": snippet["channelTitle"],
            "url": f"https://www.youtube.com/watch?v={vid_id}",
        })
    return videos


def extract_spots_from_videos(videos: list[dict], city_name: str) -> list[str]:
    """
    YouTube の動画タイトル + description から Claude API でスポット名を抽出
    Returns: スポット名リスト（日本語）
    """
    if not videos:
        return []

    import anthropic
    client = anthropic.Anthropic()

    texts = "\n\n".join(
        f"【{v['title']}】\n{v['description']}"
        for v in videos
    )
    prompt = f"""以下は「{city_name}」の旅行 vlog の YouTube 動画タイトルと概要です。
動画に登場する可能性が高い観光スポット・カフェ・飲食店・温泉・神社などの固有名詞を抽出してください。

条件:
- {city_name} にある（または近隣）場所のみ
- 固有名詞（店名・施設名・神社名など）のみ抽出
- JSON 配列で出力: ["スポット名1", "スポット名2", ...]
- 最大 20 件

動画テキスト:
{texts}
"""
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()
    try:
        start = raw.index("[")
        end = raw.rindex("]") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return []


# ---------------------------------------------------------------------------
# Google Places API (新 Places API v1)
# ---------------------------------------------------------------------------

def fetch_place_details(spot_name: str, city_name: str) -> dict | None:
    """
    Google Places API (新) で1スポットの詳細を取得
    Returns: {name, address, hours, rating, maps_url, genre}
    """
    if not PLACES_API_KEY:
        return None

    import requests

    # Text Search
    search_url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": PLACES_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.regularOpeningHours,places.rating,places.googleMapsUri,places.types",
    }
    payload = {
        "textQuery": f"{spot_name} {city_name}",
        "languageCode": "ja",
        "maxResultCount": 1,
    }

    resp = requests.post(search_url, headers=headers, json=payload, timeout=10)
    if resp.status_code != 200:
        return None

    places = resp.json().get("places", [])
    if not places:
        return None

    p = places[0]
    hours_raw = p.get("regularOpeningHours", {})
    hours_text = ""
    if "weekdayDescriptions" in hours_raw:
        hours_text = " / ".join(hours_raw["weekdayDescriptions"][:3])

    return {
        "name": p.get("displayName", {}).get("text", spot_name),
        "address": p.get("formattedAddress", ""),
        "hours": hours_text,
        "rating": p.get("rating"),
        "maps_url": p.get("googleMapsUri", f"https://maps.google.com/?q={spot_name}+{city_name}"),
        "types": p.get("types", []),
        "source": "google_places",
    }


# ---------------------------------------------------------------------------
# メインパイプライン
# ---------------------------------------------------------------------------

def collect_spots(city: dict, force_refresh: bool = False) -> list[dict]:
    """
    都市のスポット一覧を収集してキャッシュに保存
    Returns: spot dict のリスト
    """
    slug = city["slug"]
    cache_path = CACHE_DIR / f"{slug}.json"

    if cache_path.exists() and not force_refresh:
        print(f"  [cache] {slug}.json 使用 (--refresh で再収集)")
        with open(cache_path) as f:
            return json.load(f)

    city_name = city["name"]
    print(f"\n  [{city_name}] スポット収集開始...")
    spots = []

    # Step 1: YouTube で vlog 検索
    print(f"  [YouTube] 旅行 vlog 検索中...")
    videos = search_youtube_vlogs(city_name)
    if videos:
        print(f"  [YouTube] {len(videos)}件の動画を発見")
        spot_names = extract_spots_from_videos(videos, city_name)
        print(f"  [YouTube] {len(spot_names)}件のスポット名抽出")

        # Step 2: Google Places で各スポットを構造化
        for name in spot_names:
            if not PLACES_API_KEY:
                spots.append({
                    "name": name,
                    "address": f"{city_name}",
                    "hours": "",
                    "rating": None,
                    "maps_url": f"https://maps.google.com/?q={name}+{city_name}",
                    "source": "youtube_extracted",
                })
            else:
                detail = fetch_place_details(name, city_name)
                if detail:
                    spots.append(detail)
                time.sleep(0.3)  # API レート制限対策
    else:
        print(f"  [YouTube] API 未設定 → 手動スポットデータのみ使用")

    # キャッシュに保存
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(spots, f, ensure_ascii=False, indent=2)

    print(f"  [{city_name}] {len(spots)}件 → .cache/spots/{slug}.json")
    return spots


if __name__ == "__main__":
    import sys
    import yaml

    data_path = Path(__file__).parent.parent / "data" / "cities.yaml"
    with open(data_path) as f:
        cities = yaml.safe_load(f)["cities"]

    target = sys.argv[1] if len(sys.argv) > 1 else "ukiha"
    city = next((c for c in cities if c["slug"] == target), None)
    if city:
        spots = collect_spots(city, force_refresh="--refresh" in sys.argv)
        print(f"\n収集結果 ({len(spots)}件):")
        for s in spots[:5]:
            print(f"  - {s['name']} ({s.get('address','')})")
    else:
        print(f"都市 '{target}' が cities.yaml に見つかりません")
