# AGENTS.md — Codex / GPT Instructions

## Mission

This repository is an investment research playbook. Your job is to help maintain a rigorous, evidence-driven framework for AI infrastructure, A-share/HK-share/U.S. equity research, domestic China AI stack, and commercial space.

Do not generate direct buy/sell commands. Produce structured research, evidence maps, watchlists, thesis reviews, and update reports.

## Language policy

Use English for:

- search queries;
- U.S. company IR pages;
- SEC filings;
- Reuters/Bloomberg/WSJ/FT source gathering;
- machine-readable metadata;
- Codex task execution.

Use Chinese for:

- final user-facing reports;
- A股/港股产业链解释;
- portfolio reasoning;
- risk explanations.

The recommended pattern is bilingual: English for retrieval and technical precision, Chinese for final decision context.

## Core research framework

Evaluate every company or theme through:

1. **Order hardness** — direct named order, official partnership, Reuters/Bloomberg confirmation, or only rumor?
2. **Profit capture** — revenue growth, gross margin, net margin, operating cash flow, ROIC.
3. **Capacity bottleneck** — yield, certification, equipment, power, HBM, CoWoS, lasers, transformers, cooling.
4. **Technology route** — GPU→ASIC, 800G→1.6T/3.2T, pluggable→CPO/OCS, 48V→800VDC, training→inference/agents.
5. **Risk and valuation** — customer concentration, capex, policy, export controls, overpricing.

## Evidence hierarchy

- **S-level**: official filing, SEC/10-K/10-Q, exchange announcement, two-party official partnership, explicitly named contract.
- **A-level**: Reuters, Bloomberg, WSJ, FT, official industry body.
- **B-level**: TrendForce, LightCounting, Omdia, Dell'Oro, SemiAnalysis, public sell-side reports.
- **C-level**: Chinese media without primary source, social media, stock forums, unverified investor Q&A.

Never treat C-level evidence as a core investment reason.

## Key distinctions

Always distinguish:

- direct NVIDIA / Google / OpenAI / Meta / Anthropic order vs indirect relevance;
- confirmed production revenue vs samples / design wins / customer validation;
- current earnings driver vs future technology option;
- high-probability core thesis vs high-payoff speculative option.

## Key themes

- GPU / rack-scale AI factory: NVIDIA, AMD.
- ASIC / TPU / custom accelerators: Broadcom, Marvell, Google TPU, Amazon Trainium, Meta MTIA, OpenAI ASIC.
- HBM and memory: SK Hynix, Micron, Samsung.
- Advanced packaging: TSMC, CoWoS, SoIC, hybrid bonding, ABF substrates.
- Optical interconnect: 800G, 1.6T, 3.2T, LPO/LRO, silicon photonics, CPO, OCS.
- Power and cooling: 48/54V to 800VDC/HVDC, GaN, SiC, solid-state transformers, liquid cooling.
- AI fiber and connection materials: Corning, Amphenol, hollow-core fiber, multi-core fiber, pre-terminated cabling.
- China domestic AI stack: DeepSeek/Qwen/Kimi/Doubao/Hunyuan to Huawei Ascend/CANN, Cambricon, Hygon, domestic servers and cloud.
- Commercial space: reusable launch, satellite manufacturing, satellite internet, remote sensing.

## Required workflow

Before producing a company memo:

1. Read `configs/evidence_levels.yaml`.
2. Read `configs/scoring_model.yaml`.
3. Check `watchlists/` for existing thesis.
4. Use `python3 scripts/score_watchlist.py` or `python3 scripts/build_research_context.py` when triaging a ticker or theme.
5. Use `templates/company_memo.zh.md` or `python3 scripts/generate_company_memo.py <ticker>`.
6. Browse current sources if data may have changed.
7. Cite consequential facts.
8. End with a monitoring checklist.

## Validation

Before committing repo edits:

```bash
python scripts/validate_repo.py
```

Useful local tools:

- `python3 scripts/score_watchlist.py --market all`
- `python3 scripts/generate_company_memo.py NVDA`
- `python3 scripts/generate_rolling_report.py --days 3`
- `python3 scripts/build_catalyst_calendar.py --horizon-days 180`
- `python3 scripts/build_research_context.py --theme optical_interconnect`


## Required investment context

Before performing equity research or updating watchlists, read:

1. `docs/historical-investment-thesis.zh.md`
2. `docs/framework.zh.md`
3. `skills/ai-equity-research/SKILL.md`

The historical thesis is the repository's canonical memory of the investment logic. Do not overwrite it casually. Add new evidence or versioned updates when the market thesis changes.
