# Codex handoff: finance-research v0.3.0

## Delivered
A repo-discoverable standalone skill at `.agents/skills/finance-research/` with evidence discipline, economics/cash-flow/valuation research, core/tactical separation, four exit reviews, trader-study rules, and a new Serenity/@aleabitoreddit supply-chain bottleneck lens.

## v0.3 focus
The new lens treats social posts as discovery signals, not truth. It requires Codex to trace final demand through system architecture to modules, materials/equipment and upstream process constraints, then verify three things before calling something a bottleneck: supply constraint, substitution difficulty, and profit capture.

The seven-question Bottleneck Alpha check is: final demand, unit content, single-point bottleneck, substitution difficulty, semi-monopoly evidence, profit capture, and valuation/expectations. Qualification is tracked from sample to validation, qualification, design win/allocation, production order, ramp, revenue and cash collection. Supercycle claims require evidence across demand, supply and price/profit, not price alone.

Serenity is confirmed to the user-provided `@aleabitoreddit` account, but public posts do not verify complete holdings, execution or returns. A public community distillation of thousands of posts is recorded only as a secondary index; its performance statistics and biographical claims are not inherited as facts.

## Requested Codex work
1. Read root `AGENTS.md`, `.agents/skills/finance-research/SKILL.md`, `README.md`, and only the task-specific references.
2. Run:
   ```bash
   python3 -m unittest discover -s .agents/skills/finance-research/tests -v
   python3 .agents/skills/finance-research/scripts/check_package.py
   ```
3. Check `$finance-research` is discoverable in this checkout.
4. Run the expanded behavioral prompts in `tests/acceptance.md` where independent contexts/tools are available; otherwise mark them not run with the concrete limitation.
5. Verify the model does **not** convert “Serenity says semi-monopoly”, qualification counts, memory price increases, or third-party Serenity performance statistics directly into investment facts.
6. Check compatibility with the legacy framework under `finance_skills/` without overwriting historical theses.
7. Fix only demonstrated package defects on this branch. Do not merge, place trades, fetch private accounts, change global user settings, or install into global skill directories.

Software tests and static checks are not strategy validation. A GitHub PR/comment is not proof that Codex has executed the host-side acceptance run.
