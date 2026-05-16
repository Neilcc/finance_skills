#!/usr/bin/env python3
"""Shared helpers for the finance_skills command-line scripts."""

from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "PyYAML is required. Install it with: python3 -m pip install -r requirements.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]


class FinanceSafeLoader(yaml.SafeLoader):
    """SafeLoader without YAML 1.1 bool coercion.

    Finance tickers such as ON are valid symbols and must not become True.
    """


for first_letter, resolvers in list(FinanceSafeLoader.yaml_implicit_resolvers.items()):
    FinanceSafeLoader.yaml_implicit_resolvers[first_letter] = [
        resolver for resolver in resolvers if resolver[0] != "tag:yaml.org,2002:bool"
    ]

EVIDENCE_POINTS = {
    "S": 95.0,
    "A": 82.0,
    "B": 62.0,
    "C": 35.0,
}

LABEL_PRIORS = {
    "core": 88.0,
    "growth": 74.0,
    "option": 58.0,
    "options": 58.0,
    "domestic_ai_stack": 56.0,
    "watch": 48.0,
    "high_risk": 42.0,
}

HARD_BOTTLENECK_THEMES = {
    "gpu_rack_scale_compute",
    "asic_tpu_custom_compute",
    "hbm_advanced_packaging",
    "optical_interconnect",
    "ai_pcb",
    "power_cooling_800vdc",
    "ai_fiber_materials",
    "advanced_packaging",
    "advanced_packaging_pcb",
    "high_speed_materials",
}


@dataclass(frozen=True)
class WatchlistItem:
    ticker: str
    company: str
    theme: str
    evidence: str
    label: str
    market: str

    def as_dict(self) -> dict[str, str]:
        return {
            "ticker": self.ticker,
            "company": self.company,
            "theme": self.theme,
            "evidence": self.evidence,
            "label": self.label,
            "market": self.market,
        }


def root_path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)


def load_yaml(relative_path: str) -> Any:
    path = root_path(relative_path)
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=FinanceSafeLoader) or {}


def write_text_or_stdout(text: str, output: str | None) -> None:
    if output:
        path = Path(output)
        if not path.is_absolute():
            path = ROOT / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        try:
            display_path = path.relative_to(ROOT)
        except ValueError:
            display_path = path
        print(f"Wrote {display_path}")
    else:
        print(text)


def load_themes() -> dict[str, dict[str, Any]]:
    return dict(load_yaml("watchlists/themes.yaml").get("themes", {}))


def load_evidence_levels() -> dict[str, dict[str, Any]]:
    return dict(load_yaml("configs/evidence_levels.yaml").get("evidence_levels", {}))


def load_scoring_model() -> dict[str, Any]:
    return dict(load_yaml("configs/scoring_model.yaml").get("scoring_model", {}))


def normalize_market(market: str) -> str:
    aliases = {
        "all": "all",
        "us": "us",
        "usa": "us",
        "a_hk": "a_hk",
        "ahk": "a_hk",
        "cn": "a_hk",
        "china": "a_hk",
    }
    key = market.lower().replace("-", "_")
    if key not in aliases:
        raise SystemExit(f"Unsupported market '{market}'. Use all, us, or a_hk.")
    return aliases[key]


def evidence_tokens(value: str) -> list[str]:
    return re.findall(r"[SABC][+-]?", str(value).upper())


def evidence_score(value: str) -> float:
    tokens = evidence_tokens(value)
    if not tokens:
        return 0.0
    scores = []
    for token in tokens:
        base = EVIDENCE_POINTS[token[0]]
        if token.endswith("+"):
            base += 3.0
        elif token.endswith("-"):
            base -= 5.0
        scores.append(max(0.0, min(100.0, base)))
    return sum(scores) / len(scores)


def theme_alignment_score(theme: str) -> float:
    if theme in HARD_BOTTLENECK_THEMES:
        return 82.0
    if theme in load_themes():
        return 66.0
    return 40.0


def score_item(item: WatchlistItem) -> dict[str, Any]:
    evidence = evidence_score(item.evidence)
    label_prior = LABEL_PRIORS.get(item.label, 50.0)
    theme_score = theme_alignment_score(item.theme)
    score = evidence * 0.50 + label_prior * 0.35 + theme_score * 0.15
    if item.label == "high_risk":
        score -= 8.0
    score = max(0.0, min(100.0, score))
    return {
        **item.as_dict(),
        "evidence_score": round(evidence, 1),
        "research_priority": round(score, 1),
        "score_band": score_band(score),
    }


def score_band(score: float) -> str:
    if score >= 82:
        return "core-candidate"
    if score >= 70:
        return "active-watch"
    if score >= 55:
        return "option-monitor"
    return "needs-evidence"


def iter_watchlist_items(market: str = "all") -> Iterable[WatchlistItem]:
    market = normalize_market(market)
    files = []
    if market in {"all", "us"}:
        files.append(("us", "watchlists/us_watchlist.yaml", "us_watchlist"))
    if market in {"all", "a_hk"}:
        files.append(("a_hk", "watchlists/a_hk_watchlist.yaml", "a_hk_watchlist"))

    for market_name, relative_path, top_key in files:
        data = load_yaml(relative_path).get(top_key, {})
        for label, rows in data.items():
            for row in rows or []:
                yield WatchlistItem(
                    ticker=str(row.get("ticker", "")).strip(),
                    company=str(row.get("company", "")).strip(),
                    theme=str(row.get("theme", "")).strip(),
                    evidence=str(row.get("evidence", "")).strip(),
                    label=str(label).strip(),
                    market=market_name,
                )


def find_watchlist_item(ticker: str) -> WatchlistItem | None:
    needle = ticker.upper()
    for item in iter_watchlist_items("all"):
        if item.ticker.upper() == needle:
            return item
    return None


def filter_scored_items(
    market: str = "all",
    labels: set[str] | None = None,
    min_score: float | None = None,
) -> list[dict[str, Any]]:
    rows = [score_item(item) for item in iter_watchlist_items(market)]
    if labels:
        rows = [row for row in rows if row["label"] in labels]
    if min_score is not None:
        rows = [row for row in rows if row["research_priority"] >= min_score]
    return sorted(rows, key=lambda row: (-row["research_priority"], row["market"], row["ticker"]))


def to_markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join([header, divider, *body])


def render_rows(rows: list[dict[str, Any]], output_format: str, columns: list[str]) -> str:
    output_format = output_format.lower()
    if output_format == "json":
        return json.dumps(rows, ensure_ascii=False, indent=2)
    if output_format == "csv":
        from io import StringIO

        buffer = StringIO()
        writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
        return buffer.getvalue().rstrip()
    if output_format == "markdown":
        return to_markdown_table(rows, columns)
    raise SystemExit("Unsupported format. Use markdown, csv, or json.")


def today_iso() -> str:
    from datetime import date

    return date.today().isoformat()


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)
