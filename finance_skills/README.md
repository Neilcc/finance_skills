# finance_skills

这个仓库用于沉淀一套可被 GPT / Codex / Deep Research 反复调用的投资研究框架。当前重点是 AI 基础设施、A股/港股/美股产业链、国产算力、商业航天，以及未来可持续扩展的股市研究技能。

This repo stores bilingual prompts, playbooks, watchlists, and Codex-readable instructions for evidence-driven equity research.

## 核心目标

- 把我们的 AI 基础设施投资逻辑固化为可持续维护的研究系统。
- 让 GPT/Codex 在后续分析中优先读取 `AGENTS.md` 和 `skills/ai-equity-research/SKILL.md`。
- 同时保存中文与英文版本。英文更利于检索全球官方资料和SEC/IR文件；中文更利于A股、港股、产业链、用户决策语境。
- 后续可逐步加入财报摘要、滚动更新、技术路线时间轴、标的评分表。

## 当前研究中心

不要买“AI概念”，而是买 AI 扩张过程中的硬瓶颈：

```text
模型应用 / Agent / 多模态 / 长上下文
→ GPU / ASIC / TPU
→ HBM / CoWoS / 先进封装
→ NVLink / Ethernet / AI Fabric
→ 800G / 1.6T / 3.2T 光互联
→ CPO / OCS / 硅光 / 激光器
→ 800VDC / GaN / SiC / 液冷
→ 光纤 / 连接器 / 铜 / 电网 / 燃气轮机
```

## 文件结构

```text
AGENTS.md
configs/
  evidence_levels.yaml
  scoring_model.yaml
docs/
  framework.zh.md
  framework.en.md
  investment-philosophy.zh.md
  technology-watchlist.zh.md
prompts/
  master_prompt.zh.md
  master_prompt.en.md
  rolling_update_prompt.zh.md
  stock_deep_dive_prompt.zh.md
skills/
  ai-equity-research/SKILL.md
templates/
  company_memo.zh.md
  rolling_report.zh.md
watchlists/
  themes.yaml
  a_hk_watchlist.yaml
  us_watchlist.yaml
scripts/
  README.md
  finance_skillkit.py
  validate_repo.py
  score_watchlist.py
  generate_company_memo.py
  generate_rolling_report.py
  build_catalyst_calendar.py
  build_research_context.py
```

## 常用脚本

先安装脚本依赖：

```bash
python3 -m pip install -r requirements.txt
```

然后使用以下命令把研究框架转成可重复流程：

```bash
# 结构、YAML、watchlist、证据等级和模板校验
python3 scripts/validate_repo.py

# 生成本地 watchlist 研究优先级排序
python3 scripts/score_watchlist.py --market all --format markdown

# 为单个标的生成中文研究备忘录骨架
python3 scripts/generate_company_memo.py NVDA

# 生成 2-3 天滚动更新报告骨架
python3 scripts/generate_rolling_report.py --days 3

# 生成未来 180 天的主题/标的监测日历
python3 scripts/build_catalyst_calendar.py --horizon-days 180 --output outputs/catalyst_calendar.md

# 为 GPT / Codex / Deep Research 生成上下文包
python3 scripts/build_research_context.py --theme optical_interconnect --output context/optical_interconnect.md
```

脚本产生的是研究优先级、备忘录骨架和监测清单，不是收益预测或买卖建议。所有时效性事实仍必须重新核验官方公告、财报、SEC/IR、权威媒体或产业报告。

## 推送到 GitHub

```bash
git clone https://github.com/Neilcc/finance_skills.git
cd finance_skills
# 把本包内容复制进来后：
git add .
git commit -m "Initialize AI equity research playbook"
git push origin develop
```

或者直接运行本仓库里的：

```bash
bash scripts/push_to_github.sh
```

## 免责声明

本仓库只用于研究流程，不构成投资建议。所有结论必须引用来源，标注证据等级，并区分：

- 直接订单 vs 间接受益；
- 收入增长 vs 利润留存；
- 当前财报兑现 vs 未来技术期权；
- 高胜率核心仓 vs 高赔率期权仓。


## Core historical thesis

The repository now includes a consolidated historical investment thesis:

- `docs/historical-investment-thesis.zh.md` — Chinese full version.
- `docs/historical-investment-thesis.en.md` — English compact version.

Use this file as the main memory of the investment logic developed across the discussions:
AI infrastructure bottlenecks, order hardness, profit pools, technology migration, A-share/HK-share/US-share mapping, and high-upside optionality.
