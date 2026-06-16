# Task Overview
- Task ID: `0002`
- Slug: `quality-completion-to-100`
- Objective: `把 FateCat 当前质量完善度从本地可用状态推进到本地工程 100%、八字专业能力 100%、公共生产 HITL 100% 的可审查交付状态`
- Status: `In Progress`

## In Scope
- 本地开发可用性、企业结构、本地 CI/CD、八字基础、八字专业、公共生产、长期维护性七个维度推进到可审查 100% 状态
- 只使用本地 CI/CD 工具链和本仓库任务树证据，不跑 GitHub Acceptance
- 真实公网生产验收作为 HITL 节点独立阻塞，不伪造成本地通过

## Out of Scope
- 不新增旧路径 fallback、兼容盒、双轨旧流程
- 不把缺少真实 URL/token 的公网验收标为通过
- 不把命理专业能力做成无来源、无证据、不可反驳的文案扩写
- 不引入重前端或偏离现有 FateCat Web 页面设计

## Task Package Tree
- ROOT
  ├─ TP-00 [branch] [P0] 任务控制面修正
  │  ├─ TP-00.01 [leaf] [P0] 修正 0001 索引状态
  │  └─ TP-00.02 [leaf] [P0] 创建 0002 任务树
  ├─ TP-01 [branch] [P0] 本地开发可用性 100%
  │  ├─ TP-01.01 [leaf] [P0] 固化一键本地开发入口
  │  ├─ TP-01.02 [leaf] [P1] 补齐本地恢复路径
  │  └─ TP-01.03 [leaf] [P0] 本地开发 smoke 验收
  ├─ TP-02 [branch] [P0] 企业仓库结构 100%
  │  ├─ TP-02.01 [leaf] [P0] 结构与目录门禁复核
  │  ├─ TP-02.02 [leaf] [P1] catalog 与治理索引新鲜度
  │  └─ TP-02.03 [leaf] [P0] 企业结构最终验收
  ├─ TP-03 [branch] [P0] 本地 CI/CD 100%
  │  ├─ TP-03.01 [leaf] [P0] 本地 CI profile 目录化
  │  ├─ TP-03.02 [leaf] [P1] 供应链与制品证据
  │  └─ TP-03.03 [leaf] [P0] 本地 CI/CD 全链路验收
  ├─ TP-04 [branch] [P0] 八字基础能力 100%
  │  ├─ TP-04.01 [leaf] [P0] 扩展 golden matrix 到 300+
  │  ├─ TP-04.02 [leaf] [P1] 历法 oracle 对照增强
  │  └─ TP-04.03 [leaf] [P0] 基础能力证据覆盖验收
  ├─ TP-05 [branch] [P0] 八字专业完整度 100%
  │  ├─ TP-05.01 [leaf] [P0] 高级格局 registry
  │  ├─ TP-05.02 [leaf] [P0] 合化成败引擎
  │  ├─ TP-05.03 [leaf] [P0] 用神裁决引擎
  │  ├─ TP-05.04 [leaf] [P1] 岁运专题 profile
  │  └─ TP-05.05 [leaf] [P0] 专业 benchmark 与报告验收
  ├─ TP-06 [branch] [P0] 公共生产稳定性 100%
  │  ├─ TP-06.01 [leaf] [P0] 生产等价配置复核
  │  ├─ TP-06.02 [leaf] [P1] 多副本限流与边缘防护方案
  │  ├─ TP-06.03 [leaf] [P1] 观测与错误定位增强
  │  └─ TP-06.04 [leaf] [P0] 真实公网 API 与 Bot live 验收
  ├─ TP-07 [branch] [P0] 长期维护性 100%
  │  ├─ TP-07.01 [leaf] [P0] 拆分 bazi kernel 子模块
  │  ├─ TP-07.02 [leaf] [P1] 收敛 delivery 大文件
  │  ├─ TP-07.03 [leaf] [P1] 兼容面 burn-down
  │  └─ TP-07.04 [leaf] [P0] 长期维护性最终验收
  └─ TP-08 [branch] [P0] 最终审查与交付
     ├─ TP-08.01 [leaf] [P0] 全仓本地质量审查
     ├─ TP-08.02 [leaf] [P0] 处理最终 findings
     └─ TP-08.03 [leaf] [P0] 生成 closeout

