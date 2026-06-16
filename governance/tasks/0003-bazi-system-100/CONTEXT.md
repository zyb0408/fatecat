# Repo Evidence
- 仓库根：/home/lenovo/.projects/fatecat
- 当前任务索引：0001 Blocked，0002 In Progress，0003 本任务 Planning/In Progress
- 已有规则资产：contracts/fate/rule_depth_registry.json 44 条，contracts/fate/classics_rule_index.json 98 条
- 已有数据资产：coverage_matrix_cases.json 300+ synthetic golden，calendar_boundary_cases.json，rule_depth_cases.json，statement_cases.json
- 已有评测资产：MingLi-Bench 本地 160 题；scripts/generate-mingli-predictions.sh；fate_core.evaluation.mingli_baseline
- 已登记参考源：lunar-python production_dependency；sxtwl/sxwnl/paipan/bazica oracle_only；bazi-1 reference_only；MingLi-Bench evaluation_only

# Constraints Matrix
- 允许：修改 governance/tasks/0003-bazi-system-100/ 与 governance/tasks/INDEX.md；后续执行叶子可按节点声明修改 contracts、data-products、fate-core、tests、docs
- 禁止：破坏 checkpoint commit、执行破坏性 git 命令、伪造 benchmark 准确率、复制大段典籍原文、引入无许可生产依赖
- 依赖：lunar-python 主链；sxtwl/sxwnl/paipan/bazica 做 oracle；MingLi-Bench 做 evaluation；本地 CI quick/full/deep 分层验证
- HITL：若需要专家命例标注、真实命例授权或人工评审，必须标 Blocked/HITL，不得硬编数据

# Change Boundary
- 计划阶段只写任务容器；实现阶段每次只执行当前 ready 叶子节点
- 命理规则变化必须先进入 classics_rule_index 或 rule_depth_registry，再接 evaluator/report，最后补测试
- 任何报告断语必须保留 sourceRuleId、evidenceFields、riskBoundary 和 falsifier
- 高级格局、合化、用神、岁运专题不得直接写成不可反驳结论

# Risk Matrix
- P0：把 100% 误解为预测绝对准确，会导致产品口径失真
- P0：用无来源规则或无 license 文本扩写专业能力，会破坏治理和可信度
- P0：benchmark 使用答案泄漏，会污染样本外评估
- P1：继续堆核心大文件，会让规则体系不可维护
- P1：全量 golden 过慢，会拖垮日常 CI，需要 deep/release 分片
- P2：过早引入重型规则引擎，会增加所有权面而不提升准确率

# Assumptions and Falsification
- 假设：当前 76% 估算可作为计划基线，但必须由 SCORECARD.md 和实测命令重新固化
- 反证：若 full MingLi 评测低于随机基线或分类报告无法解释失败，则专题推理不能计入 100%
- 反证：若高级规则没有 appliesWhen/doesNotApplyWhen/golden 反例，则不能标 Done
- 反证：若 golden/oracle 不一致且无法解释，则必须转 DEBUG.md，不得继续加规则
- 反证：若本地 quick/full 失败，则最终 REVIEW/SHIP 不得通过

# Critical Ambiguities
- 真实专业命例授权与专家标注暂不可用；本任务先使用匿名 synthetic golden、MingLi-Bench 和公开典籍短规则索引
- MingLi 准确率目标需要分阶段设定：先超过弱 baseline，再按分类推进；不能承诺 100% 命中
- 典籍材料只允许短摘要和规则索引，不允许复制长段原文或商业断语模板

# Debug Evidence Contract
- 调试模式: Optional
- 任一 golden/oracle/MingLi/full pytest/local-ci 失败即转 Required
- DEBUG.md 必须记录失败样本、盘面输入、期望、实际、规则链、根因和回归命令

# Task Package Context Map
## TP-00
- 标题: 版本与基线控制面
- 目标: 在干净版本边界上建立八字 100% 的 scorecard 和当前缺口基线
- 有效叶子依赖: -
- 当前状态: In Progress

### TP-00.01
- 标题: 提交当前质量 hardening checkpoint
- 目标: 在设计新任务前提交现有大批改动，隔离后续八字 100% 计划
- 有效叶子依赖: 
- 当前状态: Done

