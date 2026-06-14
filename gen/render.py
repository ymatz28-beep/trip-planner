"""
plan.json → HTML (kurume.html と同じクラス語彙)
Jinja2 テンプレートを使ってレンダリング
"""
import json
import subprocess
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

TEMPLATE_DIR = Path(__file__).parent.parent
OUT_DIR = Path(__file__).parent.parent


def render_plan(plan: dict, out_path: Path | None = None) -> Path:
    """
    plan dict から HTML を生成して保存
    Returns: 生成した HTML ファイルのパス
    """
    if not HAS_JINJA2:
        raise ImportError("pip install jinja2 が必要です")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
    )

    template_path = TEMPLATE_DIR / "template.html"
    if not template_path.exists():
        raise FileNotFoundError(f"template.html が見つかりません: {template_path}")

    tmpl = env.get_template("template.html")
    html = tmpl.render(**plan)

    if out_path is None:
        out_path = OUT_DIR / f"{plan['slug']}.html"

    out_path.write_text(html, encoding="utf-8")
    print(f"[render] → {out_path.resolve()}")
    subprocess.run(["open", str(out_path)], check=False)
    return out_path


if __name__ == "__main__":
    import sys

    plan_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if plan_path and plan_path.exists():
        plan = json.loads(plan_path.read_text())
        render_plan(plan)
    else:
        print("使い方: python -m gen.render <plan.json のパス>")
