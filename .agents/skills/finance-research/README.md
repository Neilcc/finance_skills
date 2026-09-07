# finance-research v0.4.0

金融研究与条件决策，中文输出、原语种证据检索。研究用，不下单、不跟单、不保证收益。

## v0.4 新增：UBS Portfolio Architecture

在 v0.3 的 Serenity 供应链瓶颈框架、基本面/估值、核心/战术双轨和四类退出之上，加入 UBS 2025 CIO 官方投资哲学的组合管理层：[S20]

- Personal / Long term / Active / Diversified 四支柱；
- SAA（战略配置）/ TAA（战术偏离）/ Instrument Selection（工具选择）三层；
- 参考币种、流动性、总财富与风险承受能力；
- 定期复核和再平衡；
- 杠杆作为独立风险，而不是收益捷径。

这层不替代个股Alpha。推荐顺序是：**UBS 定组合边界 → Serenity 找产业瓶颈 → 基本面/估值证伪 → 战术框架择时 → UBS 再检查集中度与再平衡。**

Serenity 原帖仍只作为 discovery signal，最终由公司、客户、交易所/监管等原始披露证明。社区整理只作为二手索引，不直接继承其胜率、收益率、杠杆或人物背景结论。[S18]

## Codex 使用

仓库级路径：`.agents/skills/finance-research/`。在该仓库工作时用 `$finance-research` 显式调用。个人全局安装为 `~/.agents/skills/finance-research/`；同名目录先检查备份，不能静默覆盖。[S11]

示例：
```text
$finance-research 研究AI光模块：先用UBS层确认这是核心SAA还是战术TAA风险预算，再用Serenity bottleneck lens追到激光器/InP等环节，用公司披露验证瓶颈，最后给估值、交易条件、退出和再平衡触发。
```

## 本地检查
```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py
```
脚本只有标准库，不联网、不交易、不读取账户或密钥。软件测试、宿主行为验收和策略回测是三回事；通过前两者也不代表有 alpha。

## 文件
`SKILL.md` 是入口；`references/serenity.md` 是供应链瓶颈专项；`references/portfolio-ubs.md` 是组合架构专项；其他 `references/` 负责证据、估值、交易和交易者协议；`SOURCES.md` 记录实际阅读范围；`tests/acceptance.md` 是 Codex 行为验收。

UBS框架只提供组合设计原则，不会从手册直接生成用户的资产比例。用户真实SAA/TAA和仓位必须基于当前目标、流动性、参考币种和授权账户数据。
