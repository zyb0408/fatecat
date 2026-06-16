# MingLi Full Evaluation Evidence

## 结论

- 日期：2026-06-16
- 评测范围：FortuneTellingBench / MingLi-Bench 本地 160 题全量
- predictions：160/160
- answered：160/160
- correct：45
- accuracy：28.12%
- 判断：全量评测链路真实可跑，略高于随机四选一基线，但不能证明专业专题推理已经强。

## 执行命令

```bash
bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl
bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json
```

## 输出产物

| 产物 | 路径 | 说明 |
| --- | --- | --- |
| predictions | `/tmp/fatecat-mingli-full.jsonl` | 160 行 FateCat scored baseline 预测 |
| report | `/tmp/fatecat-mingli-full.json` | total/answered/correct/accuracy/byCategory/results 全量评测报告 |

## 全量指标

| 指标 | 值 |
| --- | --- |
| total | 160 |
| answered | 160 |
| missing | 0 |
| correct | 45 |
| accuracy | 0.2812 |

## 分类指标

| 分类 | total | answered | correct | accuracy |
| --- | ---: | ---: | ---: | ---: |
| 事业 | 25 | 25 | 9 | 0.3600 |
| 健康 | 17 | 17 | 4 | 0.2353 |
| 外貌 | 3 | 3 | 2 | 0.6667 |
| 婚姻 | 44 | 44 | 14 | 0.3182 |
| 子女 | 6 | 6 | 2 | 0.3333 |
| 学业 | 11 | 11 | 2 | 0.1818 |
| 官非 | 1 | 1 | 1 | 1.0000 |
| 家庭 | 22 | 22 | 6 | 0.2727 |
| 性格 | 14 | 14 | 4 | 0.2857 |
| 灾劫 | 2 | 2 | 0 | 0.0000 |
| 财运 | 13 | 13 | 1 | 0.0769 |
| 运势 | 2 | 2 | 0 | 0.0000 |

## 答案泄漏检查

检查脚本确认 predictions 只含以下字段：

```text
benchmark_year
category
fatecat_evidence
predicted_answer
prediction_source
question_id
question_number
response
scoring_trace
```

未发现 `expected`、`answer`、`correct`、`ground_truth`、`gold`、`label` 等答案泄漏字段。

## 风险与后续

- 财运、学业、健康、灾劫、运势分类仍弱，不能宣称专业专题推理已经强。
- 该评测是 deep/evaluation gate，实测耗时较长，不适合进入日常 quick CI。
- 下一步 `TP-07.02` 应基于 `/tmp/fatecat-mingli-full.json` 归因失败样本，不能把 benchmark 答案写回规则或 prediction 脚本。
