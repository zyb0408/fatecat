# Bazi Capability 100% Research

更新时间：2026-06-17

## 结论

- 没有一个开源库能直接把专业八字体系一次性补到 100%。
- 成熟复用边界应保持不变：`lunar-python` 做生产历法底座；`sxtwl`、`sxwnl`、`bazica`、`paipan` 做离线 oracle；`MingLi-Bench` 和 `BaziQA` 做评测层；`bazi-1` 和其他项目只能做规则参考。
- 真正要补到 100% 的部分不是“换库”，而是 FateCat 自己的规则证据层、反证条件、golden corpus、样本外评测、专题 profile 和 evaluator 维护边界。
- `100%` 口径必须继续限定为工程与专业验收成熟度，不是预测命中率 100%，也不是确定未来。

## 外部主源调研

| 资源 | 主源 | 调研结论 | FateCat 用法 |
| --- | --- | --- | --- |
| `lunar-python` | https://github.com/6tail/lunar-python / https://pypi.org/project/lunar-python/ | 覆盖中国农历、节气、干支、八字相关基础能力，适合作生产 provider。 | `production_dependency`，升级必须走 calendar oracle、golden 和 local-ci。 |
| `sxtwl` | https://pypi.org/project/sxtwl/ | 适合节气、历法、四柱对照。 | `oracle_only`，禁止进入生产请求链路。 |
| `MingLi-Bench` | https://github.com/DestinyLinker/MingLi-Bench | 适合八字/紫微样本外评测和失败归因，不是排盘底座。 | `evaluation_only`，必须 no-leak，不按答案硬编码。 |
| `BaziQA` | https://github.com/ChenJiangxi/BaziQA | 远端 README 声称 MIT，但本地历史审查出现 license/schema 口径不一致风险。 | `future_candidate/evaluation_only`，先做 license/schema/admission，再考虑 gate。 |
| `bazica` | https://github.com/tommitoan/bazica | Go 实现，可做跨实现 oracle。 | `oracle_only`，不引入 Python runtime 主链。 |
| `bazi-calculator-by-alvamind` | https://github.com/alvamind/bazi-calculator-by-alvamind | TypeScript 基础分析结构可参考，不能补齐高级正宗八字。 | `reference_only`。 |

## 本仓库基线

来源：`governance/tasks/0004-bazi-professional-system-100/SCORECARD.md`、`FINAL_REVIEW.md`、`MINGLI_FAILURE_TAXONOMY.md`。

| 维度 | 当前完善度 | 到 100% 的真实缺口 |
| --- | ---: | --- |
| 基础排盘 | 93% | 边界样本和 oracle mismatch 还不足，尤其秒级节气、早晚子时、真太阳时、跨时区、起运。 |
| 历法 / 时间边界 | 90% | provider 升级合同、依赖锁、oracle 差异报告和边界 corpus 还要固化。 |
| 证据化 / 可解释 | 88% | 专业断语仍需强制 sourceRuleId、evidenceFields、riskBoundary、counterEvidence。 |
| 常规八字分析 | 84% | strength、ten-god、regular-pattern、relation evaluator 仍未完全物理拆分。 |
| 高级格局 | 72% | 从格、假从、专旺、化气、变格缺专家样本、正反例和 guarded lifecycle。 |
| 合化成败 | 76% | 月令、透干、通根、阻隔、帮扶、冲破等条件链还需状态机化。 |
| 用神裁决 | 78% | 调候、扶抑、通关、病药、格局用神之间需要稳定评分和冲突裁决。 |
| 岁运专题 | 70% | 婚姻、事业、财运、家庭、健康、学业等 profile 的联合评分弱。 |
| Golden / 回归 | 86% | deep shards 未全量固化为 release gate；高级规则、专题、反例 corpus 不足。 |
| 样本外 benchmark | 45% | MingLi 当前 27.50% accuracy，链路已通但推理弱；BaziQA 未准入。 |

## 100% 定义

| 维度 | 100% 不是 | 100% 是 |
| --- | --- | --- |
| 排盘/历法 | 单库结果永远正确 | 多 oracle/golden 覆盖边界，差异可解释，provider 可升级可回滚。 |
| 规则/解释 | 自然语言更像大师 | 每个结论有 ruleId、证据字段、反证条件、风险边界和测试。 |
| 高级断法 | 强行 production 化 | 有正例、反例、边界例；缺专家标注时保持 beta/HITL。 |
| 用神/岁运 | 输出确定事件 | 策略并列评分，动态触发只作趋势证据，禁止现实处方。 |
| benchmark | 准确率 100% | no-leak、可复现、分类归因、阈值提升和失败回炉机制成熟。 |

## 推荐目标阈值

| Gate | 最低目标 |
| --- | --- |
| Calendar boundary corpus | >= 50 个边界样本，覆盖节气秒级、立春、早晚子时、真太阳时、跨时区、起运。 |
| Rule-depth golden | >= 120 个结构化规则样本，覆盖常规、高级格局、合化、用神、岁运专题。 |
| Statement/policy golden | >= 80 个高风险输出样本，覆盖医疗、金融、法律、心理、灾祸、婚姻确定断语。 |
| Topic profile golden | 每个 P0 专题 >= 20 个匿名样本，包含正例、反例、边界例。 |
| MingLi full gate | answered=160/160，no-leak；overall accuracy 阶段目标先到 >= 40%，再到 >= 50%；低样本主题不单独吹指标。 |
| BaziQA gate | license/schema/admission 全通过后才允许进入 evaluation release gate；否则保持 candidate。 |
| Deep release gate | shard `0..3` 全量通过；quick 只跑代表集。 |

## 禁止路径

- 禁止按 `question_id`、选项、答案、gold label 或文件顺序刷 benchmark。
- 禁止把 BaziQA、MingLi 或公开题库样本进入生产请求链路。
- 禁止没有正反例和反证条件就把高级格局升为 production。
- 禁止为了提高 benchmark 输出医疗、金融、法律、心理或确定未来断语。
- 禁止继续把新规则堆进 delivery 或单一大函数。
