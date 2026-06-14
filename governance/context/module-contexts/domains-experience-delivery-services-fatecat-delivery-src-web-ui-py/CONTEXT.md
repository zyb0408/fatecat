---
id: CTX-DOMAINS-EXPERIENCE-DELIVERY-SERVICES-FATECAT-DELIVERY-SRC-WEB-UI-PY
type: module-context
status: current
owner: engineering
created: 2026-06-15
last_reviewed: 2026-06-15
code_path: domains/experience-delivery/services/fatecat-delivery/src/web_ui.py
---

# FateCat Web HTML 语义界面 Context

## 代码路径

`domains/experience-delivery/services/fatecat-delivery/src/web_ui.py`

## 模块职责

- 服务端直出 `GET /web` 的 HTML 页面。
- 暴露原生 HTML 表单，用 GET 参数生成命理排盘 Markdown 报告。
- 展示字段契约、当前输入、工作台 psql ASCII 表格、Markdown 输出、机器可读输入和页面元信息。
- 展示 TradeCat Labs 项目归属和真实外部链接。
- 用 `D:\.projects\pdf` 工作台同类的黄金比例三块全屏生产空间组织 `/web`：左上 TradeCat Labs 资产声明、右上服务端生成报告、底部参数输入。

## 非职责

- 不做品牌视觉、营销页、SaaS 后台、卡片式仪表盘或高保真前端。
- 不定义命理算法、capability registry、字段 profile 或报告规则。
- 不隐藏核心数据，不把 Markdown、JSON、psql ASCII 表格改造成不可复制组件。

## 禁止事项

- 除已授权的黄金三块生产空间工作台外壳 CSS 外，禁止 `<style>`、外部 CSS、行内 `style=`。
- 禁止授权例外之外的自定义颜色、背景、字体、字号、间距、圆角、阴影、卡片、响应式布局。
- 除 `web-production-*` 结构 class 和三块生产空间 section 外，禁止仅用于视觉的 `class`、`main`、`section`、`div` 包装。
- 禁止依赖 JavaScript 才能看到核心报告或核心字段。
- 禁止在未获得用户明确许可时偏离 `/home/lenovo/.codex/Design.md`。

## 单一真相源

- 设计规范：`/home/lenovo/.codex/Design.md`
- 实现文件：`domains/experience-delivery/services/fatecat-delivery/src/web_ui.py`
- 机械回归：`tests/regression/test_web_html.py::assert_web_production_layout_html`
- 架构 gate：`governance/architecture-gates/rules/GATE-0001-Web-HTML-禁止自定义前端样式.md`
- 长期标准：`governance/standards/零美化语义界面标准.md`

## 常用验证

- `bash scripts/local-ci.sh --profile quick`

## 相关治理文档

- `governance/evidence/lessons/LESSON-0001-Web-HTML-必须遵守零美化语义界面规范.md`
- `governance/agent-governance/agent-feedback/AF-0001-代理不得违背-Design.md-擅自美化-Web-页面.md`
- `governance/standards/零美化语义界面标准.md`

## Agent Rules

- 不要把本模块上下文散落到代码目录。
- 如需引用原模块 README，只在这里链接，不复制覆盖。
- 修改本模块前必须读取 `/home/lenovo/.codex/Design.md`。
- 任何 Web HTML 改动必须先证明没有黄金三块生产空间之外的 CSS、视觉 class 和装饰性容器回潮。
