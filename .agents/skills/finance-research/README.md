# finance-research v0.3.0

金融研究与条件决策，中文输出、原语种证据检索。研究用，不下单、不跟单、不保证收益。

## v0.3 新增
在 v0.2 的核心/战术双轨、五维产业框架、现金反证、反向估值和四类退出之上，加入 **Serenity / @aleabitoreddit Supply-Chain Bottleneck Lens**：从最终需求一路追到材料/晶圆/设备/认证；用“最终需求、单位含量、单点瓶颈、替代难度、半垄断性、利润捕获、预期差”七问做验证；加入 qualification cycle 状态机和 supercycle 判定。

Serenity 原帖只作为 discovery signal，最终由公司、客户、交易所/监管等原始披露证明。社区对其数千条帖子的公开整理只作为二手索引，不直接继承其胜率、收益率、杠杆或人物背景结论。[S18]

## Codex 使用
仓库级路径：`.agents/skills/finance-research/`。在该仓库工作时用 `$finance-research` 显式调用。个人全局安装为 `~/.agents/skills/finance-research/`；同名目录先检查备份，不能静默覆盖。[S11]

示例：
```text
$finance-research 用 Serenity 的 bottleneck lens 研究光模块/CPO：先从 hyperscaler CAPEX 画到激光器、InP 晶圆和上游材料，再用公司披露验证每个瓶颈；最后给利润捕获、反向估值和四类退出。
```

## 本地检查
```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py
```
脚本只有标准库，不联网、不交易、不读取账户或密钥。软件测试、宿主行为验收和策略回测是三回事；通过前两者也不代表有 alpha。

## 文件
`SKILL.md` 是入口；`references/serenity.md` 是供应链瓶颈专项；其他 `references/` 负责证据、估值、交易和交易者协议；`SOURCES.md` 记录实际阅读范围；`tests/acceptance.md` 是 Codex 行为验收。

Serenity 身份已确认到用户给出的 `@aleabitoreddit`，但其完整交易、仓位和收益仍未核验；陈小群资料仍非完整个人账本。
