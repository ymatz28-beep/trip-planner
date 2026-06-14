"""
trip-planner CLI
使い方:
  python -m gen.cli                          # 対話モード（vibe → 都市提案 → 生成）
  python -m gen.cli 糸島                    # 都市名直指定
  python -m gen.cli 糸島 --date 2026-07-12  # 日付も指定
  python -m gen.cli ukiha --refresh         # キャッシュを無視して再収集
"""
import argparse
import json
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_PATH = ROOT / "data" / "cities.yaml"
CACHE_DIR = ROOT / ".cache"


def load_cities() -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)["cities"]


def find_city(query: str, cities: list[dict]) -> dict | None:
    """slug または都市名（部分一致）で検索"""
    q = query.strip()
    for c in cities:
        if c["slug"] == q or c["name"] == q or q in c["name"]:
            return c
    return None


def run(args=None):
    parser = argparse.ArgumentParser(
        description="AI 旅行プラン生成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python -m gen.cli                 # 対話モード
  python -m gen.cli 糸島            # 糸島のプランを生成
  python -m gen.cli ukiha --date 2026-07-20
  python -m gen.cli 南阿蘇 --refresh
        """,
    )
    parser.add_argument("city", nargs="?", help="都市名または slug（省略で対話モード）")
    parser.add_argument("--date", default="", help="旅行日（例: 2026-07-12）")
    parser.add_argument("--refresh", action="store_true", help="キャッシュを無視して再収集")
    parser.add_argument("--no-collect", action="store_true", help="スポット収集をスキップ（キャッシュのみ使用）")
    parser.add_argument("--no-render", action="store_true", help="HTML 生成をスキップ（plan.json まで）")
    ns = parser.parse_args(args)

    cities = load_cities()
    answers = {}

    # --- 都市確定 ---
    if ns.city:
        city = find_city(ns.city, cities)
        if not city:
            print(f"エラー: 都市 '{ns.city}' が cities.yaml に見つかりません")
            print("登録済み:", ", ".join(c["name"] for c in cities))
            sys.exit(1)
        print(f"\n旅先: {city['name']} ({city['prefecture']}) — 車{city.get('drive_min','?')}分")
        answers["q1_value"] = "day_trip"
        answers["q5_density"] = "medium"
        answers["q3_value"] = "friends"
    else:
        from gen.match import interactive_match
        city = interactive_match()
        if not city:
            print("キャンセルされました")
            sys.exit(0)

    # --- 日付 ---
    date = ns.date
    if not date:
        date = input("\n旅行日は？（例: 2026-07-12、空白で未定）: ").strip()
        if not date:
            date = "未定"

    print(f"\n[gen] {city['name']} / {date} のプランを生成します\n")

    # --- Step 1: スポット収集 ---
    if ns.no_collect:
        cache_path = CACHE_DIR / "spots" / f"{city['slug']}.json"
        spots = json.loads(cache_path.read_text()) if cache_path.exists() else []
        print(f"[collect] キャッシュ使用: {len(spots)}件")
    else:
        from gen.collect import collect_spots
        spots = collect_spots(city, force_refresh=ns.refresh)

    # --- Step 2: plan.json 生成 ---
    from gen.compose import compose_plan
    plan = compose_plan(city, spots, date, answers)

    plan_path = CACHE_DIR / f"{city['slug']}_plan.json"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[compose] plan.json → {plan_path.resolve()}")

    # --- Step 3: HTML レンダリング ---
    if not ns.no_render:
        template_path = ROOT / "template.html"
        if not template_path.exists():
            print("\n[render] template.html が未作成です")
            print("  まず kurume.html から template.html を生成してください:")
            print("  python -m gen.templatize")
        else:
            from gen.render import render_plan
            out = render_plan(plan)
            print(f"\n✅ 完了: {out.resolve()}")
    else:
        print(f"\n✅ plan.json 生成完了: {plan_path.resolve()}")


if __name__ == "__main__":
    run()
