#!/usr/bin/env python3
"""Generate a Chinese company memo skeleton from templates and watchlists."""

from __future__ import annotations

import argparse
from pathlib import Path

from finance_skillkit import (
    ROOT,
    fail,
    find_watchlist_item,
    load_themes,
    root_path,
    score_item,
    today_iso,
    write_text_or_stdout,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a company research memo skeleton.")
    parser.add_argument("ticker", help="Ticker in the local watchlists, e.g. NVDA or 300308.SZ")
    parser.add_argument("--output", help="Optional output path relative to repo root.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing an existing output file.",
    )
    return parser.parse_args()


def default_output_path(ticker: str) -> str:
    safe = ticker.replace("/", "_").replace(":", "_")
    return f"research/{safe}/company_memo.zh.md"


def build_memo(ticker: str) -> str:
    item = find_watchlist_item(ticker)
    if not item:
        fail(f"Ticker '{ticker}' was not found in watchlists/.")
    assert item is not None

    themes = load_themes()
    scored = score_item(item)
    template = root_path("templates/company_memo.zh.md").read_text(encoding="utf-8")
    title_company = f"{item.company} ({item.ticker})"
    memo = template.replace("{{company}}", title_company)
    theme_thesis = themes.get(item.theme, {}).get("thesis", "")
    metadata = f"""生成日期：{today_iso()}

市场：{item.market}
仓位分类：{item.label}
主题：{item.theme}
现有证据等级：{item.evidence}
研究优先级：{scored["research_priority"]} / {scored["score_band"]}
主题假设：{theme_thesis}

> 使用说明：本文件是研究骨架，不是投资建议。正式结论必须补充最新公告、财报、电话会、权威媒体或产业报告来源。

"""
    memo = memo.replace("\n\n## 一句话结论", f"\n\n{metadata}## 一句话结论", 1)
    memo = memo.replace(
        "## 订单硬度\n",
        "## 订单硬度\n\n- 直接订单：待核验。\n- 间接受益：待核验。\n- 证据等级："
        f"{item.evidence}。\n- 必须区分官方点名、权威媒体确认、产业链推断和市场传闻。\n",
    )
    memo = memo.replace(
        "## 未来6个月监测清单\n",
        "## 未来6个月监测清单\n\n"
        "- 最新季报收入、毛利率、净利率、经营现金流和存货/应收变化。\n"
        "- 是否出现客户点名、正式订单、产能扩张或长期供货协议。\n"
        "- 主题技术路线是否发生迁移，是否削弱当前环节价值。\n"
        "- 估值是否已经透支未来 2-3 个季度增长。\n",
    )
    return memo.rstrip() + "\n"


def main() -> int:
    args = parse_args()
    output = args.output or default_output_path(args.ticker)
    path = Path(output)
    if not path.is_absolute():
        path = ROOT / path
    if path.exists() and not args.overwrite:
        fail(f"{path.relative_to(ROOT)} already exists. Use --overwrite to replace it.")
    write_text_or_stdout(build_memo(args.ticker), str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
