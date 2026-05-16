# Docs Index

Recommended reading order:

1. `historical-investment-thesis.zh.md` — full historical investment thesis in Chinese.
2. `framework.zh.md` — structured Chinese framework.
3. `framework.en.md` — English framework for global-source research.
4. `investment-philosophy.zh.md` — shorter investment philosophy.
5. `technology-watchlist.zh.md` — technology transition watchlist.

Use English documents for overseas source retrieval and Chinese documents for final investor-facing synthesis.

Operational scripts:

1. `scripts/validate_repo.py` — validates repository structure, YAML, watchlists, evidence levels, scoring labels, and templates.
2. `scripts/score_watchlist.py` — creates a research-priority ranking from watchlist metadata.
3. `scripts/generate_company_memo.py` — creates a company memo skeleton from the local template.
4. `scripts/generate_rolling_report.py` — creates a 2-3 day rolling update skeleton.
5. `scripts/build_catalyst_calendar.py` — creates recurring monitoring tasks for orders, capex, margins, and technology-route changes.
6. `scripts/build_research_context.py` — packages local context for GPT/Codex/Deep Research.
