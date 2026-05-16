#!/usr/bin/env python3
"""Validate repository structure, YAML, watchlists, and script contracts."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from finance_skillkit import (
    FinanceSafeLoader,
    ROOT,
    evidence_tokens,
    iter_watchlist_items,
    load_evidence_levels,
    load_scoring_model,
    load_themes,
    load_yaml,
    root_path,
)


REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "configs/evidence_levels.yaml",
    "configs/scoring_model.yaml",
    "docs/INDEX.md",
    "docs/framework.zh.md",
    "docs/framework.en.md",
    "docs/investment-philosophy.zh.md",
    "docs/technology-watchlist.zh.md",
    "docs/historical-investment-thesis.zh.md",
    "docs/historical-investment-thesis.en.md",
    "prompts/master_prompt.zh.md",
    "prompts/master_prompt.en.md",
    "prompts/rolling_update_prompt.zh.md",
    "prompts/stock_deep_dive_prompt.zh.md",
    "templates/company_memo.zh.md",
    "templates/rolling_report.zh.md",
    "watchlists/a_hk_watchlist.yaml",
    "watchlists/us_watchlist.yaml",
    "watchlists/themes.yaml",
    "skills/ai-equity-research/SKILL.md",
    "scripts/finance_skillkit.py",
    "scripts/score_watchlist.py",
    "scripts/generate_company_memo.py",
    "scripts/generate_rolling_report.py",
    "scripts/build_catalyst_calendar.py",
    "scripts/build_research_context.py",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def collect_yaml_errors() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.yaml")):
        try:
            with path.open("r", encoding="utf-8") as handle:
                yaml.load(handle, Loader=FinanceSafeLoader)
        except yaml.YAMLError as exc:
            errors.append(f"YAML parse: {rel(path)}: {exc}")
    return errors


def validate_watchlists() -> list[str]:
    errors: list[str] = []
    themes = load_themes()
    evidence_levels = load_evidence_levels()
    allowed_evidence = set(evidence_levels)
    labels = set(load_yaml("configs/scoring_model.yaml").get("labels", {}))
    seen: set[tuple[str, str]] = set()

    for item in iter_watchlist_items("all"):
        location = f"{item.market}:{item.label}:{item.ticker or '<missing ticker>'}"
        if not item.ticker:
            errors.append(f"watchlist: {location}: missing ticker")
        if not item.company:
            errors.append(f"watchlist: {location}: missing company")
        if item.label not in labels:
            errors.append(f"watchlist: {location}: label not defined in scoring_model.yaml")
        if item.theme not in themes:
            errors.append(f"watchlist: {location}: theme '{item.theme}' not defined in themes.yaml")
        tokens = evidence_tokens(item.evidence)
        if not tokens:
            errors.append(f"watchlist: {location}: missing or invalid evidence '{item.evidence}'")
        for token in tokens:
            if token[0] not in allowed_evidence:
                errors.append(f"watchlist: {location}: evidence level '{token}' not defined")
        key = (item.market, item.ticker.upper())
        if key in seen:
            errors.append(f"watchlist: {location}: duplicated ticker in market")
        seen.add(key)
    return errors


def validate_scoring_model() -> list[str]:
    errors: list[str] = []
    scoring = load_scoring_model()
    expected = {
        "order_hardness",
        "profit_capture",
        "capacity_bottleneck",
        "technology_route_position",
        "technology_transition_upside",
        "valuation_and_risk",
    }
    missing = expected - set(scoring)
    if missing:
        errors.append(f"scoring_model: missing weights: {', '.join(sorted(missing))}")
    positive_sum = sum(float(value) for key, value in scoring.items() if key != "valuation_and_risk")
    if positive_sum <= 0:
        errors.append("scoring_model: positive weights must sum above zero")
    if float(scoring.get("valuation_and_risk", 0)) > 0:
        errors.append("scoring_model: valuation_and_risk should be a penalty weight")
    return errors


def validate_templates() -> list[str]:
    errors: list[str] = []
    company_template = root_path("templates/company_memo.zh.md").read_text(encoding="utf-8")
    rolling_template = root_path("templates/rolling_report.zh.md").read_text(encoding="utf-8")
    if "{{company}}" not in company_template:
        errors.append("templates/company_memo.zh.md: missing {{company}} placeholder")
    if "{{date}}" not in rolling_template:
        errors.append("templates/rolling_report.zh.md: missing {{date}} placeholder")
    return errors


def main() -> int:
    errors: list[str] = []

    for required in REQUIRED_FILES:
        if not root_path(required).exists():
            errors.append(f"missing: {required}")

    if not errors:
        errors.extend(collect_yaml_errors())
        errors.extend(validate_scoring_model())
        errors.extend(validate_watchlists())
        errors.extend(validate_templates())

    if errors:
        print(f"FAIL - {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    item_count = sum(1 for _ in iter_watchlist_items("all"))
    print(f"OK - structure, YAML, templates, and {item_count} watchlist entries validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
