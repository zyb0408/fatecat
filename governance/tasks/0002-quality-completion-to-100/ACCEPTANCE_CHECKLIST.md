# Acceptance Checklist

# Global Standards
- [ ] 每个叶子节点有真实 Verify 和 Gate
- [ ] 每个完成节点有 Recent Evidence
- [ ] 本地验证失败时不得标 Done
- [ ] 外部 HITL 缺输入时不得伪造通过
- [ ] 新增规则、依赖、文档、配置均有存在性理由和维护边界
- [ ] 最终汇报区分 Done、Blocked、Skipped、Unknown

# Task Package Checklists
## TP-00
- 标题: 任务控制面修正
- 验收项:
  - [ ] `任务控制面修正` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 修正任务索引、状态和下一阶段任务容器，确保任务真相源可继续执行
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-00.01
- 标题: 修正 0001 索引状态
- 验收项:
  - [ ] INDEX 不再把 0001 写成 In Progress
  - [ ] 0001 decompose 校验 OK
- Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0001-quality-standards-100 --phase decompose && sed -n '1,30p' governance/tasks/INDEX.md
- Gate: 0001 状态为 Blocked，且 0001 任务文档校验通过
- 输出物:
  - [ ] governance/tasks/INDEX.md 状态修正
- 标准清单:
  - [ ] Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0001-quality-standards-100 --phase decompose && sed -n '1,30p' governance/tasks/INDEX.md
  - [ ] Gate: 0001 状态为 Blocked，且 0001 任务文档校验通过
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-00.02
- 标题: 创建 0002 任务树
- 验收项:
  - [ ] 任务容器存在并可校验
  - [ ] 下一批 ready 叶子节点清晰
- Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0002-quality-completion-to-100 --phase decompose
- Gate: 0002 文档无非法占位符，任务树依赖和 ready queue 可渲染
- 输出物:
  - [ ] governance/tasks/0002-quality-completion-to-100/TREE_SPEC.json
  - [ ] governance/tasks/0002-quality-completion-to-100/README.md
  - [ ] governance/tasks/0002-quality-completion-to-100/PLAN.md
  - [ ] governance/tasks/0002-quality-completion-to-100/TODO.md
  - [ ] governance/tasks/0002-quality-completion-to-100/STATUS.md
- 标准清单:
  - [ ] Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0002-quality-completion-to-100 --phase decompose
  - [ ] Gate: 0002 文档无非法占位符，任务树依赖和 ready queue 可渲染
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-01
- 标题: 本地开发可用性 100%
- 验收项:
  - [ ] `本地开发可用性 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 把本地开发体验从可用提升到可复制、可恢复、可验证的 100% 状态
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 固化一键本地开发入口
- 验收项:
  - [ ] 新人能按文档完成 venv、安装、启动、smoke
  - [ ] 命令不依赖 GitHub Actions
- Verify: rg 'local-ci|delivery-smoke|uvicorn|/web|Bot' references README.md Makefile scripts -n
- Gate: README/references/Makefile/scripts 中存在可执行本地开发入口和验证路径
- 输出物:
  - [ ] 本地开发入口清单
  - [ ] 必要时更新 references/commands.md 或 README.md
- 标准清单:
  - [ ] Verify: rg 'local-ci|delivery-smoke|uvicorn|/web|Bot' references README.md Makefile scripts -n
  - [ ] Gate: README/references/Makefile/scripts 中存在可执行本地开发入口和验证路径
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.02
- 标题: 补齐本地恢复路径
- 验收项:
  - [ ] 恢复命令覆盖 .venv、pip、.venv/bin/python -m pytest cache、runtime/export/docker 残留
- Verify: rg 'venv|clean-runtime|pip cache|pytest_cache|build/|dist/' references README.md scripts -n
- Gate: 本地依赖坏掉、runtime 脏掉、测试缓存脏掉时有可执行恢复命令
- 输出物:
  - [ ] 本地恢复 runbook
- 标准清单:
  - [ ] Verify: rg 'venv|clean-runtime|pip cache|pytest_cache|build/|dist/' references README.md scripts -n
  - [ ] Gate: 本地依赖坏掉、runtime 脏掉、测试缓存脏掉时有可执行恢复命令
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.03
- 标题: 本地开发 smoke 验收
- 验收项:
  - [ ] 本地开发可用性可按命令复现
- Verify: bash scripts/local-ci.sh --profile quick && bash scripts/delivery-smoke.sh
- Gate: quick profile 和 delivery smoke PASS，失败则转 DEBUG.md
- 输出物:
  - [ ] 本地开发 smoke evidence
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile quick && bash scripts/delivery-smoke.sh
  - [ ] Gate: quick profile 和 delivery smoke PASS，失败则转 DEBUG.md
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 企业仓库结构 100%
- 验收项:
  - [ ] `企业仓库结构 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 确保 canonical roots、catalog、governance、contracts 和防回潮门禁达到企业仓库结构 100%
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 结构与目录门禁复核
- 验收项:
  - [ ] 企业 canonical roots 保持为唯一活跃结构
