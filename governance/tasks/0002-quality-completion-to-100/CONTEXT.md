# Repo Evidence
- 当前仓库：/home/lenovo/.projects/fatecat
- 0001 状态：governance/tasks/0001-quality-standards-100/STATUS.md 为 Blocked，阻塞点是公网 API 与 live Bot HITL
- 已验证：0001 任务文档 decompose 校验通过；当前 INDEX 已修正为 Blocked
- 最近本地证据：REVIEW.md 记录 local-ci all PASS、full .venv/bin/python -m pytest 158 passed、ruff/mypy PASS、Docker 容器 /web smoke OK

# Constraints Matrix
- 允许：修改 governance/tasks/0002-quality-completion-to-100/、必要时维护 governance/tasks/INDEX.md，并按任务树后续叶子修改相关源码/文档/测试
- 禁止：破坏用户已有未提交改动、执行破坏性 git 命令、跑 GitHub Acceptance、伪造外部生产验收
- HITL：真实 HTTPS 生产 URL、TLS/反代配置、生产 CORS allowlist、真实 FATE_BOT_TOKEN 需要用户或部署环境提供

# Change Boundary
- 每次只执行当前 ready 叶子节点声明的变更
- 命理核心输出变化必须由 golden/oracle/evidence 解释，否则停止并转 debug/review
- 架构文件移动或模块拆分必须同步更新对应 AGENTS.md
- 生产相关任务只能固化本地等价配置和 runbook；真实公网验收必须等外部输入

# Risk Matrix
- P0：错误宣称公网生产 100%，会误导发布决策
- P0：八字规则无证据扩写，会降低专业可信度
- P1：继续堆大文件会恶化长期维护性
- P1：新增依赖或规则没有 license/source/owner，会破坏企业治理
- P2：过度任务拆分会降低执行效率，需保持叶子节点可直接验收

# Assumptions and Falsification
- 假设：当前本地 CI/CD 与 0001 记录的证据大体可信，但本任务仍需在关键节点复跑验证
- 反证：若 local-ci all、golden/oracle、policy asset 或容器 smoke 失败，则不得推进对应维度到 100%
- 反证：若真实公网 URL/token 不可用，则公共生产只能停在 HITL Blocked，不能进入 Done
- 反证：若高级八字规则无法给出 source/ruleId/riskBoundary，则该能力不能计入专业 100%

# Critical Ambiguities
- 公共生产 URL、TLS/反代、真实 Bot token 尚未提供；这只阻塞 TP-06.04 和最终公网 100%
- 专业八字 100% 的经典语料边界需要以本仓库 registry 和可许可参考源为准；不采纳无 license 的生产依赖扩散

# Debug Evidence Contract
- 调试模式: Optional
- 若 local-ci、golden/oracle、容器 smoke 或公网 readiness 失败，必须转 Required 并维护 DEBUG.md
- DEBUG.md 必须记录复现、观察、假设、实验、根因、修复、回归证据

# Task Package Context Map
## TP-00
- 标题: 任务控制面修正
- 目标: 修正任务索引、状态和下一阶段任务容器，确保任务真相源可继续执行
- 有效叶子依赖: -
- 当前状态: Done

### TP-00.01
- 标题: 修正 0001 索引状态
- 目标: 让 governance/tasks/INDEX.md 与 0001 STATUS.md 的 Blocked 状态一致
- 有效叶子依赖: 
- 当前状态: Done

### TP-00.02
- 标题: 创建 0002 任务树
- 目标: 创建并回填 0002 任务容器，承接剩余 100% 推进工作
- 有效叶子依赖: TP-00.01
- 当前状态: Done

## TP-01
- 标题: 本地开发可用性 100%
- 目标: 把本地开发体验从可用提升到可复制、可恢复、可验证的 100% 状态
- 有效叶子依赖: -
- 当前状态: Done

### TP-01.01
- 标题: 固化一键本地开发入口
- 目标: 确认并文档化 API/Web/Bot dry-run、本地环境启动和常见开发命令
- 有效叶子依赖: TP-00.01, TP-00.02
- 当前状态: Done

