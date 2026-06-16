# Calendar Oracle Audit

任务节点：`TP-02.01`

## 结论

- `PASS`：当前历法 oracle 只在测试/评估链路使用，未进入 `fate-core` 或 `fatecat-delivery` 生产源码。
- `PASS`：`lunar-python` 是唯一允许进入生产主链的历法依赖；`sxtwl`、`bazica`、`bazi-calculator-by-alvamind` 均被限定为 oracle/reference。
- `WARN`：`calendar_boundary_cases.json` 现有 4 条样本缺少逐条 `source`、`failureExplanation`、`privacy`、`license` 字段；这不阻塞本节点的 oracle 隔离审计，但阻塞 `TP-02.02` 的时间边界 golden 扩展。

## 已验证命令

```bash
.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
```

结果：

```text
10 passed in 71.82s
```

## 覆盖范围

### Oracle 隔离

实现文件：

- `tests/regression/test_calendar_oracle_contract.py`
- `tools/reference-repos/vendor_sources.json`

已验证约束：

- `sxtwl` 只出现在 regression oracle 测试中。
- 生产源码根禁止出现 `import sxtwl`、`from sxtwl`、`bazica`、`bazi-calculator-by-alvamind`。
- `vendor_sources.json` 中：
  - `lunar-python`: `production_dependency`, `productionUseAllowed=true`
  - `sxwnl`: `oracle_only`, `productionUseAllowed=false`
  - `bazica`: `oracle_only`, `productionUseAllowed=false`
  - `bazi-calculator-by-alvamind`: `reference_only`, `productionUseAllowed=false`

### 节气 golden

实现文件：

- `domains/fate-analysis/data-products/calendar/solar_terms/golden/solar_terms_1900_2030.json`
- `tests/regression/test_solar_terms_golden.py`

已验证约束：

- fixture 覆盖 1900-2030 年，24 节气/年，总计 3144 行。
- fixture 来源记录 SHA256：`76585429b1af2d4b9b66bf06c6eaf7ce8696a76b47fd18b1f27497df8d4759e4`。
- 测试校验 lunar-python 与 golden fixture 的节气时间差在声明容差内。
- 测试锁定 1936、1969、2000、2024、2030 年的月柱交节变化。
- 测试锁定立春前后年柱变化。

### 八字时间边界

实现文件：

- `domains/fate-analysis/data-products/bazi/golden/calendar_boundary_cases.json`
- `tests/regression/test_solar_terms_golden.py`

现有样本：

- `beijing_early_zi_2000`
- `beijing_late_zi_2000`
- `urumqi_lichun_2024`
- `hong_kong_utc_input`

已覆盖语义：

- 真太阳时偏移。
- 早子时/晚子时。
- 立春前后年柱/月柱边界。
- UTC 输入归一化到 `Asia/Hong_Kong`。
- 起运时间回归。

## 缺口转交

`TP-02.02` 必须补齐：

- 每条 boundary case 的 `source`。
- 每条 boundary case 的 `expected` 生成依据。
- 每条 boundary case 的 `failureExplanation`。
- 每条 boundary case 的 `privacy` 和 `license` 说明。
- 至少新增覆盖：
  - 非东八区输入。
  - 节气前后秒级边界。
  - 经纬度极端偏移但仍在有效范围的样本。
  - 男/女顺逆起运差异边界。

## Gate 判定

- `oracle 只用于测试/评估`：`PASS`
- `差异样本有 failureExplanation`：`WARN`

说明：本节点没有发现 oracle 与 production 主链的差异失败样本；但已有 boundary fixture 缺少逐条 failure explanation。按任务树责任边界，`TP-02.01` 记录为通过并携带 `TP-02.02` 必修缺口。
