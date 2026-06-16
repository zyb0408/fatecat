# FateCat 八字体系 100% 资源地图

更新时间：2026-06-16

## 资源使用原则

- 生产主链只允许使用已声明依赖、许可证明确、测试覆盖明确的资源。
- oracle 只用于测试、对照和差异解释，不进入请求链路。
- reference_only 只用于规则材料、结构参考或人工整理，不复制大段源码/原文，不作为生产依赖扩散。
- evaluation_only 只用于离线 benchmark，不参与生产排盘，不调用默认多模型 API runner。
- future_candidate 需要单独架构、license、验收和 release gate 后才能升级。

## 核心资源表

| 资源 | usageRole | license boundary | productionUseAllowed | 可补能力 | 禁止用途 |
| --- | --- | --- | --- | --- | --- |
| `lunar-python` | `production_dependency` | MIT，`licenseStatus=spdx`，`tools/reference-repos/github/lunar-python-master/LICENSE` | true | 四柱、节气、干支、生肖、八字、五行、十神、大运、基础历法。 | 禁止绕过包依赖直接依赖 vendor 快照；禁止把 oracle 差异直接改成生产真相。 |
| `bazi-1` | `reference_only` | `licenseStatus=missing_upstream_license`，无独立 LICENSE，`distributionAllowed=false`，需人工审计。 | false | 金不换、调候、神煞、格局、干支关系、十神规则材料。 | 禁止作为生产依赖；禁止复制大段原文或商业断语模板；禁止无 sourceRuleId 进入报告。 |
| `sxwnl` | `oracle_only` | `licenseStatus=missing_upstream_license`，无独立 LICENSE，`distributionAllowed=false`，需人工审计。 | false | 节气、历法、四柱离线对照，尤其用于 calendar oracle contract。 | 禁止进入主生产链；禁止作为用户请求路径依赖；禁止绕过 license 风险。 |
| `paipan` | `oracle_only` | WTFPL-2.0，`licenseStatus=spdx`，`tools/reference-repos/github/paipan-master/LICENSE` | false | 真太阳时、早晚子时、排盘口径对照。 | 禁止直接替换生产时间管线；上线前必须有 adapter 测试和口径说明。 |
| `bazica` | `oracle_only` | MIT，`licenseStatus=spdx`，`tools/reference-repos/github/bazica-master/LICENSE` | false | Go 八字排盘交叉校验、四柱/大运 oracle。 | 禁止引入 Python 主链；禁止为了参考引入跨语言运行时所有权。 |
| `bazi-calculator-by-alvamind` | `reference_only` | MIT 字段来自 package.json，本地无独立 LICENSE；`auditRequired=true`。 | false | TypeScript 基础分析结构、输入输出组织参考。 | 禁止作为生产依赖；禁止无审计复制实现；禁止用它补高级专业断法。 |
| `MingLi-Bench` | `evaluation_only` | MIT，`licenseStatus=spdx`，`tools/reference-repos/github/MingLi-Bench-main/LICENSE` | false | 160 题样本外 benchmark、分类准确率、失败样本归因、prompt/predictions 离线评分。 | 禁止进入请求链路；禁止默认调用多模型 API runner；禁止答案泄漏；禁止把 sample 命中率当专业完成度。 |
| `dantalion` | `future_candidate` | MIT，`licenseStatus=spdx`，`tools/reference-repos/github/dantalion-master/LICENSE` | false | 现代占卜/娱乐化候选材料。 | 当前不用于正宗八字补齐主线；禁止进入默认报告。 |
| `iztro` | `future_candidate` | MIT，`licenseStatus=spdx`，`tools/reference-repos/github/iztro-main/LICENSE` | false | 紫微生产候选，不属于八字 100% 主线。 | 禁止混入默认综合八字 Markdown；紫微需独立 capability 和验收。 |

## 能力缺口到资源映射

| 能力缺口 | 主资源 | 辅助资源 | 交付形态 |
| --- | --- | --- | --- |
| 基础排盘 | `lunar-python` | `sxwnl`、`bazica` | production provider + oracle contract + golden。 |
| 节气/立春/起运 | `lunar-python` | `sxwnl`、`paipan` | calendar boundary golden + tolerance/failureExplanation。 |
| 真太阳时/早晚子时 | 当前项目 adapter | `paipan` | adapter 测试 + boundary golden + 口径说明。 |
| 日主强弱 | `lunar-python` + 本仓 evaluator | `bazi-1` | rule_depth_registry + golden。 |
| 常规格局 | 本仓 evaluator | `bazi-1`、`bazi-calculator-by-alvamind` | classics_rule_index + rule_depth_registry + report evidence。 |
| 高级格局 | 本仓 evaluator | `bazi-1` | appliesWhen/doesNotApplyWhen + 正反例 golden。 |
| 合化成败 | 本仓 evaluator | `bazi-1`、`paipan` | condition chain + transform status + golden 反例。 |
| 用神裁决 | 本仓 evaluator | `bazi-1` | 调候/扶抑/通关/病药 strategy matrix。 |
| 岁运专题 | `lunar-python` 运势字段 + 本仓 evaluator | `MingLi-Bench` | dynamic trigger matrix + topic profile + benchmark feedback。 |
| 样本外评测 | `MingLi-Bench` | 本仓 scored baseline | predictions JSONL + report JSON + failure taxonomy。 |

## 升级与禁止升级条件

| 资源 | 可升级条件 | 禁止升级条件 |
| --- | --- | --- |
| `lunar-python` | 上游版本升级通过 calendar oracle、solar terms golden、bazi golden 和 local-ci quick/full。 | 上游 API 变化未验证，或 vendor 快照与包依赖口径不一致。 |
| `bazi-1` | 只能把短规则摘要和来源转成本仓 registry 条件；license 风险解除前不得升级为生产依赖。 | 缺上游 LICENSE、规则来源不可追踪、需要复制大段原文。 |
| `sxwnl` | 只能增强 oracle 对照；若要生产化，必须先完成 license、adapter、性能、回归和替换策略。 | 缺 license 或对照差异无法解释。 |
| `paipan` | 真太阳时/早晚子时 adapter 有独立测试、口径文档和 golden 对照。 | 未说明口径差异就替换当前时间管线。 |
| `bazica` | 只在 oracle 层扩展样本；如进入主链必须有跨语言运行策略和维护成本审查。 | 为了快速补功能引入 Go 运行时到 Python 请求链路。 |
| `MingLi-Bench` | 用于评测门槛、分类失败队列和 regression policy。 | 用答案训练或硬编码预测；把 benchmark 数据当用户样例。 |

## TP-01.01 Gate 判定

`TP-01.01` 完成条件：

- 每个资源都有 `usageRole`。
- 每个资源都有 license boundary。
- 每个资源都有可补能力。
- 每个资源都有禁止用途。
- 明确 `lunar-python` 是主生产底座，`MingLi-Bench` 是 `evaluation_only`，`sxwnl`/`paipan`/`bazica` 是 `oracle_only`，`bazi-1`/`bazi-calculator-by-alvamind` 是 `reference_only`。

