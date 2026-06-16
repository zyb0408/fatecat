# TP-09.04 MingLi Failure Taxonomy

## 结论

- 状态：PASS。
- 来源：`/tmp/fatecat-mingli-full.json`，由 TP-09.02 full gate 生成。
- 评测规模：160 题，answered=160，correct=44，accuracy=27.50%。
- 目标：把失败按能力面回炉为规则 backlog，不按 `question_id`、标准答案或单题选项硬编码。

## 聚合失败面

| 主题 | 失败数 | 总数 | 当前准确率 | 优先级 |
| --- | ---: | ---: | ---: | --- |
| 婚姻 | 30 | 44 | 31.82% | P0 |
| 事业 | 17 | 25 | 32.00% | P0 |
| 家庭 | 16 | 22 | 27.27% | P0 |
| 健康 | 13 | 17 | 23.53% | P0 |
| 财运 | 12 | 13 | 7.69% | P0 |
| 性格 | 10 | 14 | 28.57% | P1 |
| 学业 | 9 | 11 | 18.18% | P1 |
| 子女 | 4 | 6 | 33.33% | P1 |
| 灾劫 | 2 | 2 | 0.00% | P0 high-risk |
| 运势 | 2 | 2 | 0.00% | P1 |
| 外貌 | 1 | 3 | 66.67% | P2 |
| 官非 | 0 | 1 | 100.00% | P2，样本太少 |

## Failure Classes

| Failure Class | Owner | 缺口类型 | 回炉方向 | 禁止路径 |
| --- | --- | --- | --- | --- |
| `FT-MARRIAGE-STRUCTURE` | topic.marriage | 婚姻/配偶星、夫妻宫、合冲刑害、岁运触发联合判断不足 | 扩展婚姻 profile 的配偶星强弱、夫妻宫关系、桃花/合冲、岁运触发矩阵；新增匿名 golden，不按题目答案调权重 | 禁止按 `ftb_*`、年份选项或 expected letter 硬编码；禁止输出离婚/丧偶确定断语 |
| `FT-WEALTH-EVENT` | topic.wealth | 财运对投资、破财、债务、得财事件的符号映射弱 | 建立财星、食伤生财、比劫夺财、库冲开闭、岁运财星触发的证据链；财运输出维持风险边界 | 禁止生成投资建议、破产断言或按选项关键词追答案 |
| `FT-CAREER-ROLE` | topic.career | 事业/官杀/印星/食伤与职业形态映射不足 | 把事业 profile 拆成职业稳定性、权责、组织类型、变动触发、官非边界；引入更多非答案 golden | 禁止用职业名词列表直接猜选项；禁止把官非样本扩展成现实法律判断 |
| `FT-FAMILY-KINSHIP` | topic.family | 六亲定位、父母宫、年月柱与亲缘事件映射不足 | 建立父母/兄弟/子女的十神定位和宫位证据，配合冲合刑害、岁运触发输出不确定性 | 禁止对亲人死亡、离异、贫富作确定恐吓式断语 |
| `FT-HEALTH-RISK` | topic.health | 健康/灾劫题命中差，且高风险话术边界严格 | 只做风险边界内的命理符号提示：五行偏枯、冲刑、忌神、岁运压力；新增 policy regression | 禁止疾病诊断、治疗建议、事故确定预言或恐吓文案 |
| `FT-EDUCATION-APTITUDE` | topic.education | 学业题样本少且 profile 粒度弱 | 建立印星、食伤、文昌/学堂、官印组合、岁运学习阶段的候选证据；先保持 beta | 禁止用学历结果反推规则；禁止宣称能决定考试/升学结果 |
| `FT-PERSONALITY-MAPPING` | topic.personality | 性格题容易退化为关键词匹配，缺少十神结构解释 | 基于十神结构、日主强弱、透干/藏干组合输出性格倾向证据和反证 | 禁止人格标签化、心理诊断或绝对化性格结论 |
| `FT-FORTUNE-TIMING` | fortune.dynamic | 运势/年份触发少样本但全错，动态时间定位不足 | 增强大运-流年-流月层级、伏吟反吟、天克地冲、合化破化触发的时间证据 | 禁止按选项年份距离 expected answer 调参；禁止确定未来事件 |
| `FT-OPTION-SCORER` | evaluation.baseline | 当前 MingLi baseline 是弱规则选项 scorer，不能代表报告推理能力 | 把 scorer 降级为 evaluation baseline；专业提升必须来自可解释 evaluator 与 golden，而不是 benchmark 选项文本技巧 | 禁止把选项关键词当生产规则；禁止把 accuracy 包装成专业能力 |
| `FT-BAZIQA-CANDIDATE` | evaluation.dataset | BaziQA license/schema 存疑，尚未接入失败评测 | 先完成许可证、schema、隐私、adapter quarantine；只允许 future_candidate/evaluation_only | 禁止 vendor 数据、禁止 runtime 接入、禁止 Celebrity50 进入公共报告 |

## Owner Queue

| Owner | Backlog | 验收方式 |
| --- | --- | --- |
| `topic.wealth` | `FT-WEALTH-EVENT` | 财星/库/比劫/岁运规则 registry + 匿名 golden + policy regression |
| `topic.marriage` | `FT-MARRIAGE-STRUCTURE`, `FT-FAMILY-KINSHIP` 子女部分 | 婚姻/子女 profile evidenceFields + 正反例 golden |
| `topic.career` | `FT-CAREER-ROLE`, `FT-PERSONALITY-MAPPING` 部分 | 事业 profile 分层 + 十神结构 trace |
| `topic.family` | `FT-FAMILY-KINSHIP` | 六亲定位 registry + 反证条件 |
| `topic.health` | `FT-HEALTH-RISK` | 高风险 policy regression 必须先过，再允许报告展示 |
| `topic.education` | `FT-EDUCATION-APTITUDE` | 学业 beta profile + golden，不升 production |
| `fortune.dynamic` | `FT-FORTUNE-TIMING` | 大运/流年触发 matrix + 时间边界 golden |
| `evaluation.baseline` | `FT-OPTION-SCORER` | baseline 只保留样本外比较；prediction 输出继续禁 gold 字段 |
| `evaluation.dataset` | `FT-BAZIQA-CANDIDATE` | license/source/schema 不清时保持 candidate_only |

## 禁止规则

- 禁止按 `question_id`、`case_id`、`original_number`、年份编号或文件顺序写规则。
- 禁止读取 `expected`、`answer`、`correct`、`gold`、`label` 参与 prediction 生成。
- 禁止把 benchmark 选项关键词直接提升为生产断语。
- 禁止为了提高 accuracy 输出医疗、金融、法律、心理、灾祸、死亡、离婚、破产等确定性判断。
- 禁止把 BaziQA 或 Celebrity50 接入 runtime。

## 下一步

`TP-10` 的实现只能从 owner queue 抽取可解释 evaluator 或 rule registry 切片；每个切片必须有：

- sourceRuleId
- evidenceFields
- 反证条件
- policy boundary
- 匿名 golden
- 不依赖 benchmark answer 的回归测试
