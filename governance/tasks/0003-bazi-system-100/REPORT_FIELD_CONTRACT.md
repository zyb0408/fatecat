# Report Field Contract

## 目标

把高级格局、合化、用神、岁运触发、专题 profile 的输出字段固定为可追溯合同，避免报告层出现未登记断语。

## API 合同

| 字段 | 来源 | 必需子字段 | 边界 |
| --- | --- | --- | --- |
| `baziBenchmark.patternRegistry.specialPatternCandidates` | fate-core evaluator | `schemaVersion`, `candidates`, `riskBoundary` | 高级格局只登记 candidate/guarded/not_supported，不直接定格 |
| `baziBenchmark.combineTransformMatrix` | fate-core evaluator | `schemaVersion`, `stateCatalog`, `candidates`, `riskBoundary` | 合化区分 structural_relation、transform_candidate、transform_success、transform_broken |
| `baziBenchmark.yongShenDecision` | fate-core evaluator | `primaryStrategy`, `scoredStrategies`, `conflictPolicy`, `riskBoundary` | 调候、扶抑、通关、病药并列保留，不用单一用神覆盖全部 |
| `baziBenchmark.fortuneTriggers` | fate-core evaluator | `year`, `ganZhi`, `triggerTypes`, `reasons`, `riskBoundary` | 动态层只作趋势触发证据 |
| `baziBenchmark.topicProfiles` | fate-core evaluator | `topic`, `score`, `basis`, `scoreBasis`, `evidenceFields`, `riskBoundary`, `lifecycle` | 专题 profile 是结构化证据入口，不输出高风险建议 |
| `baziRuleDepth.combinationStatements` | rule-depth renderer | `topic`, `statement`, `ruleIds`, `evidence`, `confidence`, `riskBoundary` | 组合断语必须回指 ruleIds 和 riskBoundary |
| `analysisEvidence.items.baziBenchmark` | evidence builder | `ruleIds`, `evidenceFields`, `riskBoundary` | evidence 默认机器可读，不直接变成 Markdown 断语 |

## Markdown 合同

- 标准 Markdown 由 `report_generator.generate_full_report(report_system)` 服务端生成。
- `topicProfiles` 不进入默认 Markdown 主体；默认 Markdown 只输出标准排盘报告和已登记规则深度摘要。
- 高风险专题不得输出医疗、金融、法律、心理替代建议。
- 任何新增 Markdown 段落必须先在 `contracts/fate/rule_depth_registry.json` 或对应 contract 中登记 ruleId、evidenceFields 和 riskBoundary。

## Web 合同

- `/web` 核心 Markdown 由服务端直接写入 `<pre><code id="report-markdown">`。
- 工作台只展示后端结构化字段，不定义命理规则。
- 页面说明与元信息默认折叠。
- 八字工作台的专题 profile / 风险边界以 `<details>` 折叠块展示。
- 复制 Markdown 内容不受工作台影响。

## 验收命令

```bash
.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py -q
```
