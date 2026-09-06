# Codex handoff: finance-research v0.2.0

## Delivered
A repo-discoverable standalone skill at `.agents/skills/finance-research/`, with a task router, evidence protocol, economics/cash-flow/valuation research, core/tactical separation, four exit reviews, trader-study rules, original-source reading limits, deterministic arithmetic, integrity checks and behavioral acceptance prompts.

All existing `finance_skills/` files are preserved. No current holdings, account balances, credentials or private chat records are included. No global installation or account changes have been performed.

## Validation before handoff
On 2026-09-06 the authoring container passed 46 software unit tests and the static package integrity check. These results do not establish Codex-host behavior or profitable trading strategies. Fourteen behavioral acceptance prompts remain for host-side execution.

## Requested Codex work
1. Read root `AGENTS.md`, the new `SKILL.md` and its `README.md`; inspect the diff without overwriting the existing project.
2. Run the two validation commands in `AGENTS.md`. Report Python version, exact commands, outputs and failures.
3. Check the new skill is discoverable in this checkout. Do not claim installation on the user's computer or across all projects.
4. Where independent contexts and required tools are actually available, execute the 14 acceptance prompts, saving only synthetic/non-private outputs with pass/fail reasons. Otherwise mark them not run with the concrete limitation.
5. Check the five-dimensional framework remains compatible with the legacy project, and evidence letter grades are not silently conflated. Fix only demonstrated package defects on this branch; update hashes after edits.
6. Report results in Chinese in the PR. Do not merge, place trades, change user settings, fetch private accounts, or expand this task into current stock recommendations.

The GitHub handoff request and a confirmed Codex run are different states. A comment alone is not proof that a cloud task ran. Sources for the supported GitHub and skill mechanisms are recorded in the skill's `SOURCES.md`.
