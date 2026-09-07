# Repository entrypoint

The existing `finance_skills/` project and its historical thesis are preserved. Before editing that subtree, read `finance_skills/AGENTS.md` and follow its scoped instructions. Resolve its relative paths from `finance_skills/`, not from the repository root.

The new standalone research skill lives at `.agents/skills/finance-research/SKILL.md`. Read it for equity, industry, trader-record, valuation or exit-plan research. Use Chinese final reports and original-language evidence retrieval. Do not read every reference for a narrow task.

## Code Review Rules

### Evidence and financial boundaries
Flag changes that turn broker-branch data into personal PnL, use future information in a historical decision, invent prices/positions, or present tests as validated trading performance. Keep facts, assumptions and unknowns separate.

### Scope and privacy
This is research software, not a trading agent. Do not place orders, change brokerage accounts, access secrets, upload real account data, overwrite historical thesis files or install into the user's global directories without explicit permission. Never auto-merge this handoff.

### Validation
From the repository root, run:
```
python3 -m unittest discover -s .agents/skills/finance-research/tests -v
python3 .agents/skills/finance-research/scripts/check_package.py
```
Behavioral acceptance in `.agents/skills/finance-research/tests/acceptance.md` is separate. Record actual outputs and environment; leave unexecuted cases unexecuted. Read `CODEX_HANDOFF.md` for handoff scope.
