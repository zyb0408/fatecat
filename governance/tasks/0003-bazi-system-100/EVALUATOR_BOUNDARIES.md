# Evaluator Boundaries

任务节点：`TP-09.02`

## 结论

八字规则 evaluator 的长期边界是：生产算法只属于 `fate-core`，评测只读取生产输出，oracle 只服务测试对照，delivery 只做交付呈现。

当前不做大爆炸迁移。`calculate_pure_analysis.py` 仍保留生产入口和返回 schema，但后续新增或拆出的 pattern、hehua、yongshen、fortune、topic 规则只能沿着本文边界移动。

## 目标依赖方向

```text
contracts/fate/*
  -> fate_core.providers / fate_core.adapters
  -> fate_core.kernel
  -> fate_core.usecases.evaluators
  -> fate_core.usecases.calculate_pure_analysis
  -> fatecat-delivery API/Web/Bot/Markdown

fate_core.evaluation
  -> fate_core.usecases

tests/oracles
  -> fate_core.providers / fate_core.usecases
```

禁止方向：

- `fate_core.kernel/providers/usecases` 禁止反向 import `fate_core.evaluation`。
- `fatecat-delivery` 禁止新增八字领域算法；只能调用 `fate_core` 用例并渲染结果。
- `sxtwl`、`sxwnl`、`bazica`、MingLi-Bench 等 oracle/evaluation 资源禁止进入生产主链。
- 无 license 或 reference-only 材料禁止作为 runtime dependency。

## 模块职责

### `fate_core.kernel`

职责：稳定底层排盘和基础领域计算。

允许：

- 历法、节气、真太阳时、早晚子时、起运。
- 四柱、五行、十神、干支关系等基础结构。
- 可被多个用例复用的纯领域计算。

禁止：

- MingLi 预测脚本、benchmark 计分、样本外评估逻辑。
- Web/Bot/Markdown 文案渲染。
- 针对单一报告入口定制的 presentation 字段。

### `fate_core.usecases.calculate_pure_analysis`

职责：生产用例编排和输出契约装配。

允许：

- 调用 kernel/provider 输出。
- 调用 evaluator 生成 `baziBenchmark`、`analysisEvidence`、`ruleIds`、`riskBoundary`。
- 保持 `calculate_pure_analysis(payload)` 对外 schema 稳定。

禁止：

- 继续无限堆叠规则细节。
- 引入 oracle/evaluation 反向依赖。
- 输出未登记、不可追溯或无风险边界的断语。

### `fate_core.usecases.evaluators`

目标目录。后续拆分时按能力切片新建；当前仍可先保留在 `calculate_pure_analysis.py` 内，但所有新增规则按此边界设计。

| Evaluator | 目标文件 | 输入 | 输出 | 证据要求 |
| --- | --- | --- | --- | --- |
| pattern | `fate_core/usecases/evaluators/pattern.py` | 四柱、月令、强弱、透干、通根、规则 registry | `specialPatternCandidates` | `sourceRuleId`、成立条件、破格条件、`riskBoundary` |
| hehua | `fate_core/usecases/evaluators/hehua.py` | 天干地支关系、月令、透干、通根、阻隔、冲破 | `combineTransformMatrix` | state、conditionCatalog、counterConditions、`riskBoundary` |
| yongshen | `fate_core/usecases/evaluators/yongshen.py` | 强弱、寒燥、十神、通关、病药、规则 registry | `yongShenDecision` | scoredStrategies、conflictPolicy、doesNotApplyWhen、`riskBoundary` |
| fortune | `fate_core/usecases/evaluators/fortune.py` | 大运、流年、流月、伏吟、反吟、天克地冲 | `fortuneTriggers` | triggerTypes、reasons、trend-only boundary |
| topic | `fate_core/usecases/evaluators/topic.py` | topic scoring inputs、fortuneTriggers、十神统计 | `topicProfiles` | score、basis、scoreBasis、evidenceFields、lifecycle |

## Evaluation 边界

`domains/fate-analysis/services/fate-core/src/fate_core/evaluation/` 只做离线评测。

允许：

- 读取 MingLi-Bench 本地数据。
- 调用 `calculate_pure_analysis` 生成 predictions。
- 输出 total、answered、correct、accuracy、byCategory、results。
- 记录失败归因和下一轮规则建设优先级。

禁止：

- 被 `kernel`、`providers`、`usecases` 或 `delivery` import。
- 把 benchmark answer、expected、correct、gold label 写回生产逻辑。
- 用人工答案硬编码预测脚本。

## Oracle 边界

oracle 只服务测试和对照，不服务 runtime 决策。

允许：

- `tests/regression/test_calendar_oracle_contract.py` 使用 `sxtwl` 对照稳定四柱样本。
- `domains/fate-analysis/data-products/bazi/golden/*` 保存带 `productionUse: test_only_not_runtime_oracle` 的边界样本。
- 后续用 `bazica`、`sxwnl`、`sxtwl` 做离线差异审计。

禁止：

- 在生产入口直接 import oracle library。
- 让 oracle 输出覆盖 `lunar-python` provider 的 runtime 结果。
- 把无 license reference repo 当作生产依赖扩散。

## Delivery 边界

`domains/experience-delivery/services/fatecat-delivery` 只负责公共入口和交付格式。

允许：

- API/Web/Bot 路由、输入校验、限流、错误映射、健康检查。
- Markdown 报告渲染和可折叠证据块。
- TradeCat Labs 归属和页面元信息。

禁止：

- 新增格局、合化、用神、岁运、专题推理算法。
- 在报告生成器里根据文案二次推断领域结论。
- 让前端或 Bot 分支拥有不同领域判断。

## 拆分规则

1. 每次只抽一个 evaluator 的纯函数，不同时移动 schema、文案和算法。
2. `calculate_pure_analysis(payload)` 返回 schema 必须保持稳定。
3. 抽出模块前先有当前消费者和测试；没有消费者或测试的 evaluator 不创建。
4. 每个 evaluator 输出都必须带 `sourceRuleId` 或可追溯 rule id。
5. 每个 evaluator 输出都必须带 `riskBoundary` 或明确继承父级边界。
6. 新模块只读输入，不修改 raw payload 或全局 registry。
7. 失败回滚只回滚当前 evaluator 切片，不回滚已通过的其他切片。

## 行为保持测试

任一 evaluator 拆分必须至少跑：

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
.venv/bin/python -m pytest tests/regression/test_api_contracts.py -q
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
```

涉及历法/时间边界时追加：

```bash
.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
```

涉及报告/Web 时追加：

```bash
.venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_bazi_statement_golden.py -q
```

## Gate 判定

- `evaluation 不进生产 kernel`：`PASS`
- `oracle 不进主链`：`PASS`
- `delivery 不承载领域算法`：`PASS`
- `pattern/hehua/yongshen/fortune/topic evaluator 有目标边界`：`PASS`

本文件是后续拆分和 review 的边界真相源；不代表本轮已完成大文件物理拆分。