- Verify: bash scripts/check-structure.sh && rg 'compatibility_source_root|temporary-compatibility-box|scripts/project' . -g '!tools/reference-repos/**' -g '!governance/tasks/**'
- Gate: 结构门禁通过；旧路径命中只允许出现在防回潮测试、账本或历史说明中
- 输出物:
  - [ ] 结构门禁 evidence
  - [ ] 旧路径扫描结果
- 标准清单:
  - [ ] Verify: bash scripts/check-structure.sh && rg 'compatibility_source_root|temporary-compatibility-box|scripts/project' . -g '!tools/reference-repos/**' -g '!governance/tasks/**'
  - [ ] Gate: 结构门禁通过；旧路径命中只允许出现在防回潮测试、账本或历史说明中
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: catalog 与治理索引新鲜度
- 验收项:
  - [ ] 组件 owner、生命周期、迁移账本和技术债证据可互相回指
- Verify: python3 governance/tools/validate_governance_package.py --strict || true; rg 'fate-core|fatecat-delivery|compatibility-ledger|DEBT-0001' catalog governance -n
- Gate: 若治理校验工具存在且可运行则无 BLOCK；若当前治理 strict 有历史 WARN，必须记录 owner 和后续任务
- 输出物:
  - [ ] catalog/governance freshness evidence
- 标准清单:
  - [ ] Verify: python3 governance/tools/validate_governance_package.py --strict || true; rg 'fate-core|fatecat-delivery|compatibility-ledger|DEBT-0001' catalog governance -n
  - [ ] Gate: 若治理校验工具存在且可运行则无 BLOCK；若当前治理 strict 有历史 WARN，必须记录 owner 和后续任务
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.03
- 标题: 企业结构最终验收
- 验收项:
  - [ ] 无未解释结构漂移
  - [ ] 任务树校验不失败
- Verify: tmp_dir=$(mktemp -d /tmp/fatecat-export-check-XXXXXX); bash scripts/check-structure.sh && bash scripts/check-source-hygiene.sh && bash scripts/export-runtime.sh --output-parent "${tmp_dir}" --mode lite && bash scripts/check-export-hygiene.sh "${tmp_dir}/fatecat" && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto
- Gate: 结构/source/export/tasks 校验通过或历史外部阻塞被明确记录
- 输出物:
  - [ ] 企业结构 100% evidence
