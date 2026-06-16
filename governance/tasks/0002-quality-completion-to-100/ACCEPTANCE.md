# Task-Level Acceptance
- 七个质量维度都有明确叶子任务、依赖、Verify、Gate 和输出物
- 本地可执行节点全部完成后，local-ci all 和任务文档校验必须通过
- 公共生产 HITL 节点只在真实 URL/token 验收通过后 Done
- 任何 100% 结论必须引用命令、测试、文档或外部 live smoke 证据

# Validation Plan
- 每个叶子节点完成后立即更新 STATUS.md Recent Evidence
- 本地工程节点至少运行对应 pytest/ruff/mypy/local-ci/structure/gov 校验
- 八字能力节点必须运行 golden/oracle/evidence/policy 测试
- 生产节点必须运行 local public-service profile；真实公网节点必须运行 production-readiness --api-url <real-url> --require-live-bot
- 最终节点必须运行 validate_task_docs.py --phase closeout 或记录阻塞原因

# Review Gate
- auto-review lens：correctness、security、reliability、performance、architecture、operability、repo-hygiene
- future-optimal-drift：禁止把 legacy/compat 作为目标结构
- ponytail-complexity：禁止新增无存在理由的配置、抽象、文件、依赖和流程
- feature-change-safety：覆盖 API、Bot、限流、外部 token、生产配置和运行副作用

# Runtime Verification Gate
- [ ] Runtime tool/action 结果、审批状态、compaction/resume 状态和 verifier 结论均可复核

# Ship Readiness
- 本地工程 100%：local-ci all PASS、任务文档 decompose/closeout 校验 PASS、review 无 BLOCK
- 八字专业 100%：高级规则、合化、用神、岁运专题均有 source/ruleId/riskBoundary 和 golden/benchmark 证据
- 公共生产 100%：真实公网 production-readiness + live Bot PASS
- 如果 HITL 缺输入，最终交付状态只能是本地 100% + 公网 HITL Blocked

# Task Package Acceptance
## TP-00
- 验收: `任务控制面修正` 达到其 objective，且依赖关系保持一致

### TP-00.01
- 验收: `修正 0001 索引状态` 达到其 objective，且依赖关系保持一致

### TP-00.02
- 验收: `创建 0002 任务树` 达到其 objective，且依赖关系保持一致

## TP-01
- 验收: `本地开发可用性 100%` 达到其 objective，且依赖关系保持一致

### TP-01.01
- 验收: `固化一键本地开发入口` 达到其 objective，且依赖关系保持一致

### TP-01.02
- 验收: `补齐本地恢复路径` 达到其 objective，且依赖关系保持一致

### TP-01.03
- 验收: `本地开发 smoke 验收` 达到其 objective，且依赖关系保持一致

## TP-02
- 验收: `企业仓库结构 100%` 达到其 objective，且依赖关系保持一致

### TP-02.01
- 验收: `结构与目录门禁复核` 达到其 objective，且依赖关系保持一致

### TP-02.02
- 验收: `catalog 与治理索引新鲜度` 达到其 objective，且依赖关系保持一致

### TP-02.03
- 验收: `企业结构最终验收` 达到其 objective，且依赖关系保持一致

## TP-03
- 验收: `本地 CI/CD 100%` 达到其 objective，且依赖关系保持一致

### TP-03.01
- 验收: `本地 CI profile 目录化` 达到其 objective，且依赖关系保持一致

### TP-03.02
- 验收: `供应链与制品证据` 达到其 objective，且依赖关系保持一致

### TP-03.03
- 验收: `本地 CI/CD 全链路验收` 达到其 objective，且依赖关系保持一致

## TP-04
- 验收: `八字基础能力 100%` 达到其 objective，且依赖关系保持一致

### TP-04.01
- 验收: `扩展 golden matrix 到 300+` 达到其 objective，且依赖关系保持一致

### TP-04.02
- 验收: `历法 oracle 对照增强` 达到其 objective，且依赖关系保持一致

### TP-04.03
- 验收: `基础能力证据覆盖验收` 达到其 objective，且依赖关系保持一致

## TP-05
- 验收: `八字专业完整度 100%` 达到其 objective，且依赖关系保持一致

### TP-05.01
- 验收: `高级格局 registry` 达到其 objective，且依赖关系保持一致

### TP-05.02
- 验收: `合化成败引擎` 达到其 objective，且依赖关系保持一致

### TP-05.03
- 验收: `用神裁决引擎` 达到其 objective，且依赖关系保持一致

### TP-05.04
- 验收: `岁运专题 profile` 达到其 objective，且依赖关系保持一致

### TP-05.05
- 验收: `专业 benchmark 与报告验收` 达到其 objective，且依赖关系保持一致

## TP-06
- 验收: `公共生产稳定性 100%` 达到其 objective，且依赖关系保持一致

### TP-06.01
- 验收: `生产等价配置复核` 达到其 objective，且依赖关系保持一致

### TP-06.02
- 验收: `多副本限流与边缘防护方案` 达到其 objective，且依赖关系保持一致

### TP-06.03
- 验收: `观测与错误定位增强` 达到其 objective，且依赖关系保持一致

### TP-06.04
- 验收: `真实公网 API 与 Bot live 验收` 达到其 objective，且依赖关系保持一致

## TP-07
- 验收: `长期维护性 100%` 达到其 objective，且依赖关系保持一致

### TP-07.01
- 验收: `拆分 bazi kernel 子模块` 达到其 objective，且依赖关系保持一致

### TP-07.02
- 验收: `收敛 delivery 大文件` 达到其 objective，且依赖关系保持一致

### TP-07.03
- 验收: `兼容面 burn-down` 达到其 objective，且依赖关系保持一致

### TP-07.04
- 验收: `长期维护性最终验收` 达到其 objective，且依赖关系保持一致

## TP-08
- 验收: `最终审查与交付` 达到其 objective，且依赖关系保持一致

### TP-08.01
- 验收: `全仓本地质量审查` 达到其 objective，且依赖关系保持一致

### TP-08.02
- 验收: `处理最终 findings` 达到其 objective，且依赖关系保持一致

### TP-08.03
- 验收: `生成 closeout` 达到其 objective，且依赖关系保持一致

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
