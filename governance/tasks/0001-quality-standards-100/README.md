# Task Overview
- Task ID: `0001`
- Slug: `quality-standards-100`
- Objective: `把 FateCat 项目质量标准从当前 72% 推进到可审查、可验证、可维护、可生产运行的 100% 状态`
- Status: `In Progress`

## In Scope
- 修复当前阻塞级质量门禁：ruff format、本地 local-ci、REVIEW.md 过期、production-readiness 配置失败。
- 把六项质量标准分别推进到可验证 100%：满足约束、可解释、可测试、可维护、处理特殊情况、复用建立在理解上。
- 补齐公共生产服务稳定性所需的配置、限流、边界输入、Bot 背压、观测和外部验收任务。
- 把八字证据层、golden case、规则索引和复用边界继续推进到专业命理项目可审查状态。
- 把长期维护债拆成可执行重构切片，逐步从 delivery legacy 大类迁移到 fate-core 的稳定边界。

## Out of Scope
- 本计划阶段不直接修改业务代码；业务实现由后续执行波次逐叶子任务完成。
- 不运行 GitHub Acceptance，不把远端 CI 当作本地计划设计前置条件。
- 不伪造公网生产结果；真实域名、TLS、Bot token、生产 URL 缺失时必须标记为 HITL 阻塞。
- 不以追求行数为目标做大爆炸重写；重构必须保持行为和 golden case 可验证。

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 修复当前本地质量阻塞
  │  ├─ TP-01.01 [leaf] [P0] 修复 ruff format gate
  │  ├─ TP-01.02 [leaf] [P0] 刷新 REVIEW.md 质量真相源
  │  └─ TP-01.03 [leaf] [P0] 恢复 local-ci quick 绿色
  ├─ TP-02 [branch] [P0] 关闭生产准入约束缺口
  │  ├─ TP-02.01 [leaf] [P0] 固化生产 env 合同
  │  ├─ TP-02.02 [leaf] [P0] 恢复 local-ci public-service 绿色
  │  └─ TP-02.03 [leaf] [P0] 真实公网 API 与 Bot live 验收
  ├─ TP-03 [branch] [P0] 补齐特殊情况与韧性
  │  ├─ TP-03.01 [leaf] [P0] 定义并测试出生时间时区语义
  │  ├─ TP-03.02 [leaf] [P0] Bot 背压与滥用保护
  │  ├─ TP-03.03 [leaf] [P0] API guardrails 特殊输入回归
  │  └─ TP-03.04 [leaf] [P1] 历法边界 golden 扩展
  ├─ TP-04 [branch] [P1] 八字解释性与证据化补齐
  │  ├─ TP-04.01 [leaf] [P1] 核心字段 evidence 覆盖审计
  │  ├─ TP-04.02 [leaf] [P1] 八字 golden case 扩展到 100+
  │  ├─ TP-04.03 [leaf] [P1] 专题 profile 评分验证
  │  └─ TP-04.04 [leaf] [P2] MingLi-Bench 评测门禁接入
  ├─ TP-05 [branch] [P1] 长期维护性与 legacy 边界治理
  │  ├─ TP-05.01 [leaf] [P1] 绘制核心大文件职责边界图
  │  ├─ TP-05.02 [leaf] [P1] 拆分 calculate_pure_analysis 证据构建模块
  │  ├─ TP-05.03 [leaf] [P1] 迁移 BaziCalculator 领域核心到 fate-core
  │  ├─ TP-05.04 [leaf] [P1] 收敛 delivery 层 API/Web/Bot/报告边界
  │  └─ TP-05.05 [leaf] [P1] 清退无真实外部契约的 legacy/compat shim
  ├─ TP-06 [branch] [P1] 复用与供应链理解闭环
  │  ├─ TP-06.01 [leaf] [P1] CalendarProvider 生产依赖合同
  │  ├─ TP-06.02 [leaf] [P1] 参考源许可和用途 manifest
  │  ├─ TP-06.03 [leaf] [P2] 历法/四柱 oracle 对照框架
  │  └─ TP-06.04 [leaf] [P1] 规则 registry owner 和扩展规则
  ├─ TP-07 [branch] [P1] 公共服务观测和运行闭环
  │  ├─ TP-07.01 [leaf] [P1] Prometheus/Grafana 指标和告警计划
  │  ├─ TP-07.02 [leaf] [P1] 请求 ID 与业务日志贯穿
  │  ├─ TP-07.03 [leaf] [P1] SLO 与运维 runbook
  │  └─ TP-07.04 [leaf] [P0] 本地全链路 CI/CD 汇总
  └─ TP-08 [branch] [P0] 最终审查和交付收口
     ├─ TP-08.01 [leaf] [P0] 执行全仓质量审查
     ├─ TP-08.02 [leaf] [P0] 处理最终 review findings
     └─ TP-08.03 [leaf] [P0] 生成任务 closeout 和交付证据

