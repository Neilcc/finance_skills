# Skill: AI Equity Research Playbook

## When to use

Use this skill when the user asks for AI infrastructure stock research, A-share/HK-share/U.S. equity analysis, NVIDIA/Google/OpenAI/Meta/Anthropic supply-chain mapping, DeepSeek/domestic AI chain analysis, optical modules, CPO/OCS, silicon photonics, HBM, advanced packaging, 800VDC, GaN/SiC, data-center power, or rolling market updates.

## Model language strategy

Use English for search queries, U.S. official sources, SEC/IR pages, Reuters/Bloomberg/WSJ, and Codex execution.

Use Chinese for final reports, A-share/HK-share analysis, portfolio reasoning, and risk explanations.

English improves source retrieval quality. Chinese improves alignment with the user's investment decision context.

## Process

1. Read `AGENTS.md`.
2. Read `docs/framework.zh.md` and `docs/framework.en.md`.
3. Identify the relevant theme in `watchlists/themes.yaml`.
4. Pull relevant companies from `watchlists/a_hk_watchlist.yaml` and `watchlists/us_watchlist.yaml`.
5. Apply evidence levels and scoring model.
6. Use `scripts/score_watchlist.py` for triage and `scripts/build_research_context.py` to assemble local context.
7. Use templates from `templates/`, or generate a skeleton with `scripts/generate_company_memo.py`.
8. Browse for current facts before making claims that may have changed.
9. Cite all consequential facts.

## Warning

Never treat a market rumor as a confirmed order. If a company has no named NVIDIA/Google/OpenAI/Meta/Anthropic order, explicitly say so.

## Script shortcuts

```bash
python3 scripts/validate_repo.py
python3 scripts/score_watchlist.py --market all
python3 scripts/generate_company_memo.py NVDA
python3 scripts/generate_rolling_report.py --days 3
python3 scripts/build_catalyst_calendar.py --horizon-days 180
python3 scripts/build_research_context.py --ticker NVDA
```


## Historical thesis reference

For any long-form AI infrastructure equity analysis, first consult:

- `docs/historical-investment-thesis.zh.md`
- `docs/historical-investment-thesis.en.md`

These documents preserve the long-term reasoning framework: order hardness, profit retention, capacity bottlenecks, technology migration, A-share/HK-share/US-share mapping, and high-upside optionality.
