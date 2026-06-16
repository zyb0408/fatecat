# Task-Level Acceptance

- 计划覆盖用户给出的十个维度，并逐项说明 current、target、任务、verify、gate、falsifier。
- 每个任务叶子都有 `TP-XX.YY` 编号、依赖、完成证据和验收命令。
- 计划明确资源角色，不把 oracle/evaluation/reference/future_candidate 混进 production。
- 计划明确 benchmark 的 100% 不是准确率 100%，而是评测体系成熟度 100%。
- 计划可以由 `validate_task_docs.py --phase decompose` 复核，无占位符。

# Validation Plan

```bash
python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py \
  --task-dir governance/tasks/0005-bazi-capability-100-roadmap \
  --phase decompose

rg '\{\{|\}\}' governance/tasks/0005-bazi-capability-100-roadmap
```

# Review Gate

- `PASS`：十个维度都有 100% gate 和可执行任务。
- `WARN`：外部专家样本、BaziQA license、benchmark 阈值只能作为后续 HITL/准入 gate。
- `BLOCK`：任何任务要求答案泄漏、生产接入评测数据、无来源强断高级格局、输出高风险现实处方。

# Runtime Verification Gate

- 计划阶段只验证文档完整性。
- 实现阶段必须逐 leaf 执行本地测试，不允许只用 README 或人工声明验收。
- 最终 release gate 必须至少包含 local quick、local full、deep golden shard、MingLi full no-leak、policy regression。

# Ship Readiness

- 本计划完成后可进入 implementation goal。
- 进入 implementation 前必须确认是否创建新 `/goal` 或直接消费本任务树。
- 未完成 implementation 前，不得声明八字功能实际已到 100%。

# Task Package Acceptance

| Package | Acceptance |
| --- | --- |
| `TP-01` | 100% 口径、资源边界、验收合同明确。 |
| `TP-02` | 基础排盘和时间边界有足够 oracle/golden/mismatch gate。 |
| `TP-03` | 专业输出强制 evidence 和风险边界。 |
| `TP-04` | 常规规则物理拆分且 schema 稳定。 |
| `TP-05` | 高级格局有 taxonomy、正反边界例和 guarded evaluator。 |
| `TP-06` | 合化状态链可解释、可测试。 |
| `TP-07` | 用神策略评分和冲突裁决可解释。 |
| `TP-08` | 岁运专题只有趋势证据，无确定未来和现实处方。 |
| `TP-09` | golden corpus 分层，release shard 全量可复现。 |
| `TP-10` | benchmark no-leak，失败回炉，不刷答案。 |
| `TP-11` | 维护边界、交付边界、本地 release gate 闭合。 |

# Anti-Goals

- 不得修改 `governance/tasks/` 以外路径。
- 不得虚构证据。
- 不得越权补全未确认信息。
- 不得把准确率阈值写成命理必然正确。
