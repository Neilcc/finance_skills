#!/usr/bin/env python3
"""Build a compact research context pack for GPT/Codex/Deep Research."""

from __future__ import annotations

import argparse

from finance_skillkit import (
    fail,
    filter_scored_items,
    find_watchlist_item,
    load_evidence_levels,
    load_scoring_model,
    load_themes,
    root_path,
    score_item,
    today_iso,
    write_text_or_stdout,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a markdown context pack for research.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ticker", help="Build context for a ticker in the watchlists.")
    group.add_argument("--theme", help="Build context for a theme in watchlists/themes.yaml.")
    parser.add_argument("--top", type=int, default=10, help="Max names to include for a theme context.")
    parser.add_argument("--output", help="Optional output path relative to repo root.")
    return parser.parse_args()


def evidence_summary() -> str:
    levels = load_evidence_levels()
    lines = []
    for level in ["S", "A", "B", "C"]:
        data = levels.get(level, {})
        lines.append(f"- {level}: {data.get('name', '')}。使用原则：{data.get('usage', '')}")
    return "\n".join(lines)


def scoring_summary() -> str:
    scoring = load_scoring_model()
    return "\n".join(f"- {key}: {value}" for key, value in scoring.items())


def base_context(title: str) -> list[str]:
    return [
        f"# {title}",
        "",
        f"生成日期：{today_iso()}",
        "",
        "## 研究边界",
        "",
        "- 本材料用于生成研究任务上下文，不构成投资建议。",
        "- 必须区分直接订单、间接受益、产业链推断和传闻。",
        "- 任何时效性事实都需要重新浏览官方来源或权威媒体。",
        "",
        "## 证据等级",
        "",
        evidence_summary(),
        "",
        "## 本地评分权重",
        "",
        scoring_summary(),
        "",
    ]


def ticker_context(ticker: str) -> str:
    item = find_watchlist_item(ticker)
    if not item:
        fail(f"Ticker '{ticker}' was not found in watchlists/.")
    assert item is not None

    themes = load_themes()
    scored = score_item(item)
    title = f"Research Context: {item.company} ({item.ticker})"
    lines = base_context(title)
    lines.extend(
        [
            "## Watchlist Metadata",
            "",
            f"- Market: {item.market}",
            f"- Bucket: {item.label}",
            f"- Theme: {item.theme}",
            f"- Evidence: {item.evidence}",
            f"- Research priority: {scored['research_priority']} / {scored['score_band']}",
            f"- Theme thesis: {themes.get(item.theme, {}).get('thesis', '')}",
            "",
            "## Research Tasks",
            "",
            "1. Verify latest company filings, IR decks, and earnings call commentary.",
            "2. Build an evidence map separating S/A/B/C evidence.",
            "3. Test profit capture through margins, cash flow, inventory, and receivables.",
            "4. Identify the main thesis-breakers for the next two quarters.",
            "5. Produce a Chinese memo using `templates/company_memo.zh.md`.",
            "",
            "## Suggested Source Queries",
            "",
            f"- `{item.company} {item.ticker} investor relations latest earnings AI data center`",
            f"- `{item.company} {item.ticker} SEC 10-K 10-Q AI revenue gross margin`",
            f"- `{item.company} {item.theme} Reuters Bloomberg order customer`",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def theme_context(theme: str, top: int) -> str:
    themes = load_themes()
    if theme not in themes:
        fail(f"Theme '{theme}' was not found in watchlists/themes.yaml.")
    rows = [row for row in filter_scored_items("all") if row["theme"] == theme][:top]
    title = f"Research Context: {theme}"
    lines = base_context(title)
    lines.extend(
        [
            "## Theme Thesis",
            "",
            themes[theme].get("thesis", ""),
            "",
            "## Watchlist Names",
            "",
        ]
    )
    for row in rows:
        lines.append(
            f"- {row['ticker']} {row['company']} ({row['market']}, {row['label']}): "
            f"evidence {row['evidence']}, priority {row['research_priority']} / {row['score_band']}"
        )
    lines.extend(
        [
            "",
            "## Theme Research Tasks",
            "",
            "1. Map where profit pools sit in the chain and where they may migrate.",
            "2. Separate confirmed orders from customer validation, design wins, and rumors.",
            "3. Compare A/H-share elasticity against U.S. profit capture.",
            "4. List what evidence would upgrade or downgrade each name.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    if args.ticker:
        text = ticker_context(args.ticker)
    else:
        text = theme_context(args.theme, args.top)
    write_text_or_stdout(text, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
