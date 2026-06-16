# FateCat 八字体系 100% Scorecard

更新时间：2026-06-16

## 口径

这里的 `100%` 指八字体系达到工程验收 100%，不是预测命中率 100%，也不是宣称命理判断绝对正确。

达成 100% 必须同时满足：

- 每个能力维度都有可追溯规则、数据、测试、报告输出和失败边界。
- 每个专业结论都有 `sourceRuleId`、`evidenceFields`、`riskBoundary` 和反证条件。
- MingLi-Bench 只作为样本外评测层，输出准确率和失败归因，不作为生产排盘真相源。
- 真实专家命例、人工标注或未授权材料缺失时，标为 HITL/WARN，不硬编数据补齐。

## 当前基线证据

| 证据项 | 当前值 | 获取方式 |
| --- | ---: | --- |
| 八字 rule-depth 规则 | 22 条 | `contracts/fate/rule_depth_registry.json` 中 `system=bazi` |
| 全部 rule-depth 规则 | 44 条 | `python3 -m json.tool contracts/fate/rule_depth_registry.json` |
| 八字 classics 规则索引 | 43 条 | `contracts/fate/classics_rule_index.json` 中 `system=bazi` |
| 全部 classics 规则索引 | 98 条 | `python3 -m json.tool contracts/fate/classics_rule_index.json` |
| 八字 coverage golden | 300 例 | `domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json` |
| 八字 rule-depth golden | 8 例 | `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json` |
| 八字 statement golden | 5 例 | `domains/fate-analysis/data-products/bazi/golden/statement_cases.json` |
| 八字 calendar boundary golden | 4 例 | `domains/fate-analysis/data-products/bazi/golden/calendar_boundary_cases.json` |
| MingLi-Bench 题量 | 160 题 | `tools/reference-repos/github/MingLi-Bench-main/data/data.json` |
| MingLi-Bench 年份 | 2022-2025 | `bash scripts/run-mingli-bench.sh --stats` |
| 本地 CI 入口 | quick/full/container/public-service/all | `bash scripts/local-ci.sh --help` |

## 完成度矩阵

| 维度 | 当前完成度 | 100% 完成标准 | Verify | Falsifier |
| --- | ---: | --- | --- | --- |
| 基础排盘 | 90% | 四柱、节气换月、立春年界、起运、真太阳时、早晚子时、跨时区边界均有 oracle 或 golden；失败样本可定位到 case。 | `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_golden_coverage_matrix.py -q` | 任一节气、立春、子时、真太阳时或起运边界样本无 expected/source/failureExplanation。 |
| 历法/时间边界 | 86% | `lunar-python` 为 production dependency；sxtwl/sxwnl/paipan/bazica 只作 oracle；差异口径有 tolerance 或 root cause。 | `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_fate_policy_assets.py -q` | oracle 进入生产主链，或 calendar 差异无法解释仍标绿。 |
| 证据化/可解释 | 82% | 核心八字输出包含 `analysisEvidence`、`baziRuleDepth`、`sourceRuleId`、权重、risk boundary；ruleIds 能回指 registry/classics。 | `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py tests/regression/test_api_contracts.py -q` | 报告出现未登记断语，或 ruleId 无法回指规则来源。 |
| 常规八字分析 | 78% | 日主强弱、月令、藏干、十神、五行、格局候选、喜忌策略、干支关系都有结构化字段和 golden。 | `.venv/bin/python -m pytest tests/regression/test_bazi_statement_golden.py tests/regression/test_bazi_ziwei_rule_depth.py -q` | 仍依赖不可追溯自然语言拼接，或核心字段缺失时测试仍通过。 |
| 高级格局 | 58% | 正格、变格、从格、假从、专旺、化气均有 appliesWhen、doesNotApplyWhen、破格条件、sourceRuleId、golden 正反例。 | `rg '从格|化气|专旺|假从|格局正变' contracts/fate -n && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q` | 高级格局没有条件链或 golden 反例，却被报告强断为 production。 |
| 合化成败 | 60% | 合象、可化、成化、破化、争合、阻隔、被冲破均有月令、透干、通根、得令、帮扶、冲破证据字段。 | `rg '合化|成化|破化|阻隔|争合' contracts/fate -n && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q` | 只展示“合”而不区分合而不化、成化、破化，或缺反例仍标 Done。 |
| 用神裁决 | 64% | 调候、扶抑、通关、病药并列评分；冲突裁决保留排序、理由和不适用条件，不用单一用神覆盖全部。 | `rg '调候|扶抑|通关|病药|用神' contracts/fate -n && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q` | 报告/API 只输出单一用神结论且丢失策略冲突。 |
| 岁运专题 | 55% | 大运、流年、流月、伏吟反吟、天克地冲、刑冲合害只作为趋势证据；事业、财运、婚姻、健康、学业、迁移、家庭有 profile evaluator。 | `rg '大运|流年|流月|伏吟|反吟|岁运' contracts/fate domains/fate-analysis/services/fate-core/src -n` | 输出确定未来、医疗/金融/法律/心理替代建议，或专题 profile 缺 evidence/riskBoundary。 |
| Golden/回归 | 80% | quick 只跑代表集；deep/release 跑 300+ shard；每个新增规则有正例、反例、边界例和 failureExplanation。 | `FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 FATECAT_GOLDEN_SHARD_INDEX=0 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q` | 全量 golden 慢测进入日常 quick，或失败 case 无法定位到规则/输入/期望。 |
| 样本外 benchmark | 42% | MingLi-Bench 160 题全量可生成 predictions、评分、分类准确率、错题 taxonomy；准确率只作为改进指标。 | `bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json` | 使用答案泄漏、人工改预测文件，或 sample 10 被当成最终专业能力。 |

