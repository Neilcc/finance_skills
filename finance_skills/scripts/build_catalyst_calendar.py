#!/usr/bin/env python3
"""Build a monitoring calendar from watchlist themes.

The output is a research calendar, not a real market-event calendar. It creates
recurring checks that help keep order hardness, margin capture, and technology
route changes current.
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta

from finance_skillkit import iter_watchlist_items, render_rows, write_text_or_stdout


THEME_TASKS = {
    "gpu_rack_scale_compute": [
        ("quarterly", "Check data-center revenue, networking attach, rack-scale product transition, and gross margin."),
        ("monthly", "Check hyperscaler capex commentary and AI factory deployment signals."),
    ],
    "asic_tpu_custom_compute": [
        ("quarterly", "Check named ASIC customers, backlog, custom silicon revenue mix, and design-win timing."),
        ("monthly", "Check TPU/Trainium/MTIA/OpenAI ASIC supply-chain confirmations."),
    ],
    "hbm_advanced_packaging": [
        ("quarterly", "Check HBM bit shipment, ASP, yield, CoWoS capacity, and capex bottlenecks."),
        ("monthly", "Check HBM4 and advanced packaging roadmap changes."),
    ],
    "optical_interconnect": [
        ("monthly", "Check 800G/1.6T orders, customer concentration, pricing, and module margin trend."),
        ("quarterly", "Check whether profit is migrating to lasers, DSP, silicon photonics, CPO, or OCS."),
    ],
    "power_cooling_800vdc": [
        ("monthly", "Check AI rack power architecture, 800VDC/HVDC adoption, liquid-cooling orders, and grid constraints."),
        ("quarterly", "Check margin capture in power equipment, CDU, cooling, transformers, and switchgear."),
    ],
    "china_domestic_ai_stack": [
        ("monthly", "Check China-local accelerator shipments, inference workloads, procurement, and software ecosystem traction."),
        ("quarterly", "Check revenue quality, inventory, subsidy dependence, and export-control risk."),
    ],
    "commercial_space": [
        ("quarterly", "Check launch cadence, reusable rocket milestones, satellite orders, and ground-terminal economics."),
    ],
}

DEFAULT_TASKS = [
    ("quarterly", "Check latest financials: revenue, gross margin, net margin, operating cash flow, inventory, and receivables."),
    ("monthly", "Check whether the current thesis has stronger or weaker S/A/B evidence."),
]

CADENCE_DAYS = {
    "monthly": 30,
    "quarterly": 90,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a recurring catalyst and monitoring calendar.")
    parser.add_argument("--market", default="all", help="all, us, or a_hk")
    parser.add_argument("--start", default=date.today().isoformat(), help="Start date, YYYY-MM-DD.")
    parser.add_argument("--horizon-days", type=int, default=180, help="How far forward to generate checks.")
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "csv", "json"],
        help="Output format.",
    )
    parser.add_argument("--output", help="Optional output path relative to repo root.")
    return parser.parse_args()


def task_rows(market: str, start: str, horizon_days: int) -> list[dict[str, str]]:
    start_date = date.fromisoformat(start)
    horizon = start_date + timedelta(days=horizon_days)
    rows: list[dict[str, str]] = []
    for item in iter_watchlist_items(market):
        tasks = THEME_TASKS.get(item.theme, DEFAULT_TASKS)
        for cadence, task in tasks:
            step = CADENCE_DAYS[cadence]
            due = start_date + timedelta(days=step)
            while due <= horizon:
                rows.append(
                    {
                        "due_date": due.isoformat(),
                        "cadence": cadence,
                        "market": item.market,
                        "ticker": item.ticker,
                        "company": item.company,
                        "label": item.label,
                        "theme": item.theme,
                        "task": task,
                        "preferred_evidence": "S/A first; B for industry sizing; C only as a lead.",
                    }
                )
                due += timedelta(days=step)
    return sorted(rows, key=lambda row: (row["due_date"], row["market"], row["ticker"]))


def main() -> int:
    args = parse_args()
    columns = [
        "due_date",
        "cadence",
        "market",
        "ticker",
        "company",
        "label",
        "theme",
        "task",
        "preferred_evidence",
    ]
    rows = task_rows(args.market, args.start, args.horizon_days)
    text = render_rows(rows, args.format, columns)
    write_text_or_stdout(text, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
