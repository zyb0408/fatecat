# FateCat 八字体系当前能力基线证据

更新时间：2026-06-16

## 结论

当前基线可以继续使用 `综合约 76%` 作为任务推进起点，但它只是工程估算，不是专业命中率。

- 基础排盘、历法边界、证据层、golden 回归和本地 quick CI 已具备可重复验证入口。
- 专业规则还卡在高级格局、合化成败、用神冲突裁决、岁运专题和样本外准确率。
- MingLi sample 10 的 FateCat scored baseline 为 `30.00%`，只能证明评测链路真实接通，不能证明专业推理强。

## 已执行命令

```bash
python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null
python3 -m json.tool contracts/fate/classics_rule_index.json >/dev/null
bash scripts/run-mingli-bench.sh --stats
bash scripts/generate-mingli-predictions.sh --year 2025 --sample 10 --output-jsonl /tmp/fatecat-mingli-baseline.jsonl
bash scripts/run-mingli-bench.sh --year 2025 --sample 10 --predictions-file /tmp/fatecat-mingli-baseline.jsonl --output-json /tmp/fatecat-mingli-baseline.json
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-bazi-baseline
```

## 规则资产基线

| 资产 | 总数 | 八字相关 | 说明 |
| --- | ---: | ---: | --- |
| `contracts/fate/rule_depth_registry.json` | 44 | 22 | 八字和紫微规则深度 registry；只保存规则条件、证据字段、权重、冲突策略和风险边界。 |
| `contracts/fate/classics_rule_index.json` | 98 | 43 | 典籍规则短索引；只登记摘要和来源，不复制大段原文。 |

## Golden 基线

| 文件 | 当前数量 | 用途 |
| --- | ---: | --- |
| `domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json` | 300 | 八字 coverage matrix；deep gate 需分片，不进入日常 quick 全量。 |
| `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json` | 8 | 八字 rule-depth 回归样本。 |
| `domains/fate-analysis/data-products/bazi/golden/statement_cases.json` | 5 | 八字断语输出契约回归。 |
| `domains/fate-analysis/data-products/bazi/golden/calendar_boundary_cases.json` | 4 | 节气、立春、子时、真太阳时等边界样本起点。 |

## MingLi-Bench 基线

### 数据集统计

| 项 | 值 |
| --- | --- |
| 数据集 | `FortuneTellingBench` |
| 本地路径 | `tools/reference-repos/github/MingLi-Bench-main/data/data.json` |
| 年份 | 2022, 2023, 2024, 2025 |
| 总题量 | 160 |

### 全量分类分布

| 分类 | 题量 |
| --- | ---: |
| 婚姻 | 44 |
| 事业 | 25 |
| 家庭 | 22 |
| 健康 | 17 |
| 性格 | 14 |
| 财运 | 13 |
| 学业 | 11 |
| 子女 | 6 |
| 外貌 | 3 |
| 运势 | 2 |
| 灾劫 | 2 |
| 官非 | 1 |

### 2025 sample 10 评分

| 指标 | 值 |
| --- | ---: |
| total | 10 |
| answered | 10 |
| missing | 0 |
| correct | 3 |
| accuracy | 30.00% |
| predictions file | `/tmp/fatecat-mingli-baseline.jsonl` |
| report file | `/tmp/fatecat-mingli-baseline.json` |

### sample 10 分类结果

| 分类 | total | answered | correct | accuracy |
| --- | ---: | ---: | ---: | ---: |
| 事业 | 1 | 1 | 0 | 0.00% |
| 健康 | 1 | 1 | 0 | 0.00% |
| 婚姻 | 4 | 4 | 2 | 50.00% |
| 家庭 | 2 | 2 | 1 | 50.00% |
| 性格 | 1 | 1 | 0 | 0.00% |
| 财运 | 1 | 1 | 0 | 0.00% |

### sample 10 错误样本

| question_id | 分类 | expected | predicted | 初步归因 |
| --- | --- | --- | --- | --- |
| `ftb_0123` | 事业 | B | C | 事业专题规则弱，当前 scored baseline 主要靠关键词和 tie-breaker。 |
| `ftb_0125` | 婚姻 | B | C | 婚姻专题缺配偶星、刑冲合害与岁运触发的联合裁决。 |
| `ftb_0126` | 健康 | D | A | 健康属于高风险专题，当前仅能做结构压力证据，不能强断。 |
| `ftb_0127` | 性格 | B | C | 性格专题缺十神/五行/格局到选项的稳定映射。 |
| `ftb_0128` | 财运 | D | A | 财运专题缺财星、岁运触发和风险边界联合评分。 |
| `ftb_0129` | 婚姻 | D | C | 婚姻专题仍缺高级关系规则和反例。 |
| `ftb_0130` | 家庭 | B | C | 家庭专题映射不足，需拆父母/家庭结构证据。 |

## 本地 CI 基线

`bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-bazi-baseline` 通过。

| 门禁 | 结果 |
| --- | --- |
| shell syntax | PASS |
| pure preflight smoke | PASS |
| structure gate | PASS |
| source hygiene | PASS |
| privacy fixtures | PASS |
| ruff check | PASS |
| ruff format check | PASS，`131 files already formatted` |
| mypy fate_core | PASS，`Success: no issues found in 39 source files` |
| focused regression tests | PASS，`47 passed in 7.96s` |
| git whitespace check | PASS |

## 后续优先级

| 优先级 | 依据 | 对应节点 |
| --- | --- | --- |
| P0 | sample 10 里事业、健康、性格、财运均为 0/1，说明专题 profile 还弱。 | `TP-06.01`、`TP-06.02`、`TP-07.02` |
| P0 | 婚姻题量最大，sample 10 也有错题，优先补配偶星、合冲刑害、岁运联动。 | `TP-03`、`TP-04`、`TP-06` |
| P0 | 规则和 classics 已有种子，但需要映射到高级格局、合化、用神和岁运。 | `TP-01.02` |
| P1 | 300+ golden 不适合 quick 全量，需要 shard 和耗时预算。 | `TP-02.03` |

## TP-00.03 Gate 判定

- baseline report 已记录 `total/answered/correct/accuracy/byCategory/results`。
- sample 10 明确只作当前链路基线，不作为最终能力。
- 当前 76% 估算有本地规则数、golden 数、MingLi 结果和 local-ci quick 证据支撑。

