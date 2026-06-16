# Final Review

任务节点：`TP-10.01`

## 结论

本地工程门禁结论：`PASS with WARN`

- Active BLOCK：`0`
- 八字体系任务树 P0/P1 能力建设：`已完成到本轮工程验收口径`
- 专业命中率口径：`未达专业强推理口径`
- MingLi full baseline：`160 answered / 45 correct / 28.12% accuracy`
- 允许进入：`本地可交付、可继续迭代、可作为 beta 级命理分析底座`
- 不允许宣称：`八字预测 100% 准确`、`专业命理推理已经强`、`MingLi 达生产标准`

这里的 `100%` 只指任务树和工程验收项全部可追溯，不是预测准确率 100%。

## 验证命令

```bash
bash scripts/local-ci.sh --profile quick
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0003-bazi-system-100 --phase decompose
```

结果：

- `local-ci quick`：PASS，evidence `/tmp/fatecat-local-ci-20260616173830`
- focused regression：`49 passed in 9.74s`
- mypy：`Success: no issues found in 39 source files`
- 八字 rule-depth：`30 passed in 62.50s`
- task docs decompose：PASS，`placeholders=[]`、`errors=[]`

## 六维审查

| 质量标准 | 结论 | 证据 | WARN / 下一步 |
| --- | --- | --- | --- |
| 满足约束 | PASS | `SCORECARD.md` 定义 100% 工程口径；`RESOURCE_MAP.md` 区分 production/oracle/evaluation/reference；local-ci quick PASS。 | 不得把工程 100% 讲成预测准确率 100%。Owner: `fate-core`。 |
| 可解释 | PASS | `rule_depth_registry.json`、`classics_rule_index.json`、`analysisEvidence`、`sourceRuleId`、`riskBoundary` 已进入 API/报告契约；`test_bazi_ziwei_rule_depth.py` 30 passed。 | 高级格局、专题 profile 仍以 beta/evidence_seed 为主。Owner: `fate-core rules`。 |
| 可测试 | PASS | quick gate、rule-depth、API/Web、policy、calendar/golden/deep gate 均有命令；MingLi full 160 已跑通。 | 300+ golden 和 MingLi full 都慢，继续保持 deep/evaluation gate，不进日常 quick。Owner: `QA/governance`。 |
| 可维护 | WARN | `CORE_FILE_BURNDOWN.md` 和 `EVALUATOR_BOUNDARIES.md` 已定义拆分路线、行为保持测试和边界。 | `bazi_calculator.py`、`calculate_pure_analysis.py`、`report_generator.py` 仍偏大；后续按 evaluator 单切片迁移。Owner: `fate-core + delivery`。 |
| 处理特殊情况 | PASS with WARN | calendar boundary、true solar time、早晚子时、起运、合化状态、用神冲突、岁运触发均有 golden/registry/evaluator 证据。 | 专家真实命例和更多边界样本仍不足；保持 HITL/WARN，不硬造样本。Owner: `domain-review`。 |
| 复用建立在理解上 | PASS | `lunar-python` 为生产历法底座；sxtwl/sxwnl/bazica 为 oracle_only；MingLi 为 evaluation_only；预测文件无答案泄漏字段。 | 无 license/reference-only 资源不得进入 runtime dependency。Owner: `supply-chain`。 |

## 关键能力状态

| 能力面 | 状态 | 证据 |
| --- | --- | --- |
| 基础排盘与时间边界 | PASS | TP-02 完成；calendar/oracle/golden/deep gate 已记录。 |
| 高级格局 | PASS with beta boundary | TP-03 完成；从格、化气、专旺、假从等有 rule matrix、evaluator 状态和 golden。 |
| 合化成败 | PASS | TP-04 完成；输出区分 structural_relation、transform_candidate、transform_success、transform_broken。 |
| 用神裁决 | PASS | TP-05 完成；调候、扶抑、通关、病药并列评分，不用单一用神覆盖全部。 |
| 岁运专题 | PASS with beta boundary | TP-06 完成；事业、财运、婚姻、健康、学业、迁移、家庭 profile 有 score/evidence/risk/lifecycle。 |
| 样本外评测 | WARN | TP-07 完成评测链路；full accuracy 28.12%，不能宣称专业推理强。 |
| 报告/API 边界 | PASS | TP-08 完成；报告字段契约和高风险话术回归已锁定。 |
| 长期维护边界 | WARN | TP-09 完成；边界已定义，物理拆分仍是后续维护任务。 |

## Active WARN

| WARN | Evidence | Owner | Next |
| --- | --- | --- | --- |
| MingLi full accuracy 28.12% | `MINGLI_FULL_EVALUATION.md` | `fate-core rules` | 按 `BENCHMARK_GATE_POLICY.md` 先冲 overall >=32%，财运 >=15%。 |
| 专题 profile 仍是 beta | `topicProfiles.lifecycle=beta`、`REPORT_FIELD_CONTRACT.md` | `fate-core usecases` | 增加专题 golden、失败样本归因和报告边界回归后再升 production。 |
| 核心文件仍大 | `CORE_FILE_BURNDOWN.md` | `fate-core + delivery` | 按 `EVALUATOR_BOUNDARIES.md` 单 evaluator 抽取，不大爆炸重写。 |
| full golden / MingLi deep gate 慢 | `GOLDEN_DEEP_GATE.md`、`MINGLI_FULL_EVALUATION.md` | `QA/governance` | quick 保持代表集；deep/release 使用 shard 或显式 evaluation 命令。 |
| 真实专家命例不足 | `RULE_SOURCE_GAPS.md`、`MINGLI_FAILURE_TAXONOMY.md` | `domain-review` | 后续 HITL 标注，不用无来源样本补数。 |

## Falsifier 检查

- oracle 进入生产主链：未发现；边界写入 `EVALUATOR_BOUNDARIES.md`。
- evaluation 反向进入 kernel/usecase：未发现；`fate_core.evaluation` 只读 `calculate_pure_analysis`。
- delivery 承载新增领域算法：本轮未新增；边界已锁定。
- MingLi 答案泄漏：未发现；predictions 字段无 `expected`、`answer`、`correct`、`ground_truth`、`gold`、`label`。
- 高风险建议输出：policy/API/Web 回归已禁止医疗、金融、法律、心理替代建议和保证式话术。

## TP-10.01 Gate 判定

- `active BLOCK=0`：`PASS`
- `WARN 有 owner、证据和下一步`：`PASS`
- `不得伪造 100%`：`PASS`

本轮允许进入 `TP-10.02 Closeout 和版本交付`。
