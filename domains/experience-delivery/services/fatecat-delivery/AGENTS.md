# AGENTS.md - fatecat-delivery

## 目录用途

`fatecat-delivery` 是 FateCat 的交付服务。本服务根是源码真相源，运行资产从 `contracts/`、`infra/`、`tools/` 和上游 `fate-core` 读取。

## 目录结构

```text
fatecat-delivery/
├── AGENTS.md
├── README.md
├── service.yaml
├── start.py
├── scripts/
├── src/
└── tests/
```

## 职责边界

- 负责 FastAPI、Web HTML、Telegram Bot、标准 Markdown 报告和 legacy 交付适配。
- 不定义 capability registry、字段 profile 或底层命理算法。
- 不读取真实 secret 入仓；delivery smoke 可临时生成本地 `.env` 并清理。
- `src/web_ui.py` 只负责零美化语义 HTML：服务端直出、原生表单、真实链接、psql ASCII 表格、Markdown 原文和机器可读片段。
- Web HTML 禁止 CSS、视觉 class、颜色、圆角、卡片、响应式布局和装饰性容器；修改前必须读取 `/home/lenovo/.codex/Design.md` 与 `GATE-0001`。

## 依赖方向

- 当前状态：`domains/experience-delivery/services/fatecat-delivery -> domains/fate-analysis/services/fate-core + contracts/fate + infra + tools/reference-repos`
- 运行态输出只允许进入本服务 `output/` 或 `infra/runtime/local-state/`，不得写回 vendor 快照。
- `/web` 页面设计真相源：`/home/lenovo/.codex/Design.md`、`governance/standards/零美化语义界面标准.md`、`governance/context/module-contexts/domains-experience-delivery-services-fatecat-delivery-src-web-ui-py/CONTEXT.md`。
