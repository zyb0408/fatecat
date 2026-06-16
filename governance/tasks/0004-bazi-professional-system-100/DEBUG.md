# Debug Evidence

## Bug

本任务不是单一崩溃 bug，而是八字专业体系 100% 推进中的高风险质量闭环。当前已知问题是：上一轮 `0003-bazi-system-100` 只达到工程验收 `PASS with WARN`，专业推理、真实样本外 benchmark、高级格局、合化、用神、岁运专题仍未达到 100% 验收口径。

需要防止的具体失败：

- 把工程验收 100% 误写成预测准确率 100%。
- 把 MingLi/BaziQA expected answer、question_id 或选项答案写入生产规则。
- 把 oracle/evaluation/reference 资源引入生产请求链路。
- 在报告中输出无 `sourceRuleId`、无 `evidenceFields`、无 `riskBoundary` 的专业断语。
- 高风险专题输出医疗、金融、法律、心理替代建议或确定未来。

## Environment

- Repository: `/home/lenovo/.projects/fatecat`
- Task directory: `governance/tasks/0004-bazi-professional-system-100`
- Current branch: `main`
- Prior task baseline: `governance/tasks/0003-bazi-system-100`
- Production algorithm boundary: `domains/fate-analysis/services/fate-core`
- Delivery boundary: `domains/experience-delivery/services/fatecat-delivery`
- Contracts boundary: `contracts/fate`
- Golden boundary: `domains/fate-analysis/data-products/bazi/golden`
- Evaluation boundary: `domains/fate-analysis/services/fate-core/src/fate_core/evaluation`

## Reproduction

当前缺口可由以下证据复现：

```bash
sed -n '1,220p' governance/tasks/0003-bazi-system-100/FINAL_REVIEW.md
sed -n '1,220p' governance/tasks/0003-bazi-system-100/MINGLI_FULL_EVALUATION.md
sed -n '1,260p' governance/tasks/0003-bazi-system-100/MINGLI_FAILURE_TAXONOMY.md
```

关键现象：

- `FINAL_REVIEW.md` 明确：工程验收 `PASS with WARN`，专业命中率未达强推理口径。
- `MINGLI_FULL_EVALUATION.md` 明确：MingLi full `160 answered / 45 correct / 28.12% accuracy`。
- `MINGLI_FAILURE_TAXONOMY.md` 明确：失败集中在婚姻、事业、家庭、健康、财运、学业等专题。
- 2026-06-16 执行 `TP-03.01` verify 时，`tests/regression/test_bazi_ziwei_rule_depth.py::test_rule_depth_is_available_from_api_and_web_without_frontend_recalculation` 失败；旧断言要求 Web 不显示“上海”，但当前产品口径已经要求提交后的出生地区必须显示。

## Observations

- 基础排盘和历法时间已经接近成熟，但仍缺更多边界样本、oracle 差异归因和升级合同。
- 证据化已经有 `rule_depth_registry.json`、`classics_rule_index.json`、`analysisEvidence` 和 `baziRuleDepth`，但报告/API 还需要做到所有专业结论可反查。
- 高级格局、合化成败、用神裁决和岁运专题是当前专业体系短板。
- Golden 回归已有 300+ coverage matrix，但高级规则、专题 profile、反例和真实专家命例不足。
- MingLi full 链路可跑，但 28.12% baseline 只能证明评测链路接通，不能证明专业推理强。
- 当前正确路线是补 FateCat 自己的规则证据层，而不是换一个开源库或使用 LLM prompt 直接强断。
- `TP-03.01` 测试失败不是 Web 业务回归，而是旧隐私断言未同步到“出生地区显示”新口径。

## Hypotheses

### H1 (ROOT HYPOTHESIS): 专业 100% 的根因缺口是规则证据闭环不完整

- Supports: 高级格局、合化、用神、岁运专题仍以 beta/guarded/evidence_seed 为主；MingLi 失败集中在专题推理而不是基础排盘。
- Conflicts: 如果补完规则证据、反例、golden、topic profile 后 MingLi 分类和报告可解释性仍无改善，则该假设需要重审。
- Test: 执行 TP-03 到 TP-09，观察 rule-depth、API contract、topic profile、golden 和 MingLi full 是否同步改善。

### H2: 基础排盘不是当前最大瓶颈，但边界样本不足会阻碍 100% 验收

- Supports: 当前基础排盘约 93%、历法时间约 90%，主要缺口是节气秒级、立春、早晚子时、真太阳时、跨时区、DST、起运边界。
- Conflicts: 如果新增 calendar boundary 后出现大量核心排盘差异，则基础排盘风险被低估。
- Test: 执行 TP-02 并运行 calendar oracle、solar terms golden 和 bazi coverage matrix。

### H3: benchmark 提升必须来自规则能力，而不是答案拟合

- Supports: MingLi 当前 28.12%，失败有分类 owner；硬编码答案会破坏样本外真实性。
- Conflicts: 如果 prediction 文件出现 expected/answer/correct/gold/label 字段或 question_id 特化逻辑，则该路线失败。
- Test: 执行 TP-09，检查 predictions 字段、failure taxonomy 和 no-leak regression。

### H4: 维护性不收敛会让规则能力继续堆入大文件

- Supports: `bazi_calculator.py`、`calculate_pure_analysis.py`、`report_generator.py` 仍承担过多职责。
- Conflicts: 如果新增规则全部能独立进入 evaluator 且大文件不再承载新领域逻辑，则维护性风险下降。
- Test: 执行 TP-10.01，确保 pattern/hehua/yongshen/fortune/topic evaluator 按行为保持测试抽取。

### H5: Web 地区显示失败来自过期测试口径

- Supports: 用户已明确要求出生地区显示；`/web` 实际输出包含提交的“上海”；失败断言是 `assert "上海" not in ziwei_web.text`。
- Conflicts: 如果 Web 输出出现“非北京地区已隐藏”或泄露非提交样例，则不是单纯测试口径问题。
- Test: 修改断言为提交地区必须显示且旧隐藏文案不得出现，重跑 rule-depth / policy 组合测试。

## Experiments

- Calendar gate:

```bash
.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
```

- Rule-depth / evidence gate:

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
```

- Golden deep gate:

```bash
FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 FATECAT_GOLDEN_SHARD_INDEX=0 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
```

- MingLi full gate:

```bash
bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl
bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json
```

## Root Cause

待执行任务树后更新。当前阶段的根因假设是 H1：专业 100% 的核心不是排盘库缺失，而是规则证据闭环、反例矩阵、专题 profile、样本外失败归因和维护边界没有全部闭合。

## Fix

待各叶子节点执行后逐项记录。当前已完成的修复是创建 `0004-bazi-professional-system-100` 任务容器，并把 10 个专业维度拆成可执行任务树。

- `TP-03.01`：更新过期地区隐私断言，Web 提交地区应显示，旧“非北京地区已隐藏”文案不得回潮。

## Regression Evidence

待每个叶子节点执行后补充：

- leaf id
- command
- result
- evidence path
- remaining risk

## Stop Rules

- 发现 benchmark answer leakage：立即停止 benchmark 提升任务，回滚泄漏路径，补防泄漏测试。
- 发现无法解释的核心排盘差异：停止相关 evaluator 或 provider 变更，先完成 oracle/root-cause 说明。
- 发现高风险输出越界：停止报告发布，先补 policy regression。
- 发现资料 license/source 不清：相关规则只能停在 reference/beta/HITL，不能升 production。