## Requirement Alignment
- 目标: 把 FateCat 项目质量标准从当前 72% 推进到可审查、可验证、可维护、可生产运行的 100% 状态。
- approved plan 顶层步骤数: 8
- 编译后节点总数: 38
- 编译后叶子节点数: 30
- 对齐项: 用户要求使用 auto-tasks 设计完整计划，把当前质量标准百分比全部推进到 100%。
- 对齐项: 当前基线综合质量约 72%；本计划把百分比拆成可验证 gate，而不是继续使用主观评分。
- 对齐项: 本计划是任务容器和执行波次设计，不直接等同于已完成实现。
- 计划摘要: 以 gate-first 方式推进：先修当前本地阻塞，再补生产准入，再扩测试和边界，再推进八字解释与维护性，最后用 full review 和 ship gate 收口。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 先把当前已知 BLOCK 清零，恢复本地 CI 可信度。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 格式化当前失败文件，让 ruff format --check 全仓通过。 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | Yes | 把 REVIEW.md 更新到当前 HEAD、当前测试数量、当前 production-readiness 真实状态。 |
| TP-01.03 | TP-01 | 2 | P0 | action | Yes | TP-01.01, TP-01.02 | 3 | No | No | 用本地 CI 快速入口证明基础质量门禁闭合。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.03 | - | No | No | 让公共服务发布前的静态和真实环境门禁可执行、可失败、可追溯。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.03 | 4 | No | Yes | 把 CORS、records、rate limit backend、edge body limit、proxy headers、HSTS 的生产配置要求写成可验证合同。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-01.03, TP-02.01 | 5 | No | No | 使用 scripts/local-ci.sh --profile public-service 验证生产静态准入路径。 |
| TP-02.03 | TP-02 | 2 | P0 | action | Yes | TP-01.03, TP-02.02 | 6 | No | No | 在真实域名/TLS/反向代理/生产 URL/真实 Bot token 下执行 live readiness。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-01.03 | - | No | Yes | 把时区、真太阳时、节气、早晚子时、Bot 背压、多副本限流和异常输入变成测试化契约。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-01.03 | 4 | No | Yes | 明确 naive、Z、+08:00、出生地时区和真太阳时之间的输入语义。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-01.03 | 4 | No | Yes | 把 Bot 队列从近似无限等待改成有界并发、有界队列、用户级反馈和测试。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-01.03 | 4 | No | Yes | 补齐请求体超限、无 Content-Length、超时、429、错误分类、安全头的回归测试。 |
| TP-03.04 | TP-03 | 2 | P1 | action | Yes | TP-01.03, TP-03.01 | 5 | No | Yes | 扩展节气边界、早晚子时、真太阳时、地域经纬度边界 golden case。 |
| TP-04 | ROOT | 1 | P1 | package | No | TP-01.03 | - | No | Yes | 让核心命理判断具备可追溯 evidence、ruleIds、权重和风险边界。 |
| TP-04.01 | TP-04 | 2 | P1 | action | Yes | TP-01.03 | 4 | No | Yes | 审计 baziBenchmark、baziRuleDepth、analysisEvidence 的核心字段覆盖率。 |
| TP-04.02 | TP-04 | 2 | P1 | action | Yes | TP-01.03, TP-03.04, TP-04.01 | 6 | No | No | 优先覆盖节气边界、早晚子时、特殊格局、合化、从格、岁运触发。 |
| TP-04.03 | TP-04 | 2 | P1 | action | Yes | TP-01.03, TP-04.01 | 5 | No | Yes | 验证事业、财运、婚姻、健康、学业、迁移 profile 不输出确定性断语。 |
| TP-04.04 | TP-04 | 2 | P2 | action | Yes | TP-01.03 | 4 | No | Yes | 把 MingLi-Bench 作为报告/推理质量评测层，不作为生产排盘层。 |
| TP-05 | ROOT | 1 | P1 | package | No | TP-01.03 | - | No | No | 从大文件和 delivery legacy 中迁出领域核心，让 fate-core 成为命理能力真相源。 |
| TP-05.01 | TP-05 | 2 | P1 | action | Yes | TP-01.03 | 4 | No | No | 给 bazi_calculator、report_generator、calculate_pure_analysis、bot、main、web_ui 建立职责地图和迁移 kill list。 |
| TP-05.02 | TP-05 | 2 | P1 | action | Yes | TP-01.03, TP-04.01, TP-05.01 | 5 | No | No | 把输入归一化、benchmark、rule depth、topic profile 和 evidence append 拆到 fate-core 内部清晰模块。 |
| TP-05.03 | TP-05 | 2 | P1 | action | Yes | TP-01.03, TP-04.02, TP-05.01 | 7 | No | No | 逐步把历法、四柱、旺衰、格局、用神、岁运从 delivery 大类迁入 fate-core。 |
| TP-05.04 | TP-05 | 2 | P1 | action | Yes | TP-01.03, TP-03.02, TP-03.03, TP-05.01 | 5 | No | No | 把 main、web_ui、bot、report_generator 的交付职责分层，避免继续混入领域算法。 |
| TP-05.05 | TP-05 | 2 | P1 | action | Yes | TP-01.03, TP-05.03, TP-05.04 | 8 | No | No | 删除或收缩无真实公共 API、持久化数据、外部集成支撑的兼容层。 |
| TP-06 | ROOT | 1 | P1 | package | No | TP-01.03 | - | No | Yes | 确保外部库、参考仓、oracle 和规则材料都在正确边界内被复用。 |
| TP-06.01 | TP-06 | 2 | P1 | action | Yes | TP-01.03 | 4 | No | Yes | 明确 lunar-python 为主生产历法底座，sxtwl/bazica/其他项目只作为 oracle 或参考。 |
| TP-06.02 | TP-06 | 2 | P1 | action | Yes | TP-01.03 | 4 | No | Yes | 为 bazi-1、MingLi-Bench、sxtwl、iztro、lunar-python 等建立许可/用途/风险清单。 |
| TP-06.03 | TP-06 | 2 | P2 | action | Yes | TP-01.03, TP-06.01, TP-06.02 | 5 | No | Yes | 保留 sxtwl、bazica、alvamind 等作为对照 oracle，不进入主运行链。 |
| TP-06.04 | TP-06 | 2 | P1 | action | Yes | TP-01.03, TP-04.01 | 5 | No | Yes | 明确 rule_depth_registry、classics_rule_index、future_features 的 owner、字段、升级 gate。 |
| TP-07 | ROOT | 1 | P1 | package | No | TP-02.01, TP-03.03 | - | No | Yes | 把当前应用内 metrics/logs/readiness 扩展到真实运行平台可用的 SLO、告警和排障包。 |
| TP-07.01 | TP-07 | 2 | P1 | action | Yes | TP-02.01, TP-03.03 | 5 | No | Yes | 定义 p95/p99、错误率、429、413、504、inflight、Bot 队列等指标和告警阈值。 |
| TP-07.02 | TP-07 | 2 | P1 | action | Yes | TP-02.01, TP-03.03 | 5 | No | Yes | 确保 X-Request-ID 能关联 HTTP 日志、错误分类、业务计算失败和 Bot 交付。 |
| TP-07.03 | TP-07 | 2 | P1 | action | Yes | TP-02.01, TP-03.03 | 5 | No | Yes | 定义公共服务 SLO、降级策略、恢复步骤、清理本地 runtime 的流程。 |
| TP-07.04 | TP-07 | 2 | P0 | action | Yes | TP-02.01, TP-02.02, TP-03.02, TP-03.03, TP-07.01, TP-07.03 | 6 | No | No | 运行 quick/full/container/public-service 的本地 all profile，作为最终本地质量证据。 |
| TP-08 | ROOT | 1 | P0 | package | No | TP-02.03, TP-04.02, TP-05.05, TP-06.03, TP-07.04 | - | No | No | 用 auto-review 和任务 closeout 证明六项质量标准全部达到 100% gate。 |
| TP-08.01 | TP-08 | 2 | P0 | action | Yes | TP-02.03, TP-04.02, TP-05.05, TP-06.03, TP-07.04 | 9 | No | No | 按 correctness/security/reliability/performance/architecture/operability/repo-hygiene 做最终 review。 |
| TP-08.02 | TP-08 | 2 | P0 | action | Yes | TP-02.03, TP-04.02, TP-05.05, TP-06.03, TP-07.04, TP-08.01 | 10 | No | No | 修复 full-quality-review 发现的 BLOCK，记录无法关闭的外部 blocker。 |
| TP-08.03 | TP-08 | 2 | P0 | action | Yes | TP-02.03, TP-04.02, TP-05.05, TP-06.03, TP-07.04, TP-08.02 | 11 | No | No | 把任务树、执行证据、质量矩阵、review 结论和剩余 HITL 状态收口。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
