# 执行教训

## 2026-04-14

- 大体量 `git push` 必须默认放到后台持久会话执行，前台继续推进校验、文档或其他实现，不允许阻塞在上传进度上。

## 2026-06-15

- FateCat Web HTML 必须严格遵守 `/home/lenovo/.codex/Design.md` 的零美化语义界面规范。代理不得擅自加入 CSS、视觉 class、颜色、圆角、卡片、响应式布局或装饰性容器；任何 `/web` 变更必须用 `tests/regression/test_web_html.py::assert_zero_beauty_html` 和 `bash scripts/local-ci.sh --profile quick` 证明禁用项没有回潮。
