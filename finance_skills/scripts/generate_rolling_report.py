#!/usr/bin/env python3
"""Generate a rolling update report skeleton for recent AI infrastructure news."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from pathlib import Path

from finance_skillkit import ROOT, filter_scored_items, load_themes, root_path, write_text_or_stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a 2-3 day rolling update skeleton.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Report date, YYYY-MM-DD.")
    parser.add_argument("--days", type=int, default=3, help="Lookback window described in the report.")
    parser.add_argument("--top", type=int, default=12, help="Number of highest-priority tickers to list.")
    parser.add_argument("--output", help="Optional output path relative to repo root.")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing output file.")
    return parser.parse_args()


def default_output_path(report_date: str) -> str:
    return f"reports/rolling-{report_date}.zh.md"


def render_report(report_date: str, days: int, top: int) -> str:
    template = root_path("templates/rolling_report.zh.md").read_text(encoding="utf-8")
    rows = filter_scored_items("all")[:top]
    themes = load_themes()
    theme_counts = Counter(row["theme"] for row in rows)
    focus_lines = []
    for row in rows:
        focus_lines.append(
            f"- {row['ticker']} {row['company']}：{row['label']} / {row['theme']} / "
            f"证据 {row['evidence']} / 优先级 {row['research_priority']}"
        )
    theme_lines = []
    for theme, count in theme_counts.most_common():
        thesis = themes.get(theme, {}).get("thesis", "")
        theme_lines.append(f"- {theme}（{count}）：{thesis}")

    source_checklist = """## 信息源检查清单

- 官方公告、交易所公告、SEC/10-K/10-Q/8-K、公司 IR。
- Reuters、Bloomberg、WSJ、Financial Times 等权威媒体。
- TrendForce、LightCounting、Omdia、Dell'Oro、SemiAnalysis 等产业报告。
- 中文媒体、调研纪要、投资者问答只能作为线索，不能单独作为核心证据。
"""

    report = template.replace("{{date}}", report_date)
    report = report.replace(
        "## 本期核心结论\n",
        f"## 本期核心结论\n\n- 覆盖窗口：过去 {days} 天。\n- 本报告为研究骨架，需要用最新来源填充事实和引用。\n",
    )
    report = report.replace(
        "## 最新订单与资本开支\n",
        "## 最新订单与资本开支\n\n"
        "- 核验是否有客户点名订单、长期供货协议、产能预订或 capex 指引变化。\n"
        "- 对每条事实标注 S/A/B/C 证据等级。\n",
    )
    report = report.replace(
        "## 新增观察标的\n",
        "## 新增观察标的\n\n"
        "### 自动优先关注清单\n\n"
        + "\n".join(focus_lines)
        + "\n\n### 主题覆盖\n\n"
        + "\n".join(theme_lines)
        + "\n",
    )
    report = report.replace(
        "## 下次跟踪问题\n",
        source_checklist + "\n## 下次跟踪问题\n",
    )
    return report.rstrip() + "\n"


def main() -> int:
    args = parse_args()
    output = args.output or default_output_path(args.date)
    path = Path(output)
    if not path.is_absolute():
        path = ROOT / path
    if path.exists() and not args.overwrite:
        raise SystemExit(f"{path.relative_to(ROOT)} already exists. Use --overwrite to replace it.")
    write_text_or_stdout(render_report(args.date, args.days, args.top), str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
