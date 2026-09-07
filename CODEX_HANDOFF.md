# Codex handoff: finance-research v0.4.0

## Delivered
A repo-discoverable standalone skill at `.agents/skills/finance-research/` combining four layers:
1. economics / financial quality / valuation;
2. Serenity-style supply-chain bottleneck discovery with primary-source verification;
3. trader-record / tactical timing / exit discipline;
4. UBS-style portfolio architecture: goals, SAA/TAA, reference currency, liquidity, diversification, leverage review, and rebalancing.

All existing `finance_skills/` files are preserved. No current holdings, account balances, credentials or private chat records are included. No global installation or account changes have been performed.

## Validation status
Software/static package checks and behavioral acceptance are separate from strategy performance. Re-run all tests after this v0.4 update. The new UBS behavioral cases are intentionally marked unexecuted until Codex runs them in an independent host context.

## Requested Codex work
1. Read root `AGENTS.md`, `.agents/skills/finance-research/SKILL.md`, its `README.md`, and only task-relevant references.
2. Run:
   - `python3 -m unittest discover -s .agents/skills/finance-research/tests -v`
   - `python3 .agents/skills/finance-research/scripts/check_package.py`
   Report Python version, exact commands, outputs and failures.
3. Check `$finance-research` is discoverable in this checkout. Do not claim global installation.
4. Execute the behavioral acceptance prompts where independent contexts/tools are actually available. Pay special attention to Serenity evidence separation and UBS SAA/TAA/rebalancing cases.
5. Verify the portfolio layer never invents target allocations without current goals/liquidity/risk/account data, and never lets a high-conviction single-stock thesis override portfolio risk limits.
6. Fix only demonstrated package defects on this branch. Do not merge, trade, fetch private accounts, change global settings, or overwrite the legacy historical thesis.

The GitHub PR and a confirmed Codex run are different states. A comment or passing static test is not evidence of profitable trading or suitability for a real portfolio.