- 标准清单:
  - [ ] Verify: tmp_dir=$(mktemp -d /tmp/fatecat-export-check-XXXXXX); bash scripts/check-structure.sh && bash scripts/check-source-hygiene.sh && bash scripts/export-runtime.sh --output-parent "${tmp_dir}" --mode lite && bash scripts/check-export-hygiene.sh "${tmp_dir}/fatecat" && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto
  - [ ] Gate: 结构/source/export/tasks 校验通过或历史外部阻塞被明确记录
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 本地 CI/CD 100%
- 验收项:
  - [ ] `本地 CI/CD 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 把本地 quick/full/export/docker/container/public-service 形成可重复发布门禁
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 本地 CI profile 目录化
- 验收项:
  - [ ] 本地发布门禁不依赖远端 CI
- Verify: bash scripts/local-ci.sh --help || sed -n '1,220p' scripts/local-ci.sh
- Gate: quick/full/public-service/export/docker/container smoke 的职责和证据目录可读
- 输出物:
  - [ ] local-ci profile contract
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --help || sed -n '1,220p' scripts/local-ci.sh
  - [ ] Gate: quick/full/public-service/export/docker/container smoke 的职责和证据目录可读
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.02
- 标题: 供应链与制品证据
- 验收项:
  - [ ] 依赖和制品不是黑箱
- Verify: bash scripts/vendor-health.sh && bash scripts/export-runtime.sh --help && docker image inspect fatecat-delivery:local >/dev/null 2>&1 || true
- Gate: 供应链、vendor、export、container 证据路径明确；缺 Docker 时记录环境 blocker
- 输出物:
  - [ ] supply-chain/local-artifact evidence
- 标准清单:
  - [ ] Verify: bash scripts/vendor-health.sh && bash scripts/export-runtime.sh --help && docker image inspect fatecat-delivery:local >/dev/null 2>&1 || true
  - [ ] Gate: 供应链、vendor、export、container 证据路径明确；缺 Docker 时记录环境 blocker
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.03
- 标题: 本地 CI/CD 全链路验收
- 验收项:
  - [ ] 本地 CI/CD 100% 有最新可复核证据
- Verify: bash scripts/local-ci.sh --profile all
- Gate: all profile PASS；如 Docker/外部凭证缺失，必须拆分记录真实 blocker
- 输出物:
  - [ ] local-ci all evidence directory
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile all
  - [ ] Gate: all profile PASS；如 Docker/外部凭证缺失，必须拆分记录真实 blocker
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 八字基础能力 100%
- 验收项:
  - [ ] `八字基础能力 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 把四柱、节气、真太阳时、起运、证据层、golden/oracle 覆盖推进到基础 100%
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 扩展 golden matrix 到 300+
- 验收项:
  - [ ] 基础八字边界不靠单点样例证明
- Verify: python3 -m json.tool domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json >/dev/null && .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py
- Gate: 样本数 >=300；每个样本有 source/expected/coverageTags/failure explanation path
- 输出物:
  - [ ] coverage_matrix_cases.json 300+ 样本
  - [ ] golden regression evidence
- 标准清单:
  - [ ] Verify: python3 -m json.tool domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json >/dev/null && .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py
  - [ ] Gate: 样本数 >=300；每个样本有 source/expected/coverageTags/failure explanation path
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 历法 oracle 对照增强
- 验收项:
  - [ ] 历法底座可复核且边界清楚
- Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py
- Gate: oracle 只用于测试/评估，生产路径仍通过 CalendarProvider
- 输出物:
  - [ ] calendar oracle evidence
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py
  - [ ] Gate: oracle 只用于测试/评估，生产路径仍通过 CalendarProvider
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.03
- 标题: 基础能力证据覆盖验收
- 验收项:
  - [ ] 八字基础能力可解释、可测试、可回归
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_golden_coverage_matrix.py
- Gate: 无孤儿 ruleId，无核心基础判断缺 evidence
- 输出物:
  - [ ] 八字基础能力 100% evidence
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_golden_coverage_matrix.py
  - [ ] Gate: 无孤儿 ruleId，无核心基础判断缺 evidence
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 八字专业完整度 100%
- 验收项:
  - [ ] `八字专业完整度 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 补齐高级格局、合化成败、用神裁决、岁运专题和专业 benchmark
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 高级格局 registry
- 验收项:
  - [ ] 格局判断不是文案标签，而是证据化规则
- Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_ziwei_rule_depth.py
- Gate: 每条高级格局规则有 source、appliesWhen、doesNotApplyWhen、riskBoundary
- 输出物:
  - [ ] 高级格局规则 registry
  - [ ] 高级格局测试
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_ziwei_rule_depth.py
  - [ ] Gate: 每条高级格局规则有 source、appliesWhen、doesNotApplyWhen、riskBoundary
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 合化成败引擎
- 验收项:
  - [ ] 合化结论有条件链和失败原因
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py
- Gate: 合而不化、可化、破化、争合等反例均有 golden 覆盖
- 输出物:
  - [ ] 合化成败 evaluator
  - [ ] 合化 golden cases
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py
  - [ ] Gate: 合而不化、可化、破化、争合等反例均有 golden 覆盖
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.03
- 标题: 用神裁决引擎
- 验收项:
  - [ ] 用神不是单表查值，而是可解释裁决
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py
- Gate: 用神结论展示策略评分、冲突原因、保守边界，不输出确定性人生建议
- 输出物:
  - [ ] yongshen strategy scoring
  - [ ] 用神冲突测试
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py
  - [ ] Gate: 用神结论展示策略评分、冲突原因、保守边界，不输出确定性人生建议
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.04
- 标题: 岁运专题 profile
- 验收项:
  - [ ] 岁运专题具备可审查输入和保守输出边界
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py
- Gate: 专题 profile 只输出 evidence_seed/riskBoundary，不输出确定性预测或专业替代建议
- 输出物:
  - [ ] fortune topic profiles
  - [ ] 专题 profile 测试
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py
  - [ ] Gate: 专题 profile 只输出 evidence_seed/riskBoundary，不输出确定性预测或专业替代建议
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.05
- 标题: 专业 benchmark 与报告验收
- 验收项:
  - [ ] 高级八字能力不是孤立代码，而有评测与报告验收
- Verify: bash scripts/run-mingli-bench.sh --stats --sample 5 && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py
- Gate: 专业 benchmark 有统计结果；报告输出引用规则证据且风险话术通过测试
- 输出物:
  - [ ] 八字专业完整度 100% evidence
- 标准清单:
  - [ ] Verify: bash scripts/run-mingli-bench.sh --stats --sample 5 && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py
  - [ ] Gate: 专业 benchmark 有统计结果；报告输出引用规则证据且风险话术通过测试
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 公共生产稳定性 100%
- 验收项:
  - [ ] `公共生产稳定性 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 补齐本地生产等价配置、观测、限流和真实公网 live 验收
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.01
- 标题: 生产等价配置复核
- 验收项:
  - [ ] 生产配置不是靠口头约定