### TP-01.02
- 标题: 补齐本地恢复路径
- 目标: 补齐 venv 重建、缓存清理、runtime 清理、失败恢复的最小 runbook
- 有效叶子依赖: TP-00.01, TP-00.02
- 当前状态: Done

### TP-01.03
- 标题: 本地开发 smoke 验收
- 目标: 用 quick profile 和 delivery smoke 证明本地开发链路可用
- 有效叶子依赖: TP-00.01, TP-00.02, TP-01.01, TP-01.02
- 当前状态: Done

## TP-02
- 标题: 企业仓库结构 100%
- 目标: 确保 canonical roots、catalog、governance、contracts 和防回潮门禁达到企业仓库结构 100%
- 有效叶子依赖: -
- 当前状态: Done

### TP-02.01
- 标题: 结构与目录门禁复核
- 目标: 复核 canonical roots、旧路径禁用、compat ledger 和目录 AGENTS.md 状态
- 有效叶子依赖: TP-00.01, TP-00.02
- 当前状态: Done

### TP-02.02
- 标题: catalog 与治理索引新鲜度
- 目标: 确认 catalog、governance INDEX、migration ledger、tech-debt evidence 与当前结构一致
- 有效叶子依赖: TP-00.01, TP-00.02
- 当前状态: Done

### TP-02.03
- 标题: 企业结构最终验收
- 目标: 用结构、源码卫生、导出卫生和任务文档校验证明企业仓库结构 100%
- 有效叶子依赖: TP-00.01, TP-00.02, TP-02.01, TP-02.02
- 当前状态: Done

## TP-03
- 标题: 本地 CI/CD 100%
- 目标: 把本地 quick/full/export/docker/container/public-service 形成可重复发布门禁
- 有效叶子依赖: -
- 当前状态: Done

### TP-03.01
- 标题: 本地 CI profile 目录化
- 目标: 确认 local-ci 各 profile 的职责、输出证据和失败处理方式清晰
- 有效叶子依赖: TP-00.01, TP-00.02
- 当前状态: Done

### TP-03.02
- 标题: 供应链与制品证据
- 目标: 补齐依赖来源、vendor health、容器 image、export runtime 的本地证据路径
- 有效叶子依赖: TP-00.01, TP-00.02
- 当前状态: Done

### TP-03.03
- 标题: 本地 CI/CD 全链路验收
- 目标: 复跑 all profile，形成本地 CI/CD 100% 最新证据
- 有效叶子依赖: TP-00.01, TP-00.02, TP-03.01, TP-03.02
- 当前状态: Done

## TP-04
- 标题: 八字基础能力 100%
- 目标: 把四柱、节气、真太阳时、起运、证据层、golden/oracle 覆盖推进到基础 100%
- 有效叶子依赖: -
- 当前状态: Done

### TP-04.01
- 标题: 扩展 golden matrix 到 300+
- 目标: 在现有 120 样本基础上扩展到 300+，覆盖节气、子时、真太阳时、起运、地域时区、边界反例
- 有效叶子依赖: TP-00.01, TP-00.02
- 当前状态: Done

### TP-04.02
- 标题: 历法 oracle 对照增强
- 目标: 增强 lunar-python 主链与 sxtwl/oracle 开发门禁对照，确保 oracle 不污染生产路径
- 有效叶子依赖: TP-00.01, TP-00.02
- 当前状态: Done

### TP-04.03
- 标题: 基础能力证据覆盖验收
- 目标: 确认四柱、节气、起运、五行、十神、神煞等基础判断均有 ruleId/source/riskBoundary
- 有效叶子依赖: TP-00.01, TP-00.02, TP-04.01, TP-04.02
- 当前状态: Done

## TP-05
- 标题: 八字专业完整度 100%
- 目标: 补齐高级格局、合化成败、用神裁决、岁运专题和专业 benchmark
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-05.01
- 标题: 高级格局 registry
- 目标: 建立正格、变格、从格、专旺、化气、假从的规则 registry 与反例条件
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03
- 当前状态: Not Started

### TP-05.02
- 标题: 合化成败引擎
- 目标: 实现合化成败条件链：月令、透干、通根、得令、阻隔、帮扶、冲破
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03, TP-05.01
- 当前状态: Not Started

