---
id: STD-PYTHON-PROJECT-STRUCTURE
type: standard
status: active
owner: engineering
created: 2026-06-06
last_reviewed: 2026-06-06
review_cycle: P90D
---

# Python 项目结构规范

## 目标

FateCat 的 Python 工程入口已经提升到仓库根 `pyproject.toml`；后续必须让依赖、运行、测试、发布和容器边界都从企业根可复现。

## 开发

1. `.venv` 隔离依赖。
   - 创建：`python -m venv .venv`
   - 启用：macOS/Linux `source .venv/bin/activate`；Windows `.\\.venv\\Scripts\\activate`
   - 本仓库入口：`make venv`

2. Python 版本管理。
   - `.python-version` 固定主版本，当前为 `3.12`。
   - 推荐用 `pyenv` 或 `asdf` 避免本地、CI、线上 Python 版本漂移。

3. 交互式实验。
   - `ipython`、`python -i` 或 Jupyter 可用于验证接口、调参和快速试错。
   - 实验结果不得替代 pytest、golden regression 或 acceptance 证据。

## 依赖

4. `requirements.txt` 与 `pyproject.toml`。
   - `requirements.txt` 是 pip 传统复现入口。
   - root `pyproject.toml` 是企业仓库 Python 工程入口，承载依赖、构建、entry point 和工具配置。

5. 安装与导出依赖。
   - 复现环境：`python -m pip install -r requirements.txt` 或 `make install-locked`。
   - 导出当前环境：`python -m pip freeze > requirements.lock.txt` 或 `make freeze`。

6. 锁定依赖。
   - `requirements.lock.txt` 锁定当前兼容期依赖版本，防止环境漂移。
   - 若后续采用 Poetry、uv 或 Pipenv，必须用对应 lockfile，并同步更新本标准。

7. 依赖坏了的修复。
   - 最可靠路径：`make rebuild-venv`。
   - 必要时：`make clean-cache` 清理 pip cache、`__pycache__`、`.pytest_cache`、`build/`、`dist/`、`*.egg-info`。

## 运行

8. `python -m ...`。
   - 优先使用 `python -m pip`、`python -m pytest`、`python -m ruff`、`python -m mypy`，避免多 Python 环境下调用错可执行文件。

9. `.env` 与配置。
   - 本地 secret 只允许在 ignored `.env` 或外部 secret 注入中出现。
   - 本地模板位于 `infra/environments/local/.env.example` 与 `infra/environments/local/agent.env.example`。

10. 日志与调试。
    - 生产候选代码优先使用 `logging` 和结构化错误，不把散乱 `print` 当长期观测能力。
    - 本地调试可用 `breakpoint()`，不得提交无意调试断点。

11. 运行态边界。
    - 日志、缓存、数据库和输出目录必须被 `.gitignore`、`.dockerignore`、source/export hygiene 同时覆盖。
    - 不提交真实 `.env`、数据库实库、缓存、日志、node_modules、raw 私有资料、个人路径或 secret。

## 质量

12. 格式化与静态检查。
    - 默认使用 `ruff check` 与 `ruff format`，入口为 `make lint` 和 `make format`。
    - `black` 作为可用成熟格式化器保留在 dev 依赖与 `make format-black`，但当前不与 `ruff format` 同时作为默认门禁，避免双格式器争夺同一文件。
    - 类型检查使用 `mypy`，入口为 `make typecheck`。

13. 测试。
    - 仓库根测试入口使用 `pytest`，收集 canonical service tests 与 `tests/regression` 行为回归。
    - 历史测试已迁入 `tests/regression`；active acceptance 不依赖退役路径。
    - 常用命令：`pytest -q`、`pytest -k name`、`pytest --maxfail=1`。

14. 项目结构与导入。
    - 使用包结构和 `__init__.py`。
    - 优先使用相对/绝对导入；少靠 `sys.path`。跨服务导入必须指向 canonical service root。
    - 服务目录必须有最小 service contract test。

## 发布

15. `__main__.py` 与 console script entry points。
    - 包运行入口为 `fatecat = fate_core.cli:main`。
    - 保留 `python -m fate_core` 这类模块入口能力。

16. 打包与发布。
    - 构建系统使用 `hatchling`。
    - sdist/wheel 入口：`make sdist`、`make wheel`、`make build`。

17. 容器与导出。
    - 容器里不要在 root 环境裸装依赖；必须使用 venv 或明确镜像策略。
    - 固定 Python 版本与依赖。
    - 发布前必须通过 structure、source hygiene、privacy fixtures、governance strict validate、preflight、acceptance、export hygiene 和 `git diff --check`。
