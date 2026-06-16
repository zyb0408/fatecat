# Task Overview

- Task ID: `0005`
- Slug: `bazi-capability-100-roadmap`
- Objective: 调研并设计把八字功能十个完善度维度从当前基线推进到 100% 的任务树、验收门禁和执行波次计划。
- Status: `Planned`

## In Scope

- 从 `0004` 的真实 scorecard 出发，定义十个维度到 100% 的工程验收口径。
- 调研可复用开源资源、benchmark、oracle 和数据集的边界。
- 设计可执行任务树、依赖顺序、完成标准、验收命令和阻塞条件。
- 输出下一轮执行可以直接消费的 `TP-XX(.YY...)` 计划。

## Out of Scope

- 本任务不直接实现业务代码。
- 本任务不宣称预测准确率 100%。
- 本任务不把 MingLi/BaziQA 数据接入生产 runtime。
- 本任务不运行 GitHub Acceptance，不推送远端。
- 本任务不绕过 license、专家样本和高风险输出边界。

## Task Package Tree

```text
TP-01 100% 口径与资源准入
  TP-01.01 当前基线复核
  TP-01.02 外部资源准入复核
  TP-01.03 十维 100% gate 合同
TP-02 基础排盘与历法时间 100%
  TP-02.01 CalendarProvider 升级合同
  TP-02.02 边界样本扩展
  TP-02.03 oracle mismatch report
TP-03 证据化与可解释 100%
  TP-03.01 ruleId 覆盖强制门禁
  TP-03.02 evidence/counterEvidence schema
  TP-03.03 高风险输出 policy gate
TP-04 常规八字分析 100%
  TP-04.01 strength evaluator 拆分
  TP-04.02 ten-god evaluator 拆分
  TP-04.03 regular-pattern/relation evaluator 拆分
TP-05 高级格局 100%
  TP-05.01 高级格局 taxonomy
  TP-05.02 正反边界 golden
  TP-05.03 guarded evaluator
TP-06 合化成败 100%
  TP-06.01 条件链状态模型
  TP-06.02 transform evaluator
  TP-06.03 破化/争合/阻隔反例矩阵
TP-07 用神裁决 100%
  TP-07.01 用神策略合同
  TP-07.02 冲突排序 evaluator
  TP-07.03 用神反例与报告边界
TP-08 岁运专题 100%
  TP-08.01 岁运触发矩阵
  TP-08.02 P0 专题 profile evaluator
  TP-08.03 高风险专题 policy regression
TP-09 Golden / 回归 100%
  TP-09.01 corpus 扩展目标
  TP-09.02 shard release gate
  TP-09.03 mutation/schema regression
TP-10 样本外 benchmark 100%
  TP-10.01 MingLi no-leak full gate
  TP-10.02 failure-driven rule backlog
  TP-10.03 BaziQA admission gate
TP-11 维护边界与交付 100%
  TP-11.01 evaluator 物理拆分收口
  TP-11.02 Web/API/Markdown 消费边界
  TP-11.03 local release gate
```

## Requirement Alignment

| 用户维度 | 对应任务 |
| --- | --- |
| 基础排盘 93% -> 100% | `TP-02` |
| 历法 / 时间边界 90% -> 100% | `TP-02` |
| 证据化 / 可解释 88% -> 100% | `TP-03` |
| 常规八字分析 84% -> 100% | `TP-04` |
| 高级格局 72% -> 100% | `TP-05` |
| 合化成败 76% -> 100% | `TP-06` |
| 用神裁决 78% -> 100% | `TP-07` |
| 岁运专题 70% -> 100% | `TP-08` |
| Golden / 回归 86% -> 100% | `TP-09` |
| 样本外 benchmark 45% -> 100% | `TP-10` |

## Task Package Overview

| Phase | 目标 | 完成标准 |
| --- | --- | --- |
| 研究与口径 | 把 100% 从口号变成 gate | `RESEARCH.md`、`ACCEPTANCE.md` 无占位符，明确不等于预测 100%。 |
| 核心能力补齐 | 排盘、规则、解释、高级断法、用神、岁运专题 | 每个能力面都有 schema、sourceRuleId、golden、policy 和回归命令。 |
| 评测与回归 | deep shard、MingLi、BaziQA、failure taxonomy | no-leak、全量可复现、失败可回炉。 |
| 交付收口 | evaluator 拆分、Web/API/Markdown 边界、本地 release | local quick/full/deep 证据齐全，Active BLOCK=0。 |

## Reading Order

1. `RESEARCH.md`
2. `README.md`
3. `CONTEXT.md`
4. `PLAN.md`
5. `ACCEPTANCE.md`
6. `ACCEPTANCE_CHECKLIST.md`
7. `TODO.md`
8. `STATUS.md`
