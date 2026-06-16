# Task Overview
- Task ID: `0003`
- Slug: `bazi-system-100`
- Objective: `把 FateCat 八字体系从当前综合 76% 推进到基础排盘、专业规则、专题推理、样本外评测和报告证据均可验收的 100% 状态`
- Status: `Done`

## In Scope
- FateCat 八字体系从当前综合约 76% 推进到可审查、可验证、可维护的 100% 任务完成状态
- 覆盖基础排盘、历法时间边界、证据化、常规分析、高级格局、合化成败、用神裁决、岁运专题、golden/回归、样本外 benchmark
- 只用本地 CI/CD、本仓 contracts/data-products/tests/governance 证据和已登记参考源；不跑 GitHub Acceptance
- 输出任务树、材料资源图、执行波次、验收门槛和后续实现路径

## Out of Scope
- 不宣称命理预测绝对正确或 MingLi-Bench 命中率 100%
- 不把无 license 的参考仓库扩散为生产依赖
- 不在本计划阶段直接大规模重写 bazi_calculator.py
- 不把公共服务公网、Bot token、交易/金融系统能力纳入本任务
- 不引入重型规则引擎，除非 registry/evaluator 复杂度被实测证明需要

## Task Package Tree
- ROOT
  ├─ TP-00 [branch] [P0] 版本与基线控制面
  │  ├─ TP-00.01 [leaf] [P0] 提交当前质量 hardening checkpoint
  │  ├─ TP-00.02 [leaf] [P0] 建立八字 100% scorecard
  │  └─ TP-00.03 [leaf] [P0] 生成当前能力基线证据
  ├─ TP-01 [branch] [P0] 材料与资源治理
  │  ├─ TP-01.01 [leaf] [P0] 整理资源地图
  │  └─ TP-01.02 [leaf] [P0] 建立规则来源覆盖矩阵
  ├─ TP-02 [branch] [P0] 基础排盘与时间边界 100%
  │  ├─ TP-02.01 [leaf] [P0] 历法 oracle 覆盖审计
  │  ├─ TP-02.02 [leaf] [P0] 扩展时间边界 golden
  │  └─ TP-02.03 [leaf] [P1] 全量 golden deep gate 性能预算
  ├─ TP-03 [branch] [P0] 高级格局规则体系
  │  ├─ TP-03.01 [leaf] [P0] 格局分类语法矩阵
  │  ├─ TP-03.02 [leaf] [P0] 格局 evaluator 与候选成熟度
  │  └─ TP-03.03 [leaf] [P0] 高级格局 golden 与反例
  ├─ TP-04 [branch] [P0] 合化成败引擎
  │  ├─ TP-04.01 [leaf] [P0] 合化条件链 registry
  │  ├─ TP-04.02 [leaf] [P0] 合化 evaluator 与优先级
  │  └─ TP-04.03 [leaf] [P0] 合化 golden 反例集
  ├─ TP-05 [branch] [P0] 用神裁决体系
  │  ├─ TP-05.01 [leaf] [P0] 用神策略评分矩阵
  │  ├─ TP-05.02 [leaf] [P0] 用神冲突裁决 evaluator
  │  └─ TP-05.03 [leaf] [P0] 用神裁决 golden
  ├─ TP-06 [branch] [P0] 岁运与专题推理
  │  ├─ TP-06.01 [leaf] [P0] 岁运触发规则矩阵
  │  ├─ TP-06.02 [leaf] [P0] 专题 profile 推理器
  │  └─ TP-06.03 [leaf] [P1] 专题报告边界
  ├─ TP-07 [branch] [P0] Benchmark 与样本外闭环
  │  ├─ TP-07.01 [leaf] [P0] MingLi 全量 160 评测
  │  ├─ TP-07.02 [leaf] [P0] 失败样本归因和回炉队列
  │  └─ TP-07.03 [leaf] [P1] Benchmark 门槛和回归策略
  ├─ TP-08 [branch] [P1] 报告和 API 证据化 100%
  │  ├─ TP-08.01 [leaf] [P1] 报告字段契约
  │  └─ TP-08.02 [leaf] [P1] 风险话术和免责声明回归
  ├─ TP-09 [branch] [P1] 长期维护性和模块边界
  │  ├─ TP-09.01 [leaf] [P1] 大文件职责切片路线
  │  └─ TP-09.02 [leaf] [P1] 规则 evaluator 模块边界
  └─ TP-10 [branch] [P0] 最终审查和交付
     ├─ TP-10.01 [leaf] [P0] 八字体系 100% 六维审查
     └─ TP-10.02 [leaf] [P0] Closeout 和版本交付

