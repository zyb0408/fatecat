# Calendar Boundary Matrix

任务节点：`TP-02.01`

## 结论

当前 `calendar_boundary_cases.json` 已满足本轮基础排盘边界 gate：9 个 synthetic fixture 覆盖早晚子时、立春秒级边界、真太阳时、跨时区、DST、非整点时区、女性起运和起运锚点。

本节点不新增无来源样本；现有样本已经覆盖 `TP-02.01` 所列边界，后续新增只在发现 oracle mismatch 或真实边界缺口时进行。

## 覆盖要求

| 要求 | 当前状态 |
| --- | --- |
| minCaseCount >= 9 | PASS |
| early_zi | PASS |
| late_zi | PASS |
| lichun_boundary | PASS |
| second_level_boundary | PASS |
| utc_input | PASS |
| timezone_normalization | PASS |
| non_whole_hour_timezone | PASS |
| dst_boundary | PASS |
| gender_female | PASS |
| fortune_start | PASS |
| true_solar_time | PASS |

## 样本 ID

| Case ID | 覆盖重点 |
| --- | --- |
| `beijing_early_zi_2000` | 早子时、真太阳时、起运 |
| `beijing_late_zi_2000` | 晚子时、子初换日、起运 |
| `urumqi_lichun_2024` | 立春边界、极端经度偏移、起运 |
| `hong_kong_utc_input` | UTC 输入、时区归一化、真太阳时 |
| `beijing_lichun_second_before_2024` | 立春秒级前边界 |
| `beijing_lichun_second_after_2024` | 立春秒级后边界 |
| `new_york_dst_utc_input_2024` | DST、非东八区、西经输入 |
| `kathmandu_quarter_timezone_2000` | 非整点时区、跨日真太阳时 |
| `beijing_female_yun_start_2024` | 女性起运方向、立春边界 |

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
```

Result:

```text
10 passed in 160.10s
```

## Gate 判定

- `新增/现有样本都有 source`：`PASS`
- `新增/现有样本都有 expected`：`PASS`
- `新增/现有样本都有 tolerance 或 failureExplanation`：`PASS`
- `requiredTags 全部被 observedTags 覆盖`：`PASS`
