# 用神策略矩阵

## Scope

- Task: `TP-07.01`
- Objective: 定义调候、扶抑、通关、病药的输入字段、评分、冲突和不适用条件。
- Runtime owner: `fate-core`
- Implementation file: `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- Output path: `data.baziBenchmark.yongShenDecision.scoredStrategies`

## Strategy Matrix

| Strategy | Basis | Score Basis | Applies When | Does Not Apply When | Conflict Policy |
| --- | --- | --- | --- | --- | --- |
| 调候 | 月令、节气、寒暖燥湿、调候依据 | `yongShen.defaultBase`, `yongShen.basis`, `yongShen.tiaohouRaw` | 月令、节气、寒暖燥湿、调候原始依据存在 | 缺少季节气候依据；把调候当作医疗/养生处方 | 调候优先解释气候偏性，但不得覆盖扶抑、通关、病药。 |
| 扶抑 | 日主强弱、月令、通根、透干、五行分数 | `yongShen.defaultBase`, `wuxingScores.strongScore`, `wuxingScores.statusDetail` | 日主强弱、月令、通根、透干、五行分数齐备 | 只存在单一强弱标签；五行分数或藏干缺失 | 扶抑与调候冲突时并列呈现，不能单独覆盖用神。 |
| 通关 | 干支冲合刑害破、五行克战链、关系优先级 | `yongShen.defaultBase`, `baziBenchmark.ganzhiPriority` | 干支冲合刑害破或五行克战关系显著；存在可缓冲的中介五行 | 关系链不可追溯；只有单点五行偏枯而无冲突链 | 通关只解释冲突缓冲，不替代调候或扶抑主策略。 |
| 病药 | 五行偏枯、寒暖燥湿、格局病处 | `yongShen.defaultBase`, `wuxingScores.fiveElementScore`, `climateScores` | 五行偏枯、寒暖燥湿或格局病处可定位；存在对应药处证据 | 偏枯不明显；病处无法回指证据字段；输出生活处方 | 病药作为解释优先级，不输出现实诊疗、金融或法律决策。 |

## Output Contract

- 每个 strategy 必须包含 `basis`、`score`、`scoreBasis`、`evidenceFields`、`appliesWhen`、`doesNotApplyWhen`、`conflictPolicy`。
- `scoreBasis` 必须是可审计因子数组，每个因子包含 `factor`、`value`、`evidenceField`。
- 排名只代表证据完整度优先级，不代表唯一绝对用神结论。
- 报告必须保留并列策略和风险边界，禁止用单一用神覆盖全部策略。

## Verification

| Check | Result |
| --- | --- |
| `rg '调候|扶抑|通关|病药|用神' contracts/fate governance/tasks -n` | PASS |
| `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q` | `61 passed in 64.97s` |

## Gate

- PASS: 每个 strategy 都有 `basis`、`score`、`doesNotApplyWhen`。
- PASS: API contract 已断言真实输出中的 `scoredStrategies` 包含 `basis`、`scoreBasis`、`doesNotApplyWhen`。
- PASS: rule-depth regression 已断言 `scoreBasis` 因子可追溯到 evidence field。
