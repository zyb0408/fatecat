# MingLi Failure Taxonomy

## 结论

- 日期：2026-06-16
- 输入评测：`/tmp/fatecat-mingli-full.json`
- total：160
- correct：45
- failures：115
- accuracy：28.12%
- 结论：失败主要不是排盘基础问题，而是专题推理、时间触发联合裁决、格局/用神参与度和题目语义映射不足。

## 禁止动作

- 不得把 MingLi expected answer 写回 `mingli_baseline.py`、生产规则或 prompt。
- 不得按 `question_id` 做硬编码。
- 不得把低准确率包装成专业能力已完成。
- 允许把失败样本作为 owner 能力面的回炉队列和 regression taxonomy。

## 失败样本队列

| 分类 | failures | question_ids |
| --- | ---: | --- |
| 婚姻 | 30 | ftb_0002, ftb_0007, ftb_0018, ftb_0022, ftb_0026, ftb_0034, ftb_0037, ftb_0044, ftb_0048, ftb_0051, ftb_0054, ftb_0058, ftb_0063, ftb_0074, ftb_0076, ftb_0077, ftb_0083, ftb_0087, ftb_0092, ftb_0098, ftb_0101, ftb_0102, ftb_0106, ftb_0108, ftb_0112, ftb_0125, ftb_0129, ftb_0134, ftb_0143, ftb_0153 |
| 事业 | 16 | ftb_0014, ftb_0039, ftb_0042, ftb_0055, ftb_0059, ftb_0061, ftb_0062, ftb_0068, ftb_0075, ftb_0078, ftb_0088, ftb_0103, ftb_0115, ftb_0123, ftb_0141, ftb_0149 |
| 家庭 | 16 | ftb_0010, ftb_0020, ftb_0024, ftb_0032, ftb_0036, ftb_0043, ftb_0047, ftb_0081, ftb_0089, ftb_0117, ftb_0130, ftb_0131, ftb_0135, ftb_0136, ftb_0144, ftb_0151 |
| 健康 | 13 | ftb_0003, ftb_0005, ftb_0038, ftb_0045, ftb_0060, ftb_0070, ftb_0105, ftb_0113, ftb_0116, ftb_0126, ftb_0140, ftb_0150, ftb_0159 |
| 财运 | 12 | ftb_0028, ftb_0030, ftb_0053, ftb_0067, ftb_0069, ftb_0080, ftb_0090, ftb_0095, ftb_0104, ftb_0109, ftb_0120, ftb_0128 |
| 性格 | 10 | ftb_0015, ftb_0031, ftb_0056, ftb_0079, ftb_0127, ftb_0132, ftb_0145, ftb_0146, ftb_0147, ftb_0160 |
| 学业 | 9 | ftb_0027, ftb_0057, ftb_0072, ftb_0082, ftb_0111, ftb_0133, ftb_0142, ftb_0152, ftb_0156 |
| 子女 | 4 | ftb_0052, ftb_0064, ftb_0065, ftb_0114 |
| 灾劫 | 2 | ftb_0094, ftb_0137 |
| 运势 | 2 | ftb_0091, ftb_0158 |
| 外貌 | 1 | ftb_0009 |

## Owner 能力面

| owner 能力面 | 失败分类 | 缺口类型 | 回炉方向 | 禁止路径 |
| --- | --- | --- | --- | --- |
| `bazi.topic.marriage_profile` | 婚姻、子女 | 缺规则、缺时间触发、缺格局、缺用神 | 配偶星、夫妻宫、合冲刑害、岁运触发和性别语义联合评分 | 按婚姻题答案硬编码 |
| `bazi.topic.career_profile` | 事业、官非、性格 | 缺规则、缺格局、缺用神 | 官杀、印星、食伤、格局候选、岁运触发和职业语义映射 | 用职业关键词替代盘面证据 |
| `bazi.topic.family_profile` | 家庭、子女 | 缺规则、缺时间触发 | 印星、比劫、父母/家庭结构、刑冲合害与岁运层级 | 把家庭题并入婚姻强断 |
| `bazi.topic.health_boundary` | 健康、灾劫、外貌 | 缺规则、缺时间触发 | 五行偏枯、寒暖燥湿、风险边界、外貌/健康题语义拆分 | 输出诊疗、恐吓或现实处方 |
| `bazi.topic.wealth_profile` | 财运 | 缺规则、缺时间触发、缺用神 | 财星、食伤、用神策略、岁运触发和风险边界联合评分 | 输出金融决策或投资结论 |
| `bazi.topic.study_profile` | 学业 | 缺规则、缺用神 | 印星、食伤、文昌类辅助证据和阶段运势联动 | 用单一印星数量下结论 |
| `bazi.topic.fortune_timing` | 运势、灾劫 | 缺时间触发 | 大运、流年、流月、伏吟反吟、天克地冲和原局关系联合裁决 | 把动态层写成确定未来 |
| `bazi.topic.personality_appearance` | 性格、外貌 | 缺规则 | 性格/外貌目前只是 alias，需要独立 lifecycle 或降级为 unsupported | 混入事业/健康 profile 后宣称已覆盖 |

## 回炉优先级

| 优先级 | 动作 | 依据 |
| --- | --- | --- |
| P0 | 婚姻 profile 联合评分 | 失败 30，题量最大，当前错题最多 |
| P0 | 财运 profile 重做风险边界和评分 | accuracy 0.0769，说明当前财星/食伤/用神映射弱 |
| P0 | 家庭 profile 拆父母/子女/家庭结构 | 失败 16，且子女类被粗略映射到婚姻 |
| P1 | 学业 profile 补印食和阶段运势 | accuracy 0.1818 |
| P1 | 健康/灾劫/外貌只做边界化证据 | 高风险专题，不追求强断 |
| P1 | 性格/外貌新增 lifecycle 或 unsupported | 当前 alias 容易制造假覆盖 |

## 验收方式

- `MINGLI_FULL_EVALUATION.md` 保留全量总分和分类分数。
- 本文件保留失败样本 owner、缺口类型和回炉队列。
- 后续 TP 不得直接改 predictions 答案；只能改可解释规则、topic profile、时间触发或评测策略。
- 任一改动后必须重跑 full MingLi 或至少标明 sample 不能代表最终能力。
