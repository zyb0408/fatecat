# AGENTS.md - fate_core support

## 目录用途

`fate_core/support/` 提供无业务副作用的支撑工具，供 adapters、kernel、providers 和 usecases 共享。

## 目录结构

```text
support/
├── AGENTS.md
├── __init__.py
├── branding.py
├── paths.py
└── timezone.py
```

## 职责边界

- `paths.py`：从企业仓库根解析 contracts、infra、data、vendor、delivery 迁移窗口路径和真太阳时脚本路径。
- `timezone.py`：北京时间规范化、当前时间和格式化工具；不读取配置，不做 IO。
- `branding.py`：TradeCat Labs / FateCat 品牌和免责声明装配。
- `__init__.py`：导出稳定支撑符号，避免上层散落相对路径和重复时区工具。

## 依赖方向

- 允许依赖标准库和稳定静态配置路径。
- 禁止依赖 delivery 运行模块、FastAPI、Telegram Bot、报告模板或命理计算实现。
