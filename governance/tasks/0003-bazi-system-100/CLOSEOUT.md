# Closeout

任务节点：`TP-10.02`

## 结论

任务包状态：`Done`

本轮已把 FateCat 八字体系从“综合约 76% 的能力估算”推进到“任务树工程验收 100%”：

- 基础排盘、历法边界、证据化、常规分析、高级格局、合化成败、用神裁决、岁运专题、golden/回归、样本外 benchmark 均有任务节点、产物、门禁和证据。
- `100%` 只表示本轮任务树和工程证据闭环完成，不表示预测命中率 100%。
- `FINAL_REVIEW.md` 明确 active BLOCK=0；所有 WARN 均有 owner、evidence 和 next。

## 已交付产物

| 产物 | 用途 |
| --- | --- |
| `SCORECARD.md` | 定义八字 100% 工程口径、维度、verify 和 falsifier。 |
| `BASELINE_EVIDENCE.md` | 固化当前 76% 起点和 MingLi sample 10 基线。 |
| `RESOURCE_MAP.md` | 管理 lunar-python、oracle、reference、MingLi 的生产边界。 |
| `RULE_SOURCE_GAPS.md` | 记录规则来源覆盖和缺口。 |
| `CALENDAR_ORACLE_AUDIT.md` | 固化历法 oracle 只进测试/评估的边界。 |
| `GOLDEN_DEEP_GATE.md` | 定义 300+ golden 的 shard/deep gate 预算。 |
| `MINGLI_FULL_EVALUATION.md` | 记录 MingLi full 160 全量评测结果。 |
| `MINGLI_FAILURE_TAXONOMY.md` | 归因 115 个失败样本和 owner 能力面。 |
| `BENCHMARK_GATE_POLICY.md` | 定义 benchmark baseline、next gate 和禁止刷分规则。 |
| `REPORT_FIELD_CONTRACT.md` | 锁定报告/API/Web 暴露字段和风险边界。 |
| `CORE_FILE_BURNDOWN.md` | 定义大文件拆分路线、行为保持测试和回滚路径。 |
| `EVALUATOR_BOUNDARIES.md` | 定义 pattern/hehua/yongshen/fortune/topic evaluator 边界。 |
| `FINAL_REVIEW.md` | 六维审查、active WARN、falsifier 和最终进入 closeout 判断。 |

## 本轮关键代码与契约改动

- 新增岁运触发 `triggerMatrix` 和 `fortuneTriggers` 输出。
- 新增事业、财运、婚姻、健康、学业、迁移、家庭 `topicProfiles`。
- Web 工作台展示专题 profile 与风险边界，Markdown 默认不输出高风险专题 profile。
- 报告字段契约测试锁定高级格局、合化、用神、岁运、专题 profile 和 rule-depth 字段。
- 风险话术回归禁止医疗、金融、法律、心理替代建议和保证式表达。
- 修复 `_build_topic_profiles()` mypy 类型收窄，恢复 `local-ci quick`。

## 验证证据

```bash
bash scripts/local-ci.sh --profile quick
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0003-bazi-system-100 --phase decompose
```

结果：

- `local-ci quick`：PASS，evidence `/tmp/fatecat-local-ci-20260616173830`
- focused regression：`49 passed in 9.74s`
- `mypy fate_core`：PASS，`Success: no issues found in 39 source files`
- 八字 rule-depth：PASS，`30 passed in 62.50s`
- task docs decompose：PASS，`placeholders=[]`、`errors=[]`
- MingLi full：`160 answered / 45 correct / 28.12% accuracy`

Closeout 验证命令：

```bash
python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0003-bazi-system-100 --phase closeout
git status --short
```

## Git 交付证据

本轮主要提交：

```text
732467e docs: record bazi final review
a0a8059 fix: restore topic profile mypy gate
d1ea92a docs: define bazi evaluator boundaries
d042700 test: enforce fate report risk boundaries
5dd485e test: lock bazi report field contract
9e5e011 docs: define mingli benchmark gates
cd56568 docs: classify mingli failures
5aa5332 docs: record full mingli evaluation
ed23720 feat: bound bazi topic reports
f71f06a feat: add bazi topic profile lifecycle
f30f96b feat: add bazi fortune trigger matrix
```

最终 closeout commit 由本文件和状态收口改动生成。

## 剩余 WARN

| WARN | 当前证据 | 后续处理 |
| --- | --- | --- |
| MingLi full accuracy 28.12% | `MINGLI_FULL_EVALUATION.md` | 按 `BENCHMARK_GATE_POLICY.md` 先提升到 overall >=32%，不得刷题库答案。 |
| 专题 profile 仍是 beta | `FINAL_REVIEW.md` | 增加专题 golden 和 HITL 命例后再考虑 production lifecycle。 |
| 核心文件仍大 | `CORE_FILE_BURNDOWN.md` | 按 `EVALUATOR_BOUNDARIES.md` 单 evaluator 行为保持迁移。 |
| full golden / MingLi deep gate 慢 | `GOLDEN_DEEP_GATE.md` | 保持 quick/deep 分层，不把慢测塞进日常 quick。 |
| 真实专家命例不足 | `RULE_SOURCE_GAPS.md` | 后续通过 HITL 标注和授权材料补齐，不造假样本。 |

## 不做声明

- 不声明八字预测准确率 100%。
- 不声明 MingLi-Bench 已达专业生产标准。
- 不把无 license/reference-only 资源纳入 runtime dependency。
- 不跑 GitHub Acceptance；本任务按用户要求只使用本地 CI/CD 技术工具方案。
- 不纳入公网部署、Bot token、金融交易系统或公共高并发服务验收。

## TP-10.02 Gate 判定

- `closeout 可校验`：`PASS`
- `提交边界清晰`：`PASS`
- `最终结论不越过证据`：`PASS`

本任务包完成。
