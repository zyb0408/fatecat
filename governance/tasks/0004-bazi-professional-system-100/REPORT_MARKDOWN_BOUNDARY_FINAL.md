# TP-10.02 报告字段与 Markdown 边界收口

## 结论

- 状态：PASS。
- API 专业字段合同继续保留 `evidenceFields` / `riskBoundary`。
- Markdown 默认报告不展示高风险 topic profile。
- Web 工作台只展示后端结构化字段，不直接调用 fate-core evaluator 或 rule registry。

## 本轮修复

问题：

- Web 工作台原先直接 dump `baziRuleDepth` JSON。
- 该 JSON 包含 evaluator 内部 `lifecycleGate` 等治理字段，违反“报告/前端只展示公开证据字段”的边界。

修复：

- `web_ui.py` 新增 `_rule_depth_summary_rows()`。
- “规则深度 / 冲突策略”只渲染：
  - `ruleId`
  - `topic`
  - `status`
  - `confidence`
  - `evidenceFields`
  - `riskBoundary`
- 不再原样暴露完整 rule-depth JSON。

## 新增回归

`tests/regression/test_web_html.py::test_web_page_workbench_does_not_recalculate_domain_rules`

锁定：

- Web 通过 `CapabilityExecutor` 拿结果。
- Web 不直接导入 `fate_core.usecases`。
- Web 不直接导入 `fate_core.usecases.evaluators`。
- Web 不调用 `calculate_pure_analysis`。
- Web 不调用 `rules_for_system()`。
- Web 不调用 `build_fortune_trigger_matrix`。
- Web 源码不写 `bazi.depth.` 规则生成逻辑。

## 验证命令

```bash
.venv/bin/python -m ruff format --check \
  domains/experience-delivery/services/fatecat-delivery/src/web_ui.py \
  tests/regression/test_web_html.py

.venv/bin/python -m pytest \
  tests/regression/test_web_html.py \
  tests/regression/test_api_contracts.py \
  tests/regression/test_bazi_statement_golden.py -q
```

结果：

```text
2 files already formatted
46 passed in 70.22s
```

## 页面运行态检查

GET `/web` 生成报告后：

```text
lifecycle: false
lifecycleGate: false
report_markdown: true
```

说明：

- 页面不再泄漏内部生命周期治理字段。
- 页面仍可显示 ruleId / evidenceFields / riskBoundary；这些是可追溯证据，不是前端重算规则。

## 边界

- Markdown 报告仍保持默认保守：不输出高风险 `topicProfiles`。
- Web 工作台可以展示结构化字段摘要，但不能重新推导命理结论。
- 下一轮如新增专业报告段落，必须先补 API field contract 与 Markdown/Web regression。
