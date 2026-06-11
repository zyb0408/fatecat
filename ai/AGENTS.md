# AGENTS.md - ai

## 目录用途

`ai/` 承载 AI 产品、Agent、Prompt、RAG、模型网关和评估资产。FateCat 的主旨是把稳定排盘结果整理成 AI 可消费结构，而不是让 AI 直接口算排盘。

## 目录结构

```text
ai/
└── AGENTS.md
```

## 职责边界

- Agent/skill 入口、Prompt 资产、AI 评估和模型供应商接入后续归入这里。
- 命理算法、能力协议和字段 profile 不放在 `ai/`。
- 任何 AI 相关资产必须同步进入 `governance/ai-governance/` 的监管分类与影响评估。

## 依赖方向

- `ai -> contracts/* + domains/* + governance/ai-governance`
- 禁止 AI 入口绕过 `contracts/` 自行解释底层排盘字段。