## Requirement Alignment
- 用户要求：先提交控制版本，再设计八字体系推进到 100% 的落地计划
- 已完成版本控制：commit `1865e3d chore: checkpoint fatecat quality hardening`
- 当前基线：综合约 76%；基础排盘接近 90%，专业完整度约 65%，MingLi sample 10 accuracy 30%
- 本任务目标：把缺口从感性描述转成 TP-XX 任务树、资源使用策略、验收命令和 Done/Blocked 判定

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-00 | ROOT | 1 | P0 | package | No | - | - | No | No | 在干净版本边界上建立八字 100% 的 scorecard 和当前缺口基线 |
| TP-00.01 | TP-00 | 2 | P0 | action | Yes | - | 1 | No | No | 在设计新任务前提交现有大批改动，隔离后续八字 100% 计划 |
| TP-00.02 | TP-00 | 2 | P0 | action | Yes | TP-00.01 | 2 | Yes | No | 把当前 10 个完成度维度固化为 SCORECARD，并定义每个维度达到 100% 的证据门槛 |
| TP-00.03 | TP-00 | 2 | P0 | action | Yes | TP-00.02 | 3 | No | No | 用命令重新确认当前规则数、golden 数、MingLi 结果和本地 CI 状态，作为后续推进基线 |
| TP-01 | ROOT | 1 | P0 | package | No | TP-00.01, TP-00.02, TP-00.03 | - | No | No | 明确哪些库、典籍、benchmark 和 oracle 用于补齐 100%，以及每类资源的生产边界 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | TP-00.01, TP-00.02, TP-00.03 | 4 | No | Yes | 把 lunar-python、sxtwl/sxwnl、paipan、bazica、bazi-1、MingLi-Bench、本地典籍映射到能力缺口 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | TP-00.01, TP-00.02, TP-00.03, TP-01.01 | 5 | No | Yes | 把 98 条 classics rule 与 44 条 rule-depth 规则按高级格局、合化、用神、岁运专题分组 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01, TP-01.02 | - | No | No | 把基础排盘从约 90% 推到可审计 100%，重点补节气、真太阳时、早晚子时、起运和跨时区边界 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01, TP-01.02 | 6 | No | Yes | 检查 lunar-python 主链与 sxtwl/sxwnl/paipan/bazica oracle 的覆盖范围和差异点 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01 | 7 | No | No | 补充节气交界、立春年界、早晚子时、真太阳时、跨时区/DST、起运边界样本 |
| TP-02.03 | TP-02 | 2 | P1 | action | Yes | TP-01.01, TP-01.02, TP-02.02 | 8 | No | No | 把 300+ golden 从 36m 单块慢测治理成可分片、可定位、可预算的 deep gate |
| TP-03 | ROOT | 1 | P0 | package | No | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | - | No | No | 把高级格局从约 58% 推到规则来源、条件链、反例和报告边界齐备 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | 9 | No | No | 定义正格、变格、从格、假从、专旺、化气的 appliesWhen/doesNotApplyWhen 条件和冲突优先级 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.01 | 10 | No | No | 把特殊格局候选从保护层推进为可解释 evaluator，保持未满足条件时不强断 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.02 | 11 | No | No | 为每类高级格局补正例、反例、破格例、缺条件例 golden |
| TP-04 | ROOT | 1 | P0 | package | No | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | - | No | No | 把合化成败从约 60% 推到月令、透干、通根、得令、阻隔、帮扶、冲破条件链完整 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | 9 | No | No | 把合象、可化、成化、破化、争合、阻隔、被冲破写成规则条件和证据字段 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.01 | 10 | No | No | 实现合化状态评估，和三会三合六合冲刑害破优先级共存 |
| TP-04.03 | TP-04 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.02 | 11 | No | No | 补合而不化、得令成化、阻隔不化、冲破破化、争合降级等 golden |
| TP-05 | ROOT | 1 | P0 | package | No | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | - | No | No | 把用神裁决从约 64% 推到调候、扶抑、通关、病药并列策略和冲突裁决完整 |
| TP-05.01 | TP-05 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | 9 | No | No | 固化调候、扶抑、通关、病药的证据字段、权重、冲突策略和不适用条件 |
| TP-05.02 | TP-05 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.01 | 10 | No | No | 把调候优先、扶抑校正、通关桥接、病药定位做成可解释排序和冲突原因输出 |
| TP-05.03 | TP-05 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.02 | 11 | No | No | 补寒暖优先、身强身弱、五行偏枯、通关冲突、病药明显等用神 case |
| TP-06 | ROOT | 1 | P0 | package | No | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03 | - | No | No | 把岁运专题从约 55% 推到事业、财运、婚姻、健康、学业、迁移、家庭均有规则证据和 benchmark 反馈 |
| TP-06.01 | TP-06 | 2 | P0 | action | Yes | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03 | 12 | No | No | 补大运、流年、流月、伏吟反吟、天克地冲、刑冲合害的动态触发规则 |
| TP-06.02 | TP-06 | 2 | P0 | action | Yes | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01 | 13 | No | No | 为事业、财运、婚姻、健康、学业、迁移、家庭建立 topic profile evaluator 和风险边界 |
| TP-06.03 | TP-06 | 2 | P1 | action | Yes | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.02 | 14 | No | Yes | 把健康、财富、婚恋等高风险专题的免责声明、非建议边界和证据可见性接入报告 |
| TP-07 | ROOT | 1 | P0 | package | No | TP-06.01, TP-06.02, TP-06.03 | - | No | No | 把样本外 benchmark 从约 42% 推到全量可评测、可归因、可回炉的工程闭环 |
| TP-07.01 | TP-07 | 2 | P0 | action | Yes | TP-06.01, TP-06.02, TP-06.03 | 15 | No | No | 生成全量 MingLi predictions，输出年度、分类、失败样本和准确率报告 |
| TP-07.02 | TP-07 | 2 | P0 | action | Yes | TP-06.01, TP-06.02, TP-06.03, TP-07.01 | 16 | No | No | 把 MingLi 错题按专题、缺规则、缺时间触发、缺格局、缺用神、问题歧义分类 |
| TP-07.03 | TP-07 | 2 | P1 | action | Yes | TP-06.01, TP-06.02, TP-06.03, TP-07.02 | 17 | No | Yes | 定义全量、sample、category smoke 的准确率门槛和提升节奏 |
| TP-08 | ROOT | 1 | P1 | package | No | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03 | - | No | No | 确保 Web/API/Markdown 报告只展示可追溯结论，并能暴露必要证据和边界 |
| TP-08.01 | TP-08 | 2 | P1 | action | Yes | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03 | 18 | No | No | 把高级格局、合化、用神、专题 profile 的输出字段纳入 API/Markdown/Web 合同 |
| TP-08.02 | TP-08 | 2 | P1 | action | Yes | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01 | 19 | No | Yes | 确保健康、财富、婚恋、灾劫等专题不越界为现实建议 |
| TP-09 | ROOT | 1 | P1 | package | No | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02 | - | No | No | 把八字规则体系从大文件堆叠推进到 registry/evaluator/golden/report 分层维护 |
| TP-09.01 | TP-09 | 2 | P1 | action | Yes | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02 | 6 | No | Yes | 为 bazi_calculator、calculate_pure_analysis、report_generator、bot、main 定义后续安全拆分顺序 |
| TP-09.02 | TP-09 | 2 | P1 | action | Yes | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02, TP-03.01, TP-04.01, TP-05.01, TP-06.01 | 13 | No | No | 定义 pattern/hehua/yongshen/fortune/topic evaluator 的模块边界和依赖方向 |
| TP-10 | ROOT | 1 | P0 | package | No | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | - | No | No | 汇总八字 100% 推进结果，区分 Done、WARN、Blocked，并生成最终交付证据 |
| TP-10.01 | TP-10 | 2 | P0 | action | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | 20 | No | No | 按满足约束、可解释、可测试、可维护、处理特殊情况、复用建立在理解上审查八字体系 |
| TP-10.02 | TP-10 | 2 | P0 | action | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02, TP-10.01 | 21 | No | No | 生成 closeout，提交最终八字 100% 任务结果，并明确剩余 HITL/WARN |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
