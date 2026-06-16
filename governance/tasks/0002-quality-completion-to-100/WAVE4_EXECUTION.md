# Wave 4 Execution Evidence

日期：2026-06-16

## Scope

Wave 4 覆盖：

- `TP-11.02` MingLi-Bench 从 evaluator smoke 升级为 FateCat prediction eval
- `TP-11.03` local-ci profile 与证据目录固化
- `TP-12.02` 大文件职责切片
- `TP-13.03` Bot outbox/live 恢复路径

## Command Evidence

| Node | Command | Result |
| --- | --- | --- |
| TP-11.02 | `bash scripts/generate-mingli-predictions.sh --year 2025 --sample 2 --output-jsonl <tmp>/predictions.jsonl` | PASS：生成 `2` 条 `fatecat_scored_baseline_v1` predictions。 |
| TP-11.02 | `bash scripts/run-mingli-bench.sh --year 2025 --sample 2 --predictions-file <tmp>/predictions.jsonl --output-json <tmp>/evaluation.json` | PASS：answered `2/2`，accuracy `100.00%`。只作为小样本回归，不作为专业准确率声明。 |
| TP-11.02 | `bash scripts/generate-mingli-predictions.sh --year 2025 --sample 10 --output-jsonl <tmp>/predictions.jsonl && bash scripts/run-mingli-bench.sh --year 2025 --sample 10 --predictions-file <tmp>/predictions.jsonl --output-json <tmp>/evaluation.json` | PASS/WARN：answered `10/10`，accuracy `30.00%`。链路真实，baseline 仍弱。 |
| TP-11.02 | `.venv/bin/python -m pytest tests/regression/test_mingli_bench_gate.py tests/regression/test_bazi_golden_coverage_matrix.py -q` | PASS：`11 passed, 1 skipped in 51.46s`。 |
| TP-11.03 | `bash scripts/local-ci.sh --profile all` | PASS：evidence `/tmp/fatecat-local-ci-20260616012307`。 |
| TP-12.02 | `find domains/experience-delivery/services/fatecat-delivery/src domains/fate-analysis/services/fate-core/src -name '*.py' -print0 \| xargs -0 wc -l \| sort -nr \| head -25` | WARN：核心大文件仍存在，见下表。 |
| TP-13.03 | `.venv/bin/python -m pytest domains/experience-delivery/services/fatecat-delivery/tests/test_bot_send_queue.py -q` | PASS：`2 passed in 0.44s`。 |

## TP-11.02 Result

新增 `fate_core.evaluation.mingli_baseline`，并把 `scripts/generate-mingli-predictions.sh` 收缩为薄封装：

- 输入：本地 MingLi-Bench 数据。
- 处理：调用 FateCat `calculate_pure_analysis` 生成盘面证据，再按题目类别、选项关键词、topicProfiles、干支关系压力和岁运触发输出 scored baseline predictions。
- 输出：JSONL，可直接交给 `scripts/run-mingli-bench.sh --predictions-file`。
- 边界：不调用外部模型 API；不宣称专业准确率；粗粒度地点 fallback 只用于 benchmark baseline，不用于生产 geocoding。
- 维护性：评测逻辑进入 `domains/fate-analysis/services/fate-core/src/fate_core/evaluation/`，脚本从 `214` 行降至 `71` 行。

本轮真实评测结果：

- sample 2：answered `2/2`，correct `2`，accuracy `100.00%`
- sample 5：answered `5/5`，correct `3`，accuracy `60.00%`
- sample 10：answered `10/10`，correct `3`，accuracy `30.00%`
- missing：0

结论：MingLi-Bench 已从手写 evaluator smoke 和 hash baseline 升级为 FateCat-generated scored baseline；但 sample 10 只有 `30%`，仍只能证明可解释评测链路，不证明专业推理准确率。

## TP-11.03 Result

`bash scripts/local-ci.sh --profile all` 通过，证据目录：

```text
/tmp/fatecat-local-ci-20260616012307
```

关键结果：

- shell syntax / preflight / structure / source hygiene / privacy fixtures：PASS
- ruff check / ruff format / mypy：PASS
- focused regression：`47 passed`
- full pytest：`169 passed, 1 skipped in 247.47s`
- delivery API smoke：PASS
- delivery Bot dry-run smoke：PASS
- export lite / exported hygiene / exported preflight：PASS
- Docker image build：PASS
- container `/web` smoke：PASS
- public-service static readiness：PASS
- live API/Bot：SKIP，缺真实 `--api-url` 与 `--require-live-bot`

## TP-12.02 Result

当前最大 Python 文件：

| Lines | File |
| ---: | --- |
| 2500 | `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py` |
| 1941 | `domains/experience-delivery/services/fatecat-delivery/src/report_generator.py` |
| 1375 | `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py` |
| 1152 | `domains/experience-delivery/services/fatecat-delivery/src/bot.py` |
| 1067 | `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_ziwei.py` |
| 1015 | `domains/experience-delivery/services/fatecat-delivery/src/main.py` |
| 782 | `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py` |

结论：WARN。

已经有拆分进展：

- `fate_core/kernel/bone_weight.py`
- `fate_core/kernel/ming_gua.py`
- `fate_core/kernel/solar_time.py`
- `fate_core/usecases/evidence_builder.py`
- delivery `bot_logging.py`
- delivery `report_markdown.py`
- delivery `service_config.py`
- delivery `web_forms.py`

但还不能宣称大文件治理 100%。后续必须按计算、报告、Web 呈现、Bot 交付、观测防护继续切片，并保持 API/Web/Bot 输出不漂移。

## TP-13.03 Result

Bot 本地 outbox 幂等入队、原子保存和 ACK 删除测试通过。真实 Telegram live 恢复仍需要真实 `FATE_BOT_TOKEN`，不得在本地 dry-run 中宣称 live 通过。

## Wave 4 Status

| Node | Status | Evidence | Next |
| --- | --- | --- | --- |
| TP-11.02 | Done with accuracy WARN | FateCat-generated scored baseline + evaluator 通过；sample 10 accuracy `30%`。 | 后续需要真正的专题推理器，不是弱关键词 baseline。 |
| TP-11.03 | Done | local-ci all PASS，证据目录 `/tmp/fatecat-local-ci-20260616012307`。 | 可作为当前本地 CI/CD 主证据。 |
| TP-12.02 | WARN | line-count map 已生成；仍有 1000+ 行大文件。 | 继续切 bazi kernel、report、pure_analysis、bot、main、web_ui。 |
| TP-13.03 | Done with HITL note | Bot outbox tests `2 passed`。 | live Bot 仍需真实 token。 |

## Next Wave Gate

进入 Wave 5：

- `TP-15.01` 六维 auto-review。
- `TP-15.02` 处理 BLOCK/WARN。
- `TP-15.03` closeout 与交付证据。
