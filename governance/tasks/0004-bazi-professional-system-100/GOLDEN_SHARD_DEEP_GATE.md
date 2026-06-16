# TP-09.01 Golden Shard 与 Deep Gate

## 结论

- 状态：PASS，带性能 WARN。
- Gate：全量 300+ golden 不进入日常 quick；deep/release 使用分片环境变量复现。
- 当前证据：shard `0/4` 可独立通过。

## 已验证命令

```bash
FATECAT_RUN_FULL_GOLDEN_MATRIX=1 \
FATECAT_GOLDEN_SHARD_TOTAL=4 \
FATECAT_GOLDEN_SHARD_INDEX=0 \
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
```

结果：

```text
10 passed in 629.63s (0:10:29)
```

## 代码证据

- `tests/regression/test_bazi_golden_coverage_matrix.py`：
  - 默认只跑 requiredTags representative cases。
  - `FATECAT_RUN_FULL_GOLDEN_MATRIX=1` 才开启 300+ 全量慢测。
  - `FATECAT_GOLDEN_SHARD_TOTAL` / `FATECAT_GOLDEN_SHARD_INDEX` 支持 release/deep 分片。
  - `test_bazi_golden_coverage_matrix_shards_cover_all_cases_without_overlap` 证明 4 shard 覆盖全集且不重叠。

## 边界

- `0/4` shard 通过不等于所有 shard 已在本轮跑完。
- shard 单片耗时约 10 分半，不能进入 quick CI。
- release gate 应跑 4 个 shard，或在可接受时间窗口内跑 full matrix。