### TP-00.02
- 标题: 建立八字 100% scorecard
- 目标: 把当前 10 个完成度维度固化为 SCORECARD，并定义每个维度达到 100% 的证据门槛
- 有效叶子依赖: TP-00.01
- 当前状态: Not Started

### TP-00.03
- 标题: 生成当前能力基线证据
- 目标: 用命令重新确认当前规则数、golden 数、MingLi 结果和本地 CI 状态，作为后续推进基线
- 有效叶子依赖: TP-00.02
- 当前状态: Not Started

## TP-01
- 标题: 材料与资源治理
- 目标: 明确哪些库、典籍、benchmark 和 oracle 用于补齐 100%，以及每类资源的生产边界
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-01.01
- 标题: 整理资源地图
- 目标: 把 lunar-python、sxtwl/sxwnl、paipan、bazica、bazi-1、MingLi-Bench、本地典籍映射到能力缺口
- 有效叶子依赖: TP-00.01, TP-00.02, TP-00.03
- 当前状态: Not Started

### TP-01.02
- 标题: 建立规则来源覆盖矩阵
- 目标: 把 98 条 classics rule 与 44 条 rule-depth 规则按高级格局、合化、用神、岁运专题分组
- 有效叶子依赖: TP-00.01, TP-00.02, TP-00.03, TP-01.01
- 当前状态: Not Started

## TP-02
- 标题: 基础排盘与时间边界 100%
- 目标: 把基础排盘从约 90% 推到可审计 100%，重点补节气、真太阳时、早晚子时、起运和跨时区边界
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-02.01
- 标题: 历法 oracle 覆盖审计
- 目标: 检查 lunar-python 主链与 sxtwl/sxwnl/paipan/bazica oracle 的覆盖范围和差异点
- 有效叶子依赖: TP-01.01, TP-01.02
- 当前状态: Not Started

### TP-02.02
- 标题: 扩展时间边界 golden
- 目标: 补充节气交界、立春年界、早晚子时、真太阳时、跨时区/DST、起运边界样本
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01
- 当前状态: Not Started

### TP-02.03
- 标题: 全量 golden deep gate 性能预算
- 目标: 把 300+ golden 从 36m 单块慢测治理成可分片、可定位、可预算的 deep gate
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.02
- 当前状态: Not Started

## TP-03
- 标题: 高级格局规则体系
- 目标: 把高级格局从约 58% 推到规则来源、条件链、反例和报告边界齐备
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-03.01
- 标题: 格局分类语法矩阵
- 目标: 定义正格、变格、从格、假从、专旺、化气的 appliesWhen/doesNotApplyWhen 条件和冲突优先级
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03
- 当前状态: Not Started

### TP-03.02
- 标题: 格局 evaluator 与候选成熟度
- 目标: 把特殊格局候选从保护层推进为可解释 evaluator，保持未满足条件时不强断
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.01
- 当前状态: Not Started

### TP-03.03
- 标题: 高级格局 golden 与反例
- 目标: 为每类高级格局补正例、反例、破格例、缺条件例 golden
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.02
- 当前状态: Not Started

## TP-04
- 标题: 合化成败引擎
- 目标: 把合化成败从约 60% 推到月令、透干、通根、得令、阻隔、帮扶、冲破条件链完整
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-04.01
- 标题: 合化条件链 registry
- 目标: 把合象、可化、成化、破化、争合、阻隔、被冲破写成规则条件和证据字段
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03
- 当前状态: Not Started

### TP-04.02
- 标题: 合化 evaluator 与优先级
- 目标: 实现合化状态评估，和三会三合六合冲刑害破优先级共存
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.01
- 当前状态: Not Started

### TP-04.03
- 标题: 合化 golden 反例集
- 目标: 补合而不化、得令成化、阻隔不化、冲破破化、争合降级等 golden
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.02
- 当前状态: Not Started

## TP-05
- 标题: 用神裁决体系
- 目标: 把用神裁决从约 64% 推到调候、扶抑、通关、病药并列策略和冲突裁决完整
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-05.01
- 标题: 用神策略评分矩阵
- 目标: 固化调候、扶抑、通关、病药的证据字段、权重、冲突策略和不适用条件
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03
- 当前状态: Not Started

### TP-05.02
- 标题: 用神冲突裁决 evaluator
- 目标: 把调候优先、扶抑校正、通关桥接、病药定位做成可解释排序和冲突原因输出
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.01
- 当前状态: Not Started

