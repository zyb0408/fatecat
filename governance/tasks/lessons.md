# 执行教训

## 2026-04-14

- 大体量 `git push` 必须默认放到后台持久会话执行，前台继续推进校验、文档或其他实现，不允许阻塞在上传进度上。

## 2026-06-15

- FateCat Web HTML 必须严格遵守 `/home/lenovo/.codex/Design.md` 的零美化语义界面规范。代理不得擅自加入授权例外之外的 CSS、视觉 class、颜色、圆角、卡片、响应式布局或装饰性容器；当前唯一授权例外是 `/web` 复刻 `D:\.projects\pdf` 工作台黄金三块全屏生产空间：左上 TradeCat Labs 资产声明、右上服务端生成报告、底部参数输入。任何 `/web` 变更必须用 `tests/regression/test_web_html.py::assert_web_production_layout_html` 和 `bash scripts/local-ci.sh --profile quick` 证明禁用项没有回潮。
