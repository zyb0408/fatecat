# Golden Deep Gate

任务节点：`TP-02.03`

## 结论

- `PASS`：full golden 不进入 quick；默认回归只跑 requiredTags 代表集，并跳过 300-case 全量 gate。
- `PASS`：deep/release gate 已支持 `FATECAT_GOLDEN_SHARD_TOTAL` / `FATECAT_GOLDEN_SHARD_INDEX` 分片。
- `PASS`：full golden 支持 case-level timing JSON，通过 `FATECAT_GOLDEN_TIMING_JSON` 输出。
- `PASS`：当前 shard 0 在 30 秒单 case 预算内，无 over-budget case。
- `WARN`：shard 0 总耗时约 9 分 38 秒；full 300 case 串行不适合日常 CI，只能作为 deep/release 或并行 shard gate。

## Quick Gate

命令：

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
```

结果：

```text
9 passed, 1 skipped in 29.44s
```

含义：

- quick 会检查 fixture schema、300+ 可追溯性、4-way shard 无重叠，以及 requiredTags 代表集。
- quick 不执行 `test_bazi_golden_coverage_matrix_all_cases_match_current_core`。

## Deep Gate

命令：

```bash
FATECAT_RUN_FULL_GOLDEN_MATRIX=1 \
FATECAT_GOLDEN_SHARD_TOTAL=4 \
FATECAT_GOLDEN_SHARD_INDEX=0 \
FATECAT_GOLDEN_TIMING_JSON=/tmp/fatecat-golden-shard0-timing.json \
FATECAT_GOLDEN_CASE_BUDGET_SECONDS=30 \
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
```

结果：

```text
10 passed in 578.31s (0:09:38)
```

Timing 摘要：

```text
schemaVersion=1
shardTotal=4
shardIndex=0
selectedCaseCount=75
caseBudgetSeconds=30.0
totalElapsedSeconds=548.9449
overBudget=[]
```

最慢样本：

```text
bazi_matrix_145_2021_hanlu_late_zi 16.0279s
bazi_matrix_141_2021_lichun_dawn 15.9499s
bazi_matrix_133_2019_hanlu_late_zi 15.9466s
bazi_matrix_129_2019_lichun_dawn 15.8951s
bazi_matrix_181_2027_hanlu_late_zi 15.4079s
```

## 运行策略

- 日常本地开发：只跑 quick gate。
- 领域规则改动：至少跑相关 regression + one shard deep gate。
- release 前：跑 4 个 shard，可并行：
  - `FATECAT_GOLDEN_SHARD_INDEX=0`
  - `FATECAT_GOLDEN_SHARD_INDEX=1`
  - `FATECAT_GOLDEN_SHARD_INDEX=2`
  - `FATECAT_GOLDEN_SHARD_INDEX=3`
- 如果单 case 超过 `FATECAT_GOLDEN_CASE_BUDGET_SECONDS`，deep gate 失败，并通过 timing JSON 定位具体样本。

## 性能判断

- 当前主要瓶颈是 `calculate_pure_analysis` 全链路重复执行，不是 fixture 读取。
- 75-case shard 在本机约 9-10 分钟；按当前速度估算，300-case 串行约 36-40 分钟。
- 不把 full golden 放进 quick 是正确边界；后续性能优化应优先看 `BaziCalculator` / `calculate_pure_analysis` 中的重复计算和规则装配路径。
