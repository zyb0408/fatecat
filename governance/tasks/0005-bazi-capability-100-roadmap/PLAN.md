# Planning Summary

目标不是继续堆功能，而是把十个维度分别收敛到可验证的 100% gate。正确终态是：

- 生产排盘只依赖稳定 provider。
- oracle、benchmark、参考仓不进入 runtime。
- 专业规则全部可追溯、可反证、可测试。
- 高级格局和专题推理必须有 lifecycle，缺样本时保持 beta/HITL。
- quick、deep、release gate 分层，日常速度和发布严谨性不互相破坏。

# Lifecycle Gates

不得跳过 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 任何 gate；未闭合 gate 的任务不得进入后续实现或 closeout。

| Gate | 要求 |
| --- | --- |
| SPEC | 每个维度定义 100% 目标、禁止路径和 falsifier。 |
| PLAN | 任务拆成 TP leaf，显式依赖和波次。 |
| BUILD | 每个 leaf 只实现一个规则/evaluator/corpus/评测切片。 |
| TEST | 绑定 pytest、rg、benchmark、no-leak、policy regression。 |
| REVIEW | PASS/WARN/BLOCK，WARN 必须有 owner 和 next step。 |
| SHIP | local quick/full/deep gate 通过，Active BLOCK=0。 |

# Simplest Path

1. 先补 `TP-01`，把 100% gate 写死，防止后续口径漂移。
2. 再补 `TP-02` 和 `TP-03`，因为排盘和证据是后续所有规则的地基。
3. 再按规则难度推进 `TP-04` 到 `TP-08`。
4. 最后做 `TP-09`/`TP-10`，用 deep golden 和 benchmark 证明没有倒退。
5. `TP-11` 收维护边界和交付边界。

# Split Strategy

- 按能力面 vertical slice 拆，不按“先改 schema 再写测试再写报告”水平拆。
- 每个 slice 必须包含：规则合同、evaluator、golden、API/Web/Markdown 影响检查、policy gate。
- 每个高风险 topic 先 policy regression，再允许报告展示。
- 每个 benchmark 提升都必须先证明 no-leak。

# Execution Waves

| Wave | Leaf | 说明 |
| --- | --- | --- |
| 1 | `TP-01.01`、`TP-01.02` | 基线与资源复核，可并行。 |
| 2 | `TP-01.03` | 统一 100% gate。 |
| 3 | `TP-02.01`、`TP-02.02` | provider 合同和边界 corpus。 |
| 4 | `TP-02.03` | oracle mismatch report。 |
| 5 | `TP-03.01`、`TP-03.02` | rule/evidence schema。 |
| 6 | `TP-03.03` | 高风险 policy。 |
| 7 | `TP-04.01`、`TP-04.02` | 常规 evaluator 双切片。 |
| 8 | `TP-04.03` | pattern/relation。 |
| 9 | `TP-05.01`、`TP-06.01`、`TP-07.01` | 高级格局、合化、用神合同。 |
| 10 | `TP-05.02`、`TP-06.03`、`TP-07.03` | 正反例和反例矩阵。 |
| 11 | `TP-05.03`、`TP-06.02`、`TP-07.02` | evaluator 实现。 |
| 12 | `TP-08.01` | 岁运 trigger chain。 |
| 13 | `TP-08.02`、`TP-08.03` | 专题 profile 和 policy。 |
| 14 | `TP-09.01`、`TP-09.02` | corpus 和 shard gate。 |
| 15 | `TP-09.03` | mutation/schema regression。 |
| 16 | `TP-10.01`、`TP-10.02` | MingLi full 和 failure backlog。 |
| 17 | `TP-10.03` | BaziQA admission。 |
| 18 | `TP-11.01`、`TP-11.02` | 维护和交付边界。 |
| 19 | `TP-11.03` | final release gate。 |

# Runtime Workflow Contract

- Allowed tools: local filesystem, local pytest/ruff/mypy/scripts, web research against primary sources.
- Forbidden actions: push remote, run GitHub Acceptance, copy benchmark answers into production logic, connect oracle/evaluation datasets to runtime.
- Evidence required: file diff, verification command output, benchmark JSON summary, no-leak scan, final review.
- Stop conditions: answer leakage, production import of evaluation/oracle resources, high-risk deterministic output, license/source unclear but marked production.

# Next Executable Leaves

- `TP-10.02`
- `TP-10.03`

# Dependency Graph

```text
TP-01.01 + TP-01.02 -> TP-01.03
TP-01.03 -> TP-02.01, TP-02.02, TP-03.01, TP-03.02
TP-02.01 + TP-02.02 -> TP-02.03
TP-03.01 + TP-03.02 -> TP-03.03
TP-02.03 + TP-03.03 -> TP-04.*
TP-04.03 -> TP-05.*, TP-06.*, TP-07.*
TP-05.03 + TP-06.02 + TP-07.02 -> TP-08.*
TP-08.03 -> TP-09.*, TP-10.*
TP-09.03 + TP-10.03 -> TP-11.*
```

# Rollback Protocol

- 恢复 `INDEX.md` 当前任务行。
- 恢复本任务目录到初始化状态。
- 不得影响其他任务目录。
