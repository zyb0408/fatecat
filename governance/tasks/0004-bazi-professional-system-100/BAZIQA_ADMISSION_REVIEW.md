# TP-09.03 BaziQA 纳入评测审查

## 结论

- 状态：PASS，结论为 `future_candidate/evaluation_only`。
- 不允许进入 runtime。
- 不允许作为 production rule source。
- 在许可证与数据一致性问题澄清前，不纳入正式 release gate。

## 来源证据

- 仓库：`https://github.com/ChenJiangxi/BaziQA`
- 本轮审查提交：`8ea8222f8bd8ef8a6f1a5fb012344935a66e7686`
- 提交时间：`2026-03-08 23:07:31 +0800`
- README 提到论文：`https://arxiv.org/abs/2602.12889`

本轮只浅克隆到 `/tmp/fatecat-baziqa-review` 做审查，没有把数据 vendored 到仓库。

## 文件结构

```text
README.md
benchmark_report.md
dataset_and_input_format.md
data/celebrity50_zh.json
data/contest8_2021.json
data/contest8_2022.json
data/contest8_2023.json
data/contest8_2024.json
data/contest8_2025.json
```

未发现：

- `LICENSE`
- `COPYING`
- `NOTICE`

README 有 MIT badge，但缺少许可证正文文件；按生产治理口径，许可证证据不完整。

## 数据 schema

Contest8 顶层为 JSON array：

- 第 1 项：contest metadata。
- 后续项：命主对象。

命主对象核心字段：

- `person_id`
- `name`
- `profile.birth.year/month/day/hour/minute/place/raw`
- `profile.gender`
- `categories`
- `questions[].question_id`
- `questions[].question`
- `questions[].options`
- `questions[].answer`

Celebrity50 命主对象还有：

- `source_file`
- 更长的 `categories` 事件时间线
- 4 或 5 个选项的问题

## 实测数据一致性

```text
contest8_2021.json: 9 个带题命主，40 题，4 选项，有 answer
contest8_2022.json: 8 个带题命主，40 题，4 选项，有 answer
contest8_2023.json: 8 个带题命主，40 题，4 选项，有 answer
contest8_2024.json: 8 个带题命主，40 题，4 选项，有 answer
contest8_2025.json: 8 个带题命主，40 题，4 选项，有 answer
celebrity50_zh.json: 50 个命主，488 题，4/5 选项，有 answer
```

风险：

- README 声称 Celebrity50 为 250 题，但实测为 488 题。
- README 声称 Contest8 每年 8 位命主；2021 文件实测为 9 个带题命主，其中后两位为 3 题和 2 题。
- 数据包含真实人物与具体事件，不能默认进入 runtime 或公开报告链路。

## Adapter Plan

仅允许未来作为离线评测候选：

1. 外部数据路径通过 `FATECAT_BAZIQA_DATA_DIR` 指定，不 vendor 入仓库。
2. adapter 只读取 `profile.birth/gender/question/options` 生成 prompt 或 evaluation rows。
3. predictions 输出禁止包含 `answer/expected/correct/gold/label`。
4. evaluator 单独读取 gold answer 计算 accuracy。
5. 记录 source repo、commit hash、file hash、schema version。
6. `celebrity50_zh.json` 默认只进入人工审查或隔离评测，不进入公共报告、runtime 或训练数据。
7. license 未澄清前，gate 状态固定为 `candidate_only`。

## 禁止路径

- 禁止把 BaziQA answer 反写为 FateCat 规则。
- 禁止按 `question_id` 做定向规则。
- 禁止把 Celebrity50 真实人物事件用于产品输出。
- 禁止把 README 的 MIT badge 当成完整 license 证据。
- 禁止把 BaziQA 接进 `calculate_pure_analysis`、Web、Bot、API runtime。
