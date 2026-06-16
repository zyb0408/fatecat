# TP-10.02 MingLi Failure Taxonomy

## Result

PASS.

MingLi full evaluation failures have been converted into a rule backlog without using question IDs, expected answers, option text or per-question tuning.

## Source Evidence

Input artifacts:

- `/tmp/fatecat-mingli-full.jsonl`
- `/tmp/fatecat-mingli-full.json`

Summary:

| Metric | Value |
| --- | ---: |
| total | 160 |
| answered | 160 |
| correct | 44 |
| accuracy | 27.50% |
| no-leak fields | 0 |

## By-Category Signal

| Category | Total | Correct | Accuracy | Backlog Class |
| --- | ---: | ---: | ---: | --- |
| 财运 | 13 | 1 | 7.69% | wealth-topic-evidence |
| 学业 | 11 | 2 | 18.18% | education-topic-evidence |
| 健康 | 17 | 4 | 23.53% | high-risk-health-boundary |
| 家庭 | 22 | 6 | 27.27% | family-topic-evidence |
| 性格 | 14 | 4 | 28.57% | personality-evidence |
| 事业 | 25 | 8 | 32.00% | career-topic-evidence |
| 婚姻 | 44 | 14 | 31.82% | marriage-topic-evidence |
| 子女 | 6 | 2 | 33.33% | children-topic-evidence |
| 运势 | 2 | 0 | 0.00% | fortune-dynamic-boundary |
| 灾劫 | 2 | 0 | 0.00% | high-risk-fear-boundary |
| 外貌 | 3 | 2 | 66.67% | non-p0-low-sample |
| 官非 | 1 | 1 | 100.00% | non-p0-low-sample |

## Failure Backlog

| Failure Class | Owner | Gap | 回炉方向 | 禁止路径 |
| --- | --- | --- | --- | --- |
| wealth-topic-evidence | `topic_profile.py` / `yongshen.py` | 财星、食伤、用神、岁运触发只是粗权重，缺少财运专题规则矩阵。 | 补财运 topic golden；增加财星/食伤/财官印组合的 evidence profile；保持金融建议禁区。 | 禁止按 question_id、选项或正确答案调权重。 |
| education-topic-evidence | `topic_profile.py` / `ten_god.py` | 印星、食伤、文昌等学业信号未形成专题冲突裁决。 | 补学业 topic golden；增加印食组合、寒暖燥湿和运限层级解释。 | 禁止用样本答案训练硬编码规则。 |
| high-risk-health-boundary | `topic_profile.py` / policy assets | 健康只能输出五行结构压力，不能追逐医疗式准确率。 | 只扩健康 risk wording golden 和非诊断证据；增加 forbidden terms regression。 | 禁止输出疾病、治疗、用药、诊断或现实医疗建议。 |
| family-topic-evidence | `topic_profile.py` / `relation.py` | 家庭 profile 对印星、比劫、合冲刑害的解释仍粗。 | 补家庭 topic golden；扩亲属结构 evidence fields 与冲合关系边界。 | 禁止输出家庭法律/心理处方。 |
| personality-evidence | future topic profile | 当前 P0 topic 未显式覆盖性格，MingLi 有性格分类。 | 决定是否晋升性格为 P1/P0；若晋升，先补 policy boundary 和 golden。 | 禁止将人格标签写成确定评价或心理诊断。 |
| career-topic-evidence | `topic_profile.py` / `advanced_pattern.py` | 事业 profile 对格局、官杀、印星、岁运联动仍粗。 | 补事业 topic golden；增加官印、食伤制杀、财官印组合 profile。 | 禁止替代职业、雇佣、法律决策。 |
| marriage-topic-evidence | `topic_profile.py` / policy assets | 婚姻题量大，当前只保留结构证据和边界，专题判断弱。 | 补婚姻 topic golden；强化夫妻宫、财官星、合冲刑害的非确定性裁决。 | 禁止输出必结婚、必离婚、第三者等确定断语。 |
| children-topic-evidence | future topic profile | 子女 topic 当前不是 P0 专题，样本少但准确率一般。 | 先列为 future_candidate；只有 license/source/golden 足够再晋升。 | 禁止输出生育、医学、现实家庭处方。 |
| fortune-dynamic-boundary | `fortune.py` | 运势类样本少且当前动态层只作趋势证据。 | 补岁运触发 golden；只增强触发链解释，不输出结果承诺。 | 禁止为了 accuracy 输出确定未来。 |
| high-risk-fear-boundary | policy assets | 灾劫类样本属于高风险恐吓边界。 | 保持 refusal/boundary 优先；只做风险词 regression。 | 禁止恐吓式灾断。 |
| non-p0-low-sample | benchmark adapter | 外貌、官非样本太少，不足以驱动 P0 规则。 | 暂不进入 production backlog；只保留评测观察。 | 禁止低样本过拟合。 |

## Gate

PASS: 每类 failure 都有 owner、缺口、回炉方向和禁止路径。

## Guardrail

This backlog is failure-driven but not answer-driven. It may guide rule/evidence work, but must not copy benchmark answers, options, question IDs or expected labels into production logic.
