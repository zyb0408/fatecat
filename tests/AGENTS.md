# AGENTS.md - tests

## 目录用途

`tests/` 是企业仓库级测试入口，承载跨服务、契约、结构门禁和行为回归。旧兼容测试已复制到 `tests/regression/`。

## 目录结构

```text
tests/
├── AGENTS.md
└── regression/
    ├── conftest.py
    ├── fate_core/
    └── test_*.py
```

## 职责边界

- `regression/`：原项目行为回归测试，路径已切到 canonical roots。
- 服务私有测试可以留在服务根，但必须被根 `scripts/acceptance.sh` 覆盖。
- 不在这里写入运行态、golden 原始资料或外部 vendor 源码。

## 依赖方向

- `tests -> domains + contracts + catalog + governance`
