# AGENTS.md - fate_core.evaluation

## 目录用途

`evaluation/` 承载离线 benchmark、样本外评测和预测基线生成逻辑。它只读取领域用例输出，不反向参与生产排盘结论。

## 目录结构

```text
evaluation/
├── AGENTS.md
├── __init__.py
└── mingli_baseline.py
```

## 职责边界

- `mingli_baseline.py`：读取本地 MingLi-Bench 数据，调用 `calculate_pure_analysis` 生成可评测 predictions，并输出打分证据。
- 评测 baseline 必须标明能力边界；不得把弱规则命中伪装成专业准确率。
- 不读取 benchmark 标准答案参与预测；准确率只由独立 evaluator 计算。
- 不联网，不调用外部模型 API，不写回 vendor 数据。

## 依赖方向

- `evaluation -> usecases`
- `scripts/generate-mingli-predictions.sh -> evaluation.mingli_baseline`
- 禁止 `usecases/kernel/providers` 反向依赖 `evaluation`。

