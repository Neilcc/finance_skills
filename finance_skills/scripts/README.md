# Scripts

These scripts turn the repository's research framework into repeatable local workflows.

## Validate

```bash
python3 scripts/validate_repo.py
```

Checks required files, YAML parsing, watchlist fields, theme references, evidence levels, scoring labels, and template placeholders.

## Score Watchlists

```bash
python3 scripts/score_watchlist.py --market all --format markdown
python3 scripts/score_watchlist.py --market us --min-score 70 --format csv --output outputs/us_scores.csv
```

The score is a research-priority triage score based on local evidence metadata and watchlist bucket. It is not an expected-return forecast.

## Generate Company Memo

```bash
python3 scripts/generate_company_memo.py NVDA
python3 scripts/generate_company_memo.py 300308.SZ --output research/300308.SZ/company_memo.zh.md
```

Creates a Chinese memo skeleton with watchlist metadata, evidence level, theme thesis, and monitoring checklist.

## Generate Rolling Report

```bash
python3 scripts/generate_rolling_report.py --days 3
```

Creates a 2-3 day rolling update skeleton under `reports/` by default.

## Build Catalyst Calendar

```bash
python3 scripts/build_catalyst_calendar.py --horizon-days 180 --format markdown --output outputs/catalyst_calendar.md
```

Builds recurring monitoring tasks for earnings, orders, capex, margins, and technology-route changes.

## Build Research Context

```bash
python3 scripts/build_research_context.py --ticker NVDA --output context/NVDA.md
python3 scripts/build_research_context.py --theme optical_interconnect --output context/optical_interconnect.md
```

Creates a compact context pack for GPT/Codex/Deep Research, including evidence rules, scoring weights, local watchlist metadata, and source-query prompts.