## 目标门槛

| 阶段 | 必须达成 | 不允许宣称 |
| --- | --- | --- |
| P0 基础可验收 | 基础排盘、历法边界、证据化、常规八字、benchmark 链路均有本地命令。 | 不宣称专业推理已强。 |
| P0 专业规则可验收 | 高级格局、合化、用神、岁运专题都有 registry/evaluator/golden/report 边界。 | 不把候选规则写成确定断语。 |
| P1 样本外可追踪 | MingLi 全量 160 可跑，按分类输出准确率与失败归因。 | 不宣称 MingLi 命中率 100%。 |
| P1 长期可维护 | 新增规则进入 registry/evaluator/golden，不继续堆大函数。 | 不做大爆炸重写，不新增无消费者抽象。 |

## MingLi 分类优先级

| 分类 | 题量 | 推进策略 |
| --- | ---: | --- |
| 婚姻 | 44 | 优先补十神关系、配偶星、合冲刑害和风险边界。 |
| 事业 | 25 | 优先补官杀印食财格局、岁运触发和职业专题 profile。 |
| 家庭 | 22 | 优先补父母宫位类描述边界、十神家庭映射和报告风险边界。 |
| 健康 | 17 | 只做风险提示边界和结构压力证据，禁止医疗建议。 |
| 性格 | 14 | 作为低风险解释层，必须回指十神/五行/格局证据。 |
| 财运 | 13 | 只做趋势/结构证据，禁止金融建议。 |
| 学业 | 11 | 接入印星、食伤、岁运触发专题 profile。 |
| 子女 | 6 | 归入婚姻/家庭专题，保持低置信度边界。 |
| 外貌 | 3 | 不作为 P0 强断能力，仅保留 evidence_seed 或不支持。 |
| 运势 | 2 | 归入岁运触发 smoke，不单独宣称。 |
| 灾劫 | 2 | 高风险专题，只允许非确定风险边界。 |
| 官非 | 1 | 样本太少，只作失败归因标签。 |

## 执行映射

| Scorecard 维度 | 对应任务节点 |
| --- | --- |
| 基础排盘、历法/时间边界 | `TP-02.01`、`TP-02.02`、`TP-02.03` |
| 证据化/可解释、常规八字分析 | `TP-01.02`、`TP-08.01`、`TP-10.01` |
| 高级格局 | `TP-03.01`、`TP-03.02`、`TP-03.03` |
| 合化成败 | `TP-04.01`、`TP-04.02`、`TP-04.03` |
| 用神裁决 | `TP-05.01`、`TP-05.02`、`TP-05.03` |
| 岁运专题 | `TP-06.01`、`TP-06.02`、`TP-06.03` |
| Golden/回归、样本外 benchmark | `TP-07.01`、`TP-07.02`、`TP-07.03` |
| 长期维护性 | `TP-09.01`、`TP-09.02` |

## TP-00.02 Gate 判定

`TP-00.02` 完成条件：

- 10 个维度均有 current%、target evidence、verify command、falsifier。
- 明确 `100%` 是工程验收，不是预测绝对准确。
- MingLi 准确率目标为分阶段改进指标，不作为绝对完成宣称。

