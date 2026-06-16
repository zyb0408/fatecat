# CalendarProvider Contract

任务节点：`TP-02.02`

## 结论

`lunar-python` 是 FateCat 八字生产历法底座；`sxtwl`、`sxwnl`、`paipan`、`bazica` 只允许作为 oracle/reference，在测试和离线差异解释中使用，不得进入生产请求链路。

## 生产依赖

| 依赖 | 状态 | 证据 |
| --- | --- | --- |
| `lunar-python>=1.4.8` | production dependency | `pyproject.toml`、`requirements.txt` |
| `lunar-python==1.4.8` | locked | `requirements.lock.txt`、`requirements-dev.lock.txt` |
| `sxtwl>=1.4.10` | oracle dependency | `requirements.txt` |
| `sxtwl==2.0.7` | locked | `requirements.lock.txt`、`requirements-dev.lock.txt` |

## 禁止方向

- `fate_core.kernel`、`fate_core.providers`、`fate_core.usecases` 禁止 import `sxtwl`、`bazica` 或 reference-only 项目。
- `delivery` 禁止新增历法/四柱/真太阳时领域算法，只能调用 fate-core 或渲染结果。
- oracle 结果不得覆盖 production provider 结果；差异必须进入 mismatch report 或 failureExplanation。

## 升级门禁

任一 calendar provider 或 oracle 版本升级必须运行：

```bash
.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_api_contracts.py -q
```

升级失败处理：

- calendar/oracle mismatch 有明确 root cause 或 tolerance：记录后继续。
- mismatch 无法解释：停止升级，回滚依赖或保留旧版本。
- production import 出现 oracle 库：立即回滚。

## Verify

```bash
rg 'lunar-python|sxtwl|oracle_only|CalendarProvider' requirements*.txt pyproject.toml contracts governance tests -n
```

Result:

```text
PASS: 依赖声明、lock、oracle 角色和 CalendarProvider 任务证据均可检索。
```

## Gate 判定

- `生产入口不 import oracle`：`PASS`
- `依赖文件声明与锁文件一致`：`PASS`
- `CalendarProvider 升级门禁明确`：`PASS`