### TP-05.03
- 标题: 用神裁决 golden
- 目标: 补寒暖优先、身强身弱、五行偏枯、通关冲突、病药明显等用神 case
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.02
- 当前状态: Not Started

## TP-06
- 标题: 岁运与专题推理
- 目标: 把岁运专题从约 55% 推到事业、财运、婚姻、健康、学业、迁移、家庭均有规则证据和 benchmark 反馈
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-06.01
- 标题: 岁运触发规则矩阵
- 目标: 补大运、流年、流月、伏吟反吟、天克地冲、刑冲合害的动态触发规则
- 有效叶子依赖: TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03
- 当前状态: Not Started

### TP-06.02
- 标题: 专题 profile 推理器
- 目标: 为事业、财运、婚姻、健康、学业、迁移、家庭建立 topic profile evaluator 和风险边界
- 有效叶子依赖: TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01
- 当前状态: Not Started

### TP-06.03
- 标题: 专题报告边界
- 目标: 把健康、财富、婚恋等高风险专题的免责声明、非建议边界和证据可见性接入报告
- 有效叶子依赖: TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.02
- 当前状态: Not Started

## TP-07
- 标题: Benchmark 与样本外闭环
- 目标: 把样本外 benchmark 从约 42% 推到全量可评测、可归因、可回炉的工程闭环
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-07.01
- 标题: MingLi 全量 160 评测
- 目标: 生成全量 MingLi predictions，输出年度、分类、失败样本和准确率报告
- 有效叶子依赖: TP-06.01, TP-06.02, TP-06.03
- 当前状态: Not Started

### TP-07.02
- 标题: 失败样本归因和回炉队列
- 目标: 把 MingLi 错题按专题、缺规则、缺时间触发、缺格局、缺用神、问题歧义分类
- 有效叶子依赖: TP-06.01, TP-06.02, TP-06.03, TP-07.01
- 当前状态: Not Started

### TP-07.03
- 标题: Benchmark 门槛和回归策略
- 目标: 定义全量、sample、category smoke 的准确率门槛和提升节奏
- 有效叶子依赖: TP-06.01, TP-06.02, TP-06.03, TP-07.02
- 当前状态: Not Started

## TP-08
- 标题: 报告和 API 证据化 100%
- 目标: 确保 Web/API/Markdown 报告只展示可追溯结论，并能暴露必要证据和边界
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-08.01
- 标题: 报告字段契约
- 目标: 把高级格局、合化、用神、专题 profile 的输出字段纳入 API/Markdown/Web 合同
- 有效叶子依赖: TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03
- 当前状态: Not Started

### TP-08.02
- 标题: 风险话术和免责声明回归
- 目标: 确保健康、财富、婚恋、灾劫等专题不越界为现实建议
- 有效叶子依赖: TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01
- 当前状态: Not Started

## TP-09
- 标题: 长期维护性和模块边界
- 目标: 把八字规则体系从大文件堆叠推进到 registry/evaluator/golden/report 分层维护
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-09.01
- 标题: 大文件职责切片路线
- 目标: 为 bazi_calculator、calculate_pure_analysis、report_generator、bot、main 定义后续安全拆分顺序
- 有效叶子依赖: TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02
- 当前状态: Not Started

### TP-09.02
- 标题: 规则 evaluator 模块边界
- 目标: 定义 pattern/hehua/yongshen/fortune/topic evaluator 的模块边界和依赖方向
- 有效叶子依赖: TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02, TP-03.01, TP-04.01, TP-05.01, TP-06.01
- 当前状态: Not Started

## TP-10
- 标题: 最终审查和交付
- 目标: 汇总八字 100% 推进结果，区分 Done、WARN、Blocked，并生成最终交付证据
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-10.01
- 标题: 八字体系 100% 六维审查
- 目标: 按满足约束、可解释、可测试、可维护、处理特殊情况、复用建立在理解上审查八字体系
- 有效叶子依赖: TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02
- 当前状态: Not Started

### TP-10.02
- 标题: Closeout 和版本交付
- 目标: 生成 closeout，提交最终八字 100% 任务结果，并明确剩余 HITL/WARN
- 有效叶子依赖: TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02, TP-10.01
- 当前状态: Not Started
