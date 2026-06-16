# 岁运触发矩阵

## Scope

- Task: `TP-08.01`
- Objective: 建立大运、流年、流月、伏吟、反吟、岁运并临、天克地冲的动态触发矩阵。
- Runtime owner: `fate-core`
- Implementation file: `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- Contract source: `contracts/fate/rule_depth_registry.json`
- Output path: `data.baziBenchmark.fortuneTriggerMatrix`

## Runtime Contract

| Field | Meaning |
| --- | --- |
| `layerOrder` | 原局、大运、流年、流月的动态层级顺序 |
| `triggerTypeCounts` | 从 `fortuneTriggers` 聚合出的触发类型计数 |
| `matrix` | registry triggerMatrix 映射后的 runtime status |
| `conflictPolicy` | 原局优先，大运定阶段，流年定触发，流月只细化窗口 |
| `riskBoundary` | 只作趋势证据，不输出确定未来或高风险建议 |

## Trigger Types

| Type | Runtime Status Meaning |
| --- | --- |
| `major_stage` | 大运字段可用时为阶段背景，不直接断事件。 |
| `annual_trigger` | 流年字段和触发链可用时说明结构被引动。 |
| `monthly_refinement` | 流月只在有大运或流年背景时细化窗口。 |
| `fu_yin` | 动态干支与原局或大运干支相同，仅作重复引动证据。 |
| `fan_yin` | 动态干支形成反向关系，仅提示结构冲突增强。 |
| `sui_yun_bing_lin` | 流年与当前大运干支相同，仅作层级重叠证据。 |
| `tian_ke_di_chong` | 天干相克且地支相冲，不得包装成恐吓式断语。 |

## Verification

| Check | Result |
| --- | --- |
| `rg '大运|流年|流月|伏吟|反吟|天克地冲|fortuneTriggers' contracts domains/fate-analysis -n` | PASS |
| `.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py` | PASS |
| `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q` | `61 passed in 64.77s` |

## Gate

- PASS: 动态触发只作为趋势证据。
- PASS: `monthly_refinement` 明确只细化窗口，不反向覆盖大运流年。
- PASS: API contract 和 rule-depth regression 均覆盖 `fortuneTriggerMatrix`。
- PASS: 风险边界禁止确定未来、恐吓表述和高风险决策建议。
