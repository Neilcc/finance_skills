# finance-research v0.2.0

金融研究与条件决策，中文输出、原语种证据检索。研究用，不下单、不跟单、不保证收益。

## 这一版改了什么
将主入口改为任务路由和条件决策；补上核心/战术双轨、五维产业框架、现金反证、反向PE估值、四类退出、做T比较基准及盲复盘。来源等级改用语义对齐，避免旧包A与旧仓库A混淆。未知人物与业绩仍保持未知。

这是0.x版的结构重构：旧references已整合；旧risk_budget.py/validate_cases.py接口不在本版，替换为finance_math.py/check_package.py。本地旧包保持独立备份，不把旧34项测试冒充本版验收。

## Codex使用
在仓库根目录放置整个目录：`.agents/skills/finance-research/`。在该仓库工作时用 `$finance-research` 显式调用。个人全局安装为 `~/.agents/skills/finance-research/`；同名目录先检查备份，不能静默覆盖。[S11]
本包不修改config.toml、凭证、已有AGENTS.md或用户全局目录。仓库中能读到文件不代表用户本机已经拉取、安装或运行。无联网权限时只处理提供的资料。

示例：
```
$finance-research 研究光模块行业。核验最新披露，把经营、现金、估值和交易条件分开；先给一屏决策卡、最强反证与四类退出，不假设我的持仓。
```

## 本地检查
在本目录执行：
```
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py
```
脚本只有标准库，不联网、不交易、不读取账户或密钥。计算函数为Python接口，见scripts/finance_math.py和测试中的合成示例；默认不把结果持久化。

## 验收边界
软件单元测试、静态包检查、宿主agent行为验收、交易策略回测是四回事。行为用例见tests/acceptance.md，未实际在用户Codex执行之前不得标为通过；此包没有完成策略有效性回测。

## 文件
SKILL.md是入口；references是按需协议；assets是输出模板；SOURCES.md是实际阅读范围；scripts是确定性数学和静态检查；tests是软件测试与宿主验收题。
保留“不交易”、缺数据降级和反证。severity仍未唯一定位；陈小群资料仍非完整个人账本。