- Verify: bash scripts/production-readiness.sh --skip-bootstrap
- Gate: 本地生产等价静态门禁 PASS；没有真实公网时 live 项保持 SKIP
- 输出物:
  - [ ] production static readiness evidence
- 标准清单:
  - [ ] Verify: bash scripts/production-readiness.sh --skip-bootstrap
  - [ ] Gate: 本地生产等价静态门禁 PASS；没有真实公网时 live 项保持 SKIP
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.02
- 标题: 多副本限流与边缘防护方案
- 验收项:
  - [ ] 多副本公共服务不会误以为内存限流足够
- Verify: rg 'Redis|WAF|rate|body limit|trusted proxy|HSTS|CORS' references infra domains -n
- Gate: 单实例/多副本限流边界明确；公网入口必须有 edge body limit
- 输出物:
  - [ ] public service protection contract
- 标准清单:
  - [ ] Verify: rg 'Redis|WAF|rate|body limit|trusted proxy|HSTS|CORS' references infra domains -n
  - [ ] Gate: 单实例/多副本限流边界明确；公网入口必须有 edge body limit
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.03
- 标题: 观测与错误定位增强
- 验收项:
  - [ ] 公共服务不是只看 /health
- Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_operability_docs.py
- Gate: 5xx/timeout/rate-limit 可从 metrics/log/runbook 定位
- 输出物:
  - [ ] observability evidence
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_operability_docs.py
  - [ ] Gate: 5xx/timeout/rate-limit 可从 metrics/log/runbook 定位
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.04
- 标题: 真实公网 API 与 Bot live 验收
- 验收项:
  - [ ] 公共生产 100% 必须来自真实外部验收
- Verify: bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot
- Gate: 真实 /health、/ready、/metrics 和 Telegram get_me 通过；无 placeholder token
- 输出物:
  - [ ] live API readiness evidence
  - [ ] live Bot evidence
