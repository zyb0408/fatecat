# Benchmark Gate Policy

## 结论

- 当前 full MingLi baseline：160 answered / 45 correct / 28.12% accuracy。
- 该分数只说明全量评测链路可运行，不能作为专业能力完成声明。
- MingLi-Bench 是 `evaluation_only`，不得进入生产请求链路，不得把 expected answer 写回规则或预测脚本。

## 当前 Baseline

| 指标 | 当前值 | 证据 |
| --- | ---: | --- |
| total | 160 | `/tmp/fatecat-mingli-full.json` |
| answered | 160 | `MINGLI_FULL_EVALUATION.md` |
| correct | 45 | `MINGLI_FULL_EVALUATION.md` |
| accuracy | 28.12% | `MINGLI_FULL_EVALUATION.md` |
| weakest category | 财运 7.69% | `MINGLI_FAILURE_TAXONOMY.md` |
| failure count | 115 | `MINGLI_FAILURE_TAXONOMY.md` |

## Gate 分层

| gate | 命令 | 用途 | 通过条件 |
| --- | --- | --- | --- |
| smoke | `.venv/bin/python -m pytest tests/regression/test_mingli_bench_gate.py -q` | 日常确认评测脚本可运行 | predictions/evaluation smoke 通过 |
| sample baseline | `bash scripts/generate-mingli-predictions.sh --year 2025 --sample 10 --output-jsonl /tmp/fatecat-mingli-sample.jsonl && bash scripts/run-mingli-bench.sh --year 2025 --sample 10 --predictions-file /tmp/fatecat-mingli-sample.jsonl --output-json /tmp/fatecat-mingli-sample.json` | 快速观察近期题型 | 只作提示，不作为 release gate |
| full deep | `bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json` | deep/eval gate | 输出 total/answered/correct/accuracy/byCategory/results，且 predictions 无答案泄漏 |

## 下一门槛

| 阶段 | 目标 | 说明 |
| --- | --- | --- |
| P0 next | overall accuracy >= 32% | 先要求超过当前 28.12%，但不得以硬编码方式提高 |
| P0 next | 财运 accuracy >= 15% | 当前 7.69%，必须优先补财星/食伤/用神/岁运联合评分 |
| P0 next | 婚姻 failures <= 25 | 当前 30 个失败，优先补配偶星、关系链和岁运触发 |
| P1 next | 学业 accuracy >= 25% | 当前 18.18%，补印星/食伤/阶段运势 |
| P1 next | 性格/外貌明确 lifecycle | 当前 alias 覆盖不足，应转 beta profile 或 unsupported |

## 回退条件

- full accuracy 低于 28.12%，且不能由规则边界变严解释。
- answered 低于 160。
- predictions 出现 `expected`、`answer`、`correct`、`ground_truth`、`gold`、`label` 等答案字段。
- 任一 category 的 accuracy 因 unrelated 改动大幅下降，且没有 `MINGLI_FAILURE_TAXONOMY.md` 归因。
- 评测脚本开始读取 benchmark answer 影响 prediction。

## 不达标处理

- 不阻塞本地 quick CI；MingLi full 属于 deep/evaluation gate。
- 不达标时不得宣称八字专业推理增强。
- 必须更新 `MINGLI_FAILURE_TAXONOMY.md`，说明 regressions 属于缺规则、缺时间触发、缺格局、缺用神还是题目语义歧义。
- 如为 intentional boundary hardening 导致准确率下降，必须在任务证据中说明原因，并给出后续恢复路径。

## 禁止刷分

- 禁止按 `question_id`、expected answer、选项字面答案硬编码。
- 禁止把 MingLi 题库作为生产规则来源。
- 禁止只优化 sample 10 后宣称 full benchmark 改进。
- 禁止以删除高风险边界换取更高 accuracy。

## 发布口径

- 当前允许口径：`MingLi full evaluation connected; current scored baseline is 28.12%.`
- 当前禁止口径：`专业命理推理已强`、`MingLi 已达生产标准`、`八字体系 100% 准确`。