### TP-05.03
- 标题: 用神裁决引擎
- 目标: 把调候、扶抑、通关、病药做成并列策略评分与冲突裁决
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03, TP-05.01
- 当前状态: Not Started

### TP-05.04
- 标题: 岁运专题 profile
- 目标: 补齐财、官、婚、健康、迁移、事业等岁运专题 profile 的规则证据和风险边界
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03, TP-05.01
- 当前状态: Not Started

### TP-05.05
- 标题: 专业 benchmark 与报告验收
- 目标: 用 MingLi-Bench、本仓 golden 和报告回归验证专业完整度
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03, TP-05.02, TP-05.03, TP-05.04
- 当前状态: Not Started

## TP-06
- 标题: 公共生产稳定性 100%
- 目标: 补齐本地生产等价配置、观测、限流和真实公网 live 验收
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-06.01
- 标题: 生产等价配置复核
- 目标: 确认 CORS allowlist、trusted proxy、HSTS、edge body limit、timeouts 和生产 env 示例完整
- 有效叶子依赖: TP-03.01, TP-03.02, TP-03.03
- 当前状态: Not Started

### TP-06.02
- 标题: 多副本限流与边缘防护方案
- 目标: 把单进程内存限流的边界、Redis/网关/WAF 升级路径和 body limit 策略写入运行合同
- 有效叶子依赖: TP-03.01, TP-03.02, TP-03.03
- 当前状态: Not Started

### TP-06.03
- 标题: 观测与错误定位增强
- 目标: 补齐 p95/p99 histogram、错误分类、requestId 贯穿、运行 runbook 的验收证据
- 有效叶子依赖: TP-03.01, TP-03.02, TP-03.03
- 当前状态: Not Started

### TP-06.04
- 标题: 真实公网 API 与 Bot live 验收
- 目标: 在真实 HTTPS URL、TLS/反代、真实 FATE_BOT_TOKEN 可用后完成公共生产 100% 验收
- 有效叶子依赖: TP-03.01, TP-03.02, TP-03.03, TP-06.01, TP-06.02, TP-06.03
- 当前状态: Blocked

## TP-07
- 标题: 长期维护性 100%
- 目标: 继续拆核心大文件，收缩 delivery 职责，清退无契约兼容面
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-07.01
- 标题: 拆分 bazi kernel 子模块
- 目标: 把 fate_core.kernel.bazi_calculator 按 calendar、pillars、strength、relations、spirits、patterns、yongshen、fortune 逐步拆边界
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03
- 当前状态: Not Started

### TP-07.02
- 标题: 收敛 delivery 大文件
- 目标: 收敛 main.py、bot.py、report/web_ui 的职责边界，确保 delivery 只做编排、渲染、传输、观测防护
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03
- 当前状态: Not Started

### TP-07.03
- 标题: 兼容面 burn-down
- 目标: 审计 remaining adapter/shim/wrapper，删除无真实外部契约的兼容面，保留项必须有 owner 和移除条件
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03
- 当前状态: Not Started

### TP-07.04
- 标题: 长期维护性最终验收
- 目标: 用模块边界、测试、review 和 local-ci 证明长期维护性达到 100%
- 有效叶子依赖: TP-04.01, TP-04.02, TP-04.03, TP-07.01, TP-07.02, TP-07.03
- 当前状态: Not Started

## TP-08
- 标题: 最终审查与交付
- 目标: 汇总本地 100%、八字 100%、公网 HITL 状态，形成最终可交付版本
- 有效叶子依赖: -
- 当前状态: Not Started

### TP-08.01
- 标题: 全仓本地质量审查
- 目标: 执行 correctness/security/reliability/performance/architecture/operability/repo-hygiene 审查
- 有效叶子依赖: TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04
- 当前状态: Not Started

### TP-08.02
- 标题: 处理最终 findings
- 目标: 处理 TP-08.01 中发现的 BLOCK 和影响 100% gate 的 WARN
- 有效叶子依赖: TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04, TP-08.01
- 当前状态: Not Started

### TP-08.03
- 标题: 生成 closeout
- 目标: 生成任务 closeout，明确 Done、Blocked、Skipped、Unknown 和最终百分比
- 有效叶子依赖: TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04, TP-08.02
- 当前状态: Not Started
