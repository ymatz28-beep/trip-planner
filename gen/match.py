"""
vibe/キーワード → cities.yaml スコアリング → 上位3都市提案
"""
import sys
import yaml
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_cities() -> list[dict]:
    with open(DATA_DIR / "cities.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["cities"]


def load_questionnaire() -> dict:
    with open(DATA_DIR / "cities.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["questionnaire"]


def score_city(city: dict, answers: dict) -> int:
    score = 0

    # q1: distance filter (hard filter — no score, just exclude)
    dist_filter = answers.get("q1_dist_filter", [])
    if dist_filter and city.get("dist") not in dist_filter:
        return -999  # 除外

    # q2: vibe tags boost
    vibe_boost_tags = answers.get("q2_tags_boost", [])
    city_tags = set(city.get("tags", []) + city.get("keywords", []))
    score += sum(2 for t in vibe_boost_tags if t in city_tags)

    # q4: free text keyword match
    must_keywords = answers.get("q4_must_keywords", [])
    for kw in must_keywords:
        if any(kw in t for t in city_tags):
            score += 3  # キーワードの一致は高得点

    # rank bonus
    rank_bonus = {"S": 3, "A": 1, "B": 0}
    score += rank_bonus.get(city.get("rank", "B"), 0)

    return score


def run_questionnaire() -> dict:
    """対話形式で5問に答えてもらい answers dict を返す"""
    q = load_questionnaire()
    answers = {}

    print("\n" + "=" * 50)
    print("  旅先を一緒に決めましょう！")
    print("=" * 50 + "\n")

    # Q1: 距離感
    q1 = q["q1_distance"]
    print(f"Q1. {q1['label']}")
    opts = q1["options"]
    for i, opt in enumerate(opts, 1):
        print(f"  {i}. {opt['label']}")
    while True:
        try:
            choice = int(input("番号を入力: ").strip()) - 1
            if 0 <= choice < len(opts):
                selected = opts[choice]
                answers["q1_value"] = selected["value"]
                answers["q1_dist_filter"] = selected.get("filter", [])
                break
        except (ValueError, IndexError):
            pass
        print("  1〜4の番号で入力してください")

    # Q2: やりたいこと
    print(f"\nQ2. {q['q2_vibe']['label']}")
    opts2 = q["q2_vibe"]["options"]
    for i, opt in enumerate(opts2, 1):
        print(f"  {i}. {opt['label']}")
    while True:
        try:
            choice = int(input("番号を入力: ").strip()) - 1
            if 0 <= choice < len(opts2):
                selected = opts2[choice]
                answers["q2_value"] = selected["value"]
                answers["q2_tags_boost"] = selected.get("tags_boost", [])
                break
        except (ValueError, IndexError):
            pass
        print("  番号で入力してください")

    # Q3: 誰と
    print(f"\nQ3. {q['q3_companion']['label']}")
    opts3 = q["q3_companion"]["options"]
    for i, opt in enumerate(opts3, 1):
        print(f"  {i}. {opt['label']}")
    while True:
        try:
            choice = int(input("番号を入力: ").strip()) - 1
            if 0 <= choice < len(opts3):
                answers["q3_value"] = opts3[choice]["value"]
                answers["q3_note"] = opts3[choice].get("note", "")
                break
        except (ValueError, IndexError):
            pass
        print("  番号で入力してください")

    # Q4: 外せないキーワード（自由記述）
    print(f"\nQ4. {q['q4_must']['label']}")
    print(f"  例: {', '.join(q['q4_must']['examples'])}")
    raw = input("キーワード（スペース区切り、なければ Enter）: ").strip()
    answers["q4_must_keywords"] = raw.split() if raw else []

    # Q5: ペース
    print(f"\nQ5. {q['q5_pace']['label']}")
    opts5 = q["q5_pace"]["options"]
    for i, opt in enumerate(opts5, 1):
        print(f"  {i}. {opt['label']}")
    while True:
        try:
            choice = int(input("番号を入力: ").strip()) - 1
            if 0 <= choice < len(opts5):
                answers["q5_value"] = opts5[choice]["value"]
                answers["q5_density"] = opts5[choice].get("timeline_density", "medium")
                break
        except (ValueError, IndexError):
            pass
        print("  番号で入力してください")

    return answers


def recommend(answers: dict, top_n: int = 3) -> list[dict]:
    """スコアリングして上位 top_n 都市を返す"""
    cities = load_cities()
    scored = []
    for city in cities:
        s = score_city(city, answers)
        if s > -999:
            scored.append((s, city))
    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, city in scored[:top_n]:
        reason = _build_reason(city, answers)
        results.append({"city": city, "score": score, "reason": reason})
    return results


def _build_reason(city: dict, answers: dict) -> str:
    """都市をすすめる理由を1行で生成"""
    vibe_map = {
        "food":    "食の充実度",
        "nature":  "自然の景観",
        "culture": "街歩き・文化",
        "relax":   "温泉・静養",
    }
    vibe = vibe_map.get(answers.get("q2_value", ""), "魅力")

    must = answers.get("q4_must_keywords", [])
    matched = [kw for kw in must if any(kw in t for t in city.get("tags", []) + city.get("keywords", []))]

    parts = [city["vibe"]]
    if matched:
        parts.append(f"「{'・'.join(matched)}」がぴったり")
    if city.get("season_note"):
        parts.append(city["season_note"].split("。")[0])

    return " — ".join(parts)


def interactive_match() -> dict | None:
    """対話 → 都市確定まで実行。選んだ city dict を返す"""
    answers = run_questionnaire()
    results = recommend(answers)

    if not results:
        print("\n条件に合う都市が見つかりませんでした。条件を緩めてみてください。")
        return None

    print("\n" + "=" * 50)
    print("  おすすめの旅先トップ3")
    print("=" * 50)
    for i, r in enumerate(results, 1):
        c = r["city"]
        print(f"\n{i}. {c['name']} ({c['prefecture']}) — {c.get('dist', '')} / 車{c.get('drive_min', '?')}分")
        print(f"   {r['reason']}")

    print("\nどれにする？（1〜3）または 0 でやり直し: ", end="")
    while True:
        try:
            choice = int(input().strip())
            if choice == 0:
                return None
            if 1 <= choice <= len(results):
                return results[choice - 1]["city"]
        except (ValueError, IndexError):
            pass
        print("番号で入力してください: ", end="")


if __name__ == "__main__":
    city = interactive_match()
    if city:
        print(f"\n決定: {city['name']} → {city.get('base_html', city['slug'] + '.html')}")
