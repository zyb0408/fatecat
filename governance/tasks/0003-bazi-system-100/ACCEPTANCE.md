# Task-Level Acceptance
- 10 个能力维度都有 scorecard、规则/数据/测试/报告/benchmark 对应节点
- 每个叶子节点有 Verify、Gate、输出物和 Done/Blocked 判定
- 计划完成后 `validate_task_docs.py --phase decompose` 通过
- 执行完成后基础排盘、专业规则、专题推理、样本外 benchmark 和报告证据均有本地可重复命令
- 最终可声明的是八字体系工程验收 100%，不是预测命中率 100%

# Validation Plan
- 计划阶段：apply_task_tree + validate_task_docs --phase decompose + git diff --check
- 基础阶段：calendar/oracle/golden regression + full golden shard deep gate
- 规则阶段：json schema、rule registry、policy assets、rule-depth tests
- 专题阶段：MingLi full 160 predictions + by-category evaluation + failure taxonomy
- 报告阶段：API/Web/Markdown 输出 evidence/riskBoundary 回归
- 最终阶段：local-ci quick/full，active principle gate，auto-review 六维审查

# Review Gate
- correctness：四柱、节气、起运、规则条件和 benchmark 不能答案泄漏
- reliability：deep golden 可分片，失败样本可定位
- maintainability：新增规则进入 registry/evaluator，不继续堆大函数
- architecture：evaluation 不反向进入 production kernel；oracle 不进入主链
- security/compliance：license、隐私、免责声明、非医疗/金融/法律建议边界必须保留
- future-optimal：目标是规则证据系统，不是短期关键词 baseline
- ponytail：新增对象必须有当前消费者、验证命令和删除/升级条件

# Runtime Verification Gate
- [ ] Runtime tool/action 结果、审批状态、compaction/resume 状态和 verifier 结论均可复核

# Ship Readiness
- Planning Done：0003 任务树通过 decompose 校验，checkpoint commit 后工作树只含 0003 计划改动
- Build Done：所有 P0/P1 叶子 Done，P2 可有明确 backlog
- Evidence Done：SCORECARD、RESOURCE_MAP、MingLi full report、golden shard report、rule registry diff、报告证据测试齐备
- Review Done：无 active BLOCK；WARN 有 owner 和后续任务
- Ship Done：本地 quick/full PASS；deep gates 有可复现证据或明确耗时预算

# Task Package Acceptance
## TP-00
- 验收: `版本与基线控制面` 达到其 objective，且依赖关系保持一致

### TP-00.01
- 验收: `提交当前质量 hardening checkpoint` 达到其 objective，且依赖关系保持一致

### TP-00.02
- 验收: `建立八字 100% scorecard` 达到其 objective，且依赖关系保持一致

### TP-00.03
- 验收: `生成当前能力基线证据` 达到其 objective，且依赖关系保持一致

## TP-01
- 验收: `材料与资源治理` 达到其 objective，且依赖关系保持一致

### TP-01.01
- 验收: `整理资源地图` 达到其 objective，且依赖关系保持一致

### TP-01.02
- 验收: `建立规则来源覆盖矩阵` 达到其 objective，且依赖关系保持一致

## TP-02
- 验收: `基础排盘与时间边界 100%` 达到其 objective，且依赖关系保持一致

### TP-02.01
- 验收: `历法 oracle 覆盖审计` 达到其 objective，且依赖关系保持一致

### TP-02.02
- 验收: `扩展时间边界 golden` 达到其 objective，且依赖关系保持一致

### TP-02.03
- 验收: `全量 golden deep gate 性能预算` 达到其 objective，且依赖关系保持一致

## TP-03
- 验收: `高级格局规则体系` 达到其 objective，且依赖关系保持一致

### TP-03.01
- 验收: `格局分类语法矩阵` 达到其 objective，且依赖关系保持一致

### TP-03.02
- 验收: `格局 evaluator 与候选成熟度` 达到其 objective，且依赖关系保持一致

### TP-03.03
- 验收: `高级格局 golden 与反例` 达到其 objective，且依赖关系保持一致

## TP-04
- 验收: `合化成败引擎` 达到其 objective，且依赖关系保持一致

### TP-04.01
- 验收: `合化条件链 registry` 达到其 objective，且依赖关系保持一致

### TP-04.02
- 验收: `合化 evaluator 与优先级` 达到其 objective，且依赖关系保持一致

### TP-04.03
- 验收: `合化 golden 反例集` 达到其 objective，且依赖关系保持一致

## TP-05
- 验收: `用神裁决体系` 达到其 objective，且依赖关系保持一致

### TP-05.01
- 验收: `用神策略评分矩阵` 达到其 objective，且依赖关系保持一致

### TP-05.02
- 验收: `用神冲突裁决 evaluator` 达到其 objective，且依赖关系保持一致

### TP-05.03
- 验收: `用神裁决 golden` 达到其 objective，且依赖关系保持一致

## TP-06
- 验收: `岁运与专题推理` 达到其 objective，且依赖关系保持一致

### TP-06.01
- 验收: `岁运触发规则矩阵` 达到其 objective，且依赖关系保持一致

### TP-06.02
- 验收: `专题 profile 推理器` 达到其 objective，且依赖关系保持一致

### TP-06.03
- 验收: `专题报告边界` 达到其 objective，且依赖关系保持一致

## TP-07
- 验收: `Benchmark 与样本外闭环` 达到其 objective，且依赖关系保持一致

### TP-07.01
- 验收: `MingLi 全量 160 评测` 达到其 objective，且依赖关系保持一致

### TP-07.02
- 验收: `失败样本归因和回炉队列` 达到其 objective，且依赖关系保持一致

### TP-07.03
- 验收: `Benchmark 门槛和回归策略` 达到其 objective，且依赖关系保持一致

## TP-08
- 验收: `报告和 API 证据化 100%` 达到其 objective，且依赖关系保持一致

### TP-08.01
- 验收: `报告字段契约` 达到其 objective，且依赖关系保持一致

### TP-08.02
- 验收: `风险话术和免责声明回归` 达到其 objective，且依赖关系保持一致

## TP-09
- 验收: `长期维护性和模块边界` 达到其 objective，且依赖关系保持一致

### TP-09.01
- 验收: `大文件职责切片路线` 达到其 objective，且依赖关系保持一致

### TP-09.02
- 验收: `规则 evaluator 模块边界` 达到其 objective，且依赖关系保持一致

## TP-10
- 验收: `最终审查和交付` 达到其 objective，且依赖关系保持一致

### TP-10.01
- 验收: `八字体系 100% 六维审查` 达到其 objective，且依赖关系保持一致

### TP-10.02
- 验收: `Closeout 和版本交付` 达到其 objective，且依赖关系保持一致

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
