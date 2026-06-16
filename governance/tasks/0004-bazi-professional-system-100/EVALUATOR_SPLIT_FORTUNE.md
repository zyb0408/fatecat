# TP-10.01 Evaluator 物理拆分：fortune

## 结论

- 状态：PASS。
- 本轮只抽一个 evaluator：`fortuneTriggerMatrix`。
- 行为边界：输出 schema、字段名、风险边界、API/Web/Bot 可见结果保持不变。
- Delivery 边界：`domains/experience-delivery` 未新增领域算法或 evaluator 依赖。

## 重构规则来源

- `auto-refactor/references/agent-rules-books/refactoring/refactoring.md`
- `auto-refactor/references/agent-rules-books/refactoring-guru/refactoring-guru.md`
- `auto-refactor/references/agent-rules-books/working-effectively-with-legacy-code/working-effectively-with-legacy-code.md`
- `auto-refactor/references/agent-rules-books/a-philosophy-of-software-design/a-philosophy-of-software-design.md`
- `auto-refactor/references/future-optimal-refactor.md`
- `auto-refactor/references/ponytail-simplification-patterns.md`

## Target End State

`calculate_pure_analysis.py` 只负责编排 providers、evaluator 和 evidence builder；pattern、hehua、yongshen、fortune、topic 等专业 evaluator 逐步进入 `fate_core/usecases/evaluators/`。

## 本轮切片

新增：

```text
domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/
├── AGENTS.md
├── __init__.py
└── fortune.py
```

迁移：

- 从 `calculate_pure_analysis.py` 移出 `_build_fortune_trigger_matrix`。
- 在 `fortune.py` 中公开 `build_fortune_trigger_matrix(raw, triggers)`。
- `calculate_pure_analysis.py` 改为 import 并调用该 evaluator。

不做：

- 不拆 pattern/hehua/yongshen/topic。
- 不改输出 schema。
- 不新增 registry。
- 不改 delivery。
- 不把 MingLi/BaziQA 评测逻辑接进 production runtime。

## 验证命令

```bash
.venv/bin/python -m ruff format --check \
  domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py \
  domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/__init__.py \
  domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/fortune.py \
  tests/regression/test_bazi_ziwei_rule_depth.py \
  tests/regression/test_api_contracts.py \
  tests/regression/test_bazi_golden_coverage_matrix.py

.venv/bin/python -m pytest \
  tests/regression/test_bazi_ziwei_rule_depth.py \
  tests/regression/test_api_contracts.py \
  tests/regression/test_bazi_golden_coverage_matrix.py -q
```

结果：

```text
6 files already formatted
70 passed, 1 skipped in 106.56s
```

## 边界扫描

```bash
rg -n "build_fortune_trigger_matrix|_build_fortune_trigger_matrix|usecases\\.evaluators|fortuneTriggerMatrix" \
  domains/fate-analysis/services/fate-core/src \
  domains/experience-delivery/services/fatecat-delivery/src
```

结果要点：

- `calculate_pure_analysis.py` 调用 `build_fortune_trigger_matrix`。
- `usecases/evaluators/fortune.py` 定义 evaluator。
- `domains/experience-delivery` 无新增命中。
- 旧 `_build_fortune_trigger_matrix` 已不存在。

## 行数变化

```text
2101 calculate_pure_analysis.py
58   usecases/evaluators/fortune.py
5    usecases/evaluators/__init__.py
32   usecases/evaluators/AGENTS.md
```

## Rollback Boundary

如本切片失败，只需把 `build_fortune_trigger_matrix` 函数移回 `calculate_pure_analysis.py` 并移除 `usecases/evaluators/fortune.py` 调用；不影响其他 evaluator。

## 后续

后续只能按任务树继续一次迁移一个 evaluator。优先候选：

- `topic`
- `yongshen`
- `hehua`
- `pattern`

每个候选都必须先跑 API contract、rule-depth 和 golden representative regression。