- 标准清单:
  - [ ] Verify: bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot
  - [ ] Gate: 真实 /health、/ready、/metrics 和 Telegram get_me 通过；无 placeholder token
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-07
- 标题: 长期维护性 100%
- 验收项:
  - [ ] `长期维护性 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 继续拆核心大文件，收缩 delivery 职责，清退无契约兼容面
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.01
- 标题: 拆分 bazi kernel 子模块
- 验收项:
  - [ ] 核心算法边界变窄，行为由 golden 护住
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_api_contracts.py tests/regression/fate_core/test_pure_analysis_usecase.py
- Gate: 外部 API 输出不漂移；kernel/AGENTS.md 同步更新；旧 wrapper 不新增领域逻辑
- 输出物:
  - [ ] fate_core.kernel 子模块
  - [ ] kernel/AGENTS.md 更新
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_api_contracts.py tests/regression/fate_core/test_pure_analysis_usecase.py
  - [ ] Gate: 外部 API 输出不漂移；kernel/AGENTS.md 同步更新；旧 wrapper 不新增领域逻辑
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.02
- 标题: 收敛 delivery 大文件
- 验收项:
  - [ ] 交付层不再吸收领域算法债务
- Verify: .venv/bin/python -m pytest domains/experience-delivery/services/fatecat-delivery/tests tests/regression/test_web_html.py tests/regression/test_api_contracts.py
- Gate: delivery 不新增命理规则；边界合同测试通过；AGENTS.md 同步更新
- 输出物:
  - [ ] delivery boundary cleanup
  - [ ] delivery AGENTS.md 更新
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest domains/experience-delivery/services/fatecat-delivery/tests tests/regression/test_web_html.py tests/regression/test_api_contracts.py
  - [ ] Gate: delivery 不新增命理规则；边界合同测试通过；AGENTS.md 同步更新
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.03
- 标题: 兼容面 burn-down
- 验收项:
  - [ ] 不再围绕错误概念继续堆 wrapper
- Verify: rg 'compat|legacy|shim|wrapper|fallback' domains contracts catalog governance -n
- Gate: 保留的兼容面均写入 compatibility-ledger；无契约项进入 kill list 或删除
- 输出物:
  - [ ] compatibility burn-down evidence
- 标准清单:
  - [ ] Verify: rg 'compat|legacy|shim|wrapper|fallback' domains contracts catalog governance -n
  - [ ] Gate: 保留的兼容面均写入 compatibility-ledger；无契约项进入 kill list 或删除
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.04
- 标题: 长期维护性最终验收
- 验收项:
  - [ ] 长期维护不依赖个人记忆
- Verify: bash scripts/local-ci.sh --profile quick && .venv/bin/python -m pytest tests/regression/test_catalog_contracts.py tests/regression/test_operability_docs.py
- Gate: 核心边界清楚，大文件不再是新增职责入口，local quick PASS
- 输出物:
  - [ ] maintainability 100% evidence
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile quick && .venv/bin/python -m pytest tests/regression/test_catalog_contracts.py tests/regression/test_operability_docs.py
  - [ ] Gate: 核心边界清楚，大文件不再是新增职责入口，local quick PASS
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-08
- 标题: 最终审查与交付
- 验收项:
  - [ ] `最终审查与交付` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 汇总本地 100%、八字 100%、公网 HITL 状态，形成最终可交付版本
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.01
- 标题: 全仓本地质量审查
- 验收项:
  - [ ] 本地 100% 可交付
- Verify: bash scripts/local-ci.sh --profile all
- Gate: 本地全链路 PASS；review BLOCK=0；WARN 有 owner
- 输出物:
  - [ ] final local review evidence
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile all
  - [ ] Gate: 本地全链路 PASS；review BLOCK=0；WARN 有 owner
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.02
- 标题: 处理最终 findings
- 验收项:
  - [ ] 最终缺陷不留口头豁免
- Verify: 复跑触发 finding 的最小命令，并记录修复证据
- Gate: BLOCK=0；剩余 WARN 不影响 100% 或有明确后续 owner
- 输出物:
  - [ ] final findings fix evidence
- 标准清单:
  - [ ] Verify: 复跑触发 finding 的最小命令，并记录修复证据
  - [ ] Gate: BLOCK=0；剩余 WARN 不影响 100% 或有明确后续 owner
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.03
- 标题: 生成 closeout
- 验收项:
  - [ ] 最终交付版本可审查、可复现、可继续接手
- Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0002-quality-completion-to-100 --phase closeout
- Gate: TODO 全部完成或 HITL Blocked 明确；最终汇报不含伪证
- 输出物:
  - [ ] task closeout packet
  - [ ] final quality matrix
- 标准清单:
  - [ ] Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0002-quality-completion-to-100 --phase closeout
  - [ ] Gate: TODO 全部完成或 HITL Blocked 明确；最终汇报不含伪证
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
