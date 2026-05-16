#!/usr/bin/env python3
"""Rank watchlist names by research priority using local evidence metadata."""

from __future__ import annotations

import argparse

from finance_skillkit import filter_scored_items, render_rows, write_text_or_stdout


COLUMNS = [
    "market",
    "ticker",
    "company",
    "label",
    "theme",
    "evidence",
    "evidence_score",
    "research_priority",
    "score_band",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score local watchlists. This is a research triage score, not a return forecast."
    )
    parser.add_argument("--market", default="all", help="all, us, or a_hk")
    parser.add_argument(
        "--label",
        action="append",
        help="Filter by watchlist bucket. Can be repeated, e.g. --label core --label growth.",
    )
    parser.add_argument("--min-score", type=float, help="Only show rows at or above this score.")
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "csv", "json"],
        help="Output format.",
    )
    parser.add_argument("--output", help="Optional output path relative to repo root.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    labels = set(args.label) if args.label else None
    rows = filter_scored_items(args.market, labels=labels, min_score=args.min_score)
    text = render_rows(rows, args.format, COLUMNS)
    write_text_or_stdout(text, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
