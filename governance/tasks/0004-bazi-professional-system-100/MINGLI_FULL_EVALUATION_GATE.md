# TP-09.02 MingLi Full 评测门禁

## 结论

- 状态：PASS，带准确率 WARN。
- Full gate 已真实执行，不是 stats-only。
- 评测链路可用，但当前弱规则 baseline 准确率只有 `27.50%`，不能宣称专业推理强。

## 已验证命令

```bash
rm -f /tmp/fatecat-mingli-full.jsonl /tmp/fatecat-mingli-full.json
time (
  bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl &&
  bash scripts/run-mingli-bench.sh \
    --predictions-file /tmp/fatecat-mingli-full.jsonl \
    --output-json /tmp/fatecat-mingli-full.json
)
```

结果：

```text
{"predictions": 160, "output": "/tmp/fatecat-mingli-full.jsonl", "source": "fatecat_scored_baseline_v1"}
Evaluation:
  Answered: 160/160
  Correct: 44
  Accuracy: 27.50%

real  5m45.770s
```

输出产物：

```text
/tmp/fatecat-mingli-full.jsonl 305835 bytes 2026-06-16 23:12:24 +0800
/tmp/fatecat-mingli-full.json 38126 bytes 2026-06-16 23:12:24 +0800
160 /tmp/fatecat-mingli-full.jsonl
```

## 泄漏检查

检查脚本确认 prediction JSONL 顶层没有标准答案字段：

```json
{
  "predictionRows": 160,
  "forbiddenTopLevelLeakCount": 0,
  "evaluationTotal": 160,
  "answered": 160,
  "missing": 0,
  "correct": 44,
  "accuracy": 0.275,
  "predictionTopLevelKeys": [
    "benchmark_year",
    "category",
    "fatecat_evidence",
    "predicted_answer",
    "prediction_source",
    "question_id",
    "question_number",
    "response",
    "scoring_trace"
  ]
}
```

禁止进入 predictions 的字段：

- `expected`
- `answer`
- `correct`
- `gold`
- `label`

## 性能修复

发现 `mingli_baseline.generate_predictions()` 对同一出生盘重复计算。MingLi-Bench 当前是 160 题、32 个唯一出生输入，本轮已在 evaluation 层加入按出生输入的排盘缓存。

缓存 key 只包含：

- 出生年月日时分
- 性别
- 经纬度
- 出生地
- 真太阳时开关

缓存 key 不包含：

- `question_id`
- 题干
- 选项
- `answer`
- 正误结果

## 回归证据

```bash
.venv/bin/python -m ruff format --check \
  domains/fate-analysis/services/fate-core/src/fate_core/evaluation/mingli_baseline.py \
  tests/regression/test_mingli_bench_gate.py

.venv/bin/python -m pytest tests/regression/test_mingli_bench_gate.py -q

.venv/bin/python -m pytest \
  tests/regression/test_bazi_golden_coverage_matrix.py \
  tests/regression/test_mingli_bench_gate.py -q
```

结果：

```text
2 files already formatted
3 passed in 11.54s
12 passed, 1 skipped in 39.71s
```

## 边界

- `27.50%` 只是 FateCat weak-rule baseline 的当前样本外准确率。
- 该结果不支持“专业专题推理已强”的结论。
- 后续提升必须进入 `MINGLI_FAILURE_TAXONOMY`，不能按 question_id 或标准答案硬编码规则。