## Requirement Alignment
- 最终目标：FateCat 从当前本地可用状态推进到本地工程 100%、八字专业能力 100%、公共生产 HITL 100% 的可审查交付状态
- 当前事实：0001 已完成大量本地工程任务，仍因 TP-02.03 缺真实公网 URL 和真实 Bot token 阻塞最终 closeout
- 本任务承接剩余增量，不覆盖 0001，不伪造外部生产证据

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-00 | ROOT | 1 | P0 | package | No | - | - | No | No | 修正任务索引、状态和下一阶段任务容器，确保任务真相源可继续执行 |
| TP-00.01 | TP-00 | 2 | P0 | action | Yes | - | 1 | No | No | 让 governance/tasks/INDEX.md 与 0001 STATUS.md 的 Blocked 状态一致 |
| TP-00.02 | TP-00 | 2 | P0 | action | Yes | TP-00.01 | 2 | No | No | 创建并回填 0002 任务容器，承接剩余 100% 推进工作 |
| TP-01 | ROOT | 1 | P0 | package | No | TP-00.01, TP-00.02 | - | No | No | 把本地开发体验从可用提升到可复制、可恢复、可验证的 100% 状态 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | TP-00.01, TP-00.02 | 3 | No | Yes | 确认并文档化 API/Web/Bot dry-run、本地环境启动和常见开发命令 |
| TP-01.02 | TP-01 | 2 | P1 | action | Yes | TP-00.01, TP-00.02 | 3 | No | Yes | 补齐 venv 重建、缓存清理、runtime 清理、失败恢复的最小 runbook |
| TP-01.03 | TP-01 | 2 | P0 | action | Yes | TP-00.01, TP-00.02, TP-01.01, TP-01.02 | 4 | No | No | 用 quick profile 和 delivery smoke 证明本地开发链路可用 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-00.01, TP-00.02 | - | No | No | 确保 canonical roots、catalog、governance、contracts 和防回潮门禁达到企业仓库结构 100% |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-00.01, TP-00.02 | 3 | No | Yes | 复核 canonical roots、旧路径禁用、compat ledger 和目录 AGENTS.md 状态 |
| TP-02.02 | TP-02 | 2 | P1 | action | Yes | TP-00.01, TP-00.02 | 3 | No | Yes | 确认 catalog、governance INDEX、migration ledger、tech-debt evidence 与当前结构一致 |
| TP-02.03 | TP-02 | 2 | P0 | action | Yes | TP-00.01, TP-00.02, TP-02.01, TP-02.02 | 4 | No | No | 用结构、源码卫生、导出卫生和任务文档校验证明企业仓库结构 100% |
| TP-03 | ROOT | 1 | P0 | package | No | TP-00.01, TP-00.02 | - | No | No | 把本地 quick/full/export/docker/container/public-service 形成可重复发布门禁 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-00.01, TP-00.02 | 3 | No | Yes | 确认 local-ci 各 profile 的职责、输出证据和失败处理方式清晰 |
| TP-03.02 | TP-03 | 2 | P1 | action | Yes | TP-00.01, TP-00.02 | 3 | No | Yes | 补齐依赖来源、vendor health、容器 image、export runtime 的本地证据路径 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-00.01, TP-00.02, TP-03.01, TP-03.02 | 4 | No | No | 复跑 all profile，形成本地 CI/CD 100% 最新证据 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-00.01, TP-00.02 | - | No | No | 把四柱、节气、真太阳时、起运、证据层、golden/oracle 覆盖推进到基础 100% |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-00.01, TP-00.02 | 3 | No | No | 在现有 120 样本基础上扩展到 300+，覆盖节气、子时、真太阳时、起运、地域时区、边界反例 |
| TP-04.02 | TP-04 | 2 | P1 | action | Yes | TP-00.01, TP-00.02 | 3 | No | Yes | 增强 lunar-python 主链与 sxtwl/oracle 开发门禁对照，确保 oracle 不污染生产路径 |
| TP-04.03 | TP-04 | 2 | P0 | action | Yes | TP-00.01, TP-00.02, TP-04.01, TP-04.02 | 4 | No | No | 确认四柱、节气、起运、五行、十神、神煞等基础判断均有 ruleId/source/riskBoundary |
| TP-05 | ROOT | 1 | P0 | package | No | TP-04.01, TP-04.02, TP-04.03 | - | No | No | 补齐高级格局、合化成败、用神裁决、岁运专题和专业 benchmark |
| TP-05.01 | TP-05 | 2 | P0 | action | Yes | TP-04.01, TP-04.02, TP-04.03 | 5 | Yes | No | 建立正格、变格、从格、专旺、化气、假从的规则 registry 与反例条件 |
| TP-05.02 | TP-05 | 2 | P0 | action | Yes | TP-04.01, TP-04.02, TP-04.03, TP-05.01 | 6 | No | No | 实现合化成败条件链：月令、透干、通根、得令、阻隔、帮扶、冲破 |
| TP-05.03 | TP-05 | 2 | P0 | action | Yes | TP-04.01, TP-04.02, TP-04.03, TP-05.01 | 6 | No | No | 把调候、扶抑、通关、病药做成并列策略评分与冲突裁决 |
| TP-05.04 | TP-05 | 2 | P1 | action | Yes | TP-04.01, TP-04.02, TP-04.03, TP-05.01 | 6 | No | Yes | 补齐财、官、婚、健康、迁移、事业等岁运专题 profile 的规则证据和风险边界 |
| TP-05.05 | TP-05 | 2 | P0 | action | Yes | TP-04.01, TP-04.02, TP-04.03, TP-05.02, TP-05.03, TP-05.04 | 7 | No | No | 用 MingLi-Bench、本仓 golden 和报告回归验证专业完整度 |
| TP-06 | ROOT | 1 | P0 | package | No | TP-03.01, TP-03.02, TP-03.03 | - | No | No | 补齐本地生产等价配置、观测、限流和真实公网 live 验收 |
| TP-06.01 | TP-06 | 2 | P0 | action | Yes | TP-03.01, TP-03.02, TP-03.03 | 5 | Yes | Yes | 确认 CORS allowlist、trusted proxy、HSTS、edge body limit、timeouts 和生产 env 示例完整 |
| TP-06.02 | TP-06 | 2 | P1 | action | Yes | TP-03.01, TP-03.02, TP-03.03 | 5 | Yes | Yes | 把单进程内存限流的边界、Redis/网关/WAF 升级路径和 body limit 策略写入运行合同 |
| TP-06.03 | TP-06 | 2 | P1 | action | Yes | TP-03.01, TP-03.02, TP-03.03 | 5 | Yes | Yes | 补齐 p95/p99 histogram、错误分类、requestId 贯穿、运行 runbook 的验收证据 |
| TP-06.04 | TP-06 | 2 | P0 | action | Yes | TP-03.01, TP-03.02, TP-03.03, TP-06.01, TP-06.02, TP-06.03 | 6 | No | No | 在真实 HTTPS URL、TLS/反代、真实 FATE_BOT_TOKEN 可用后完成公共生产 100% 验收 |
| TP-07 | ROOT | 1 | P0 | package | No | TP-04.01, TP-04.02, TP-04.03 | - | No | No | 继续拆核心大文件，收缩 delivery 职责，清退无契约兼容面 |
| TP-07.01 | TP-07 | 2 | P0 | action | Yes | TP-04.01, TP-04.02, TP-04.03 | 5 | Yes | No | 把 fate_core.kernel.bazi_calculator 按 calendar、pillars、strength、relations、spirits、patterns、yongshen、fortune 逐步拆边界 |
| TP-07.02 | TP-07 | 2 | P1 | action | Yes | TP-04.01, TP-04.02, TP-04.03 | 5 | Yes | No | 收敛 main.py、bot.py、report/web_ui 的职责边界，确保 delivery 只做编排、渲染、传输、观测防护 |
| TP-07.03 | TP-07 | 2 | P1 | action | Yes | TP-04.01, TP-04.02, TP-04.03 | 5 | Yes | Yes | 审计 remaining adapter/shim/wrapper，删除无真实外部契约的兼容面，保留项必须有 owner 和移除条件 |
| TP-07.04 | TP-07 | 2 | P0 | action | Yes | TP-04.01, TP-04.02, TP-04.03, TP-07.01, TP-07.02, TP-07.03 | 6 | No | No | 用模块边界、测试、review 和 local-ci 证明长期维护性达到 100% |
| TP-08 | ROOT | 1 | P0 | package | No | TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04 | - | No | No | 汇总本地 100%、八字 100%、公网 HITL 状态，形成最终可交付版本 |
| TP-08.01 | TP-08 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04 | 8 | No | No | 执行 correctness/security/reliability/performance/architecture/operability/repo-hygiene 审查 |
| TP-08.02 | TP-08 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04, TP-08.01 | 9 | No | No | 处理 TP-08.01 中发现的 BLOCK 和影响 100% gate 的 WARN |
| TP-08.03 | TP-08 | 2 | P0 | action | Yes | TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04, TP-08.02 | 10 | No | No | 生成任务 closeout，明确 Done、Blocked、Skipped、Unknown 和最终百分比 |

## Reading Order
1. README.md
2. CONTEXT.md
3. SYSTEMIC_IMPROVEMENT_PLAN.md
4. PLAN.md
5. ACCEPTANCE.md
6. ACCEPTANCE_CHECKLIST.md
7. TODO.md
8. STATUS.md

## Systemic Improvement Plan V2

`SYSTEMIC_IMPROVEMENT_PLAN.md` 是 2026-06-16 基于六个质量标准审计追加的系统性完善计划：

- 满足约束
- 可解释
- 可测试
- 可维护
- 处理特殊情况
- 复用建立在理解上

该文件当前是 v2 覆盖层，不覆盖旧 `TREE_SPEC.json`。进入执行前，应将其中 `TP-09` 至 `TP-15` 编译进正式任务树或作为执行波次逐项回填 `STATUS.md`。
