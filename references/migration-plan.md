# FateCat 导出计划

## 当前布局

- 根目录是企业系统仓库和当前 skill 导出根。
- `domains/*/services/*` 承载生产候选服务源码、契约和测试入口。
- `governance/` 承载迁移账本、baseline evidence、标准、流程和风险。
- `scripts/common.sh` 只接受已就绪的企业根 runtime；退役路径不再参与解析。
- 旧组织映射只保存在 `governance/migration/` 与 `governance/tasks/project-history/`，作为历史证据。

## 导出 bundle

- 通过 `export-runtime.sh` 复制运行所需骨架到导出目录
- 导出目标结构保持当前单-skill 布局
- 默认支持两种模式：
  - `full`：保留 lifecycle packs
  - `lite`：排除 lifecycle packs，只保留模板与运行所需骨架
- 若导出产物还要跑 strict skill 校验，导出目录 basename 必须保持为 `fatecat`
- 排除 `.git/`、`.venv/`、`node_modules/`、缓存、字节码、真实 `.db` / `.sqlite`、真实 `.env`
- 生命周期模板与治理资产默认随 bundle 一起导出

## 后续优化

- 视情况增加校验脚本，确保导出后命令仍可用
- 视情况增加更细粒度的导出清单，例如只导出某个指定 lifecycle pack

## 导出边界

必须带走：

- `README.md`
- `AGENTS.md`
- `SKILL.md`
- `references/`
- `scripts/`
- `domains/`
- `contracts/`
- `catalog/`
- `governance/`
- `infra/`
- `docs/`

必须排除：

- `.git/`
- `.history/`
- `.venv/`
- `node_modules/`
- `.pytest_cache/`
- `.ruff_cache/`
- `.mypy_cache/`
- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `*.db`
- `*.sqlite`
- `*.sqlite3`
- `docs/reference-materials/lifecycle/packs/` 在 `lite` 模式下也必须排除

## 风险

- 包体积仍然很大，因为 `tools/reference-repos/` 保存完整第三方快照。
- 若把大量生命周期历史包沉淀在 `docs/reference-materials/lifecycle/packs/`，`full` bundle 体积会继续增长。
- 若未来路径发现逻辑变化，`scripts/common.sh`、服务路径常量、导出脚本和 hygiene 门禁需要一起更新。
