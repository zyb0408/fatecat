---
id: MIG-FATECAT-DIRECTORY-MAPPING
type: migration-mapping
status: active
owner: engineering
created: 2026-06-06
last_reviewed: 2026-06-06
review_cycle: P30D
---

# FateCat 企业目录映射

## 映射原则

- 目录名可以调整，职责边界不能混。
- 旧路径只允许作为迁移账本、历史证据、负例测试和临时兼容盒存在。
- 复用先于自写：成熟开源命理、历法和排盘仓库继续作为供应链资产登记，不在 vendor 内魔改。

## 顶层目标

```text
fatecat/
├── apps/
├── ai/
├── domains/
├── platform/
├── infra/
├── contracts/
├── catalog/
├── governance/
├── shared/
├── tools/
├── docs/
├── scripts/
└── tests/
```

## 旧路径到新路径

| 旧路径 | 目标路径 | 处理方式 | 当前状态 |
| --- | --- | --- | --- |
| `scripts/project/modules/fate_core/` | `domains/fate-analysis/services/fate-core/src/` | 领域服务迁移 | 源码已复制到 canonical service root；旧路径为兼容源和行为基线 |
| `scripts/project/modules/telegram/` | `domains/experience-delivery/services/fatecat-delivery/src/` | 交付服务迁移 | 源码、脚本和测试入口已复制到 canonical service root；旧路径为兼容源和行为基线 |
| `scripts/project/assets/fate/` | `contracts/fate/` | capability/profile/evidence/risk 契约迁移 | 已复制到 canonical contract root；旧路径为兼容源 |
| `scripts/project/assets/data/` | `domains/fate-analysis/data-products/` 与 `contracts/datasets/` | 静态数据与 golden 数据分层迁移 | 已复制轻量数据产品；`classics/raw` 与 `calendar/solar_terms/raw` 未进入 canonical root |
| `scripts/project/assets/database/` | `infra/databases/` | schema 和 migration 迁移 | 已复制 schema；真实 `.db` 不迁移、不提交 |
| `scripts/project/assets/config/` | `infra/environments/` | env template 与 branding 配置迁移 | 已复制 `.env.example`、`agent.env.example`、`branding.json`；真实 `.env` 禁止提交 |
| `scripts/project/assets/deploy/` | `infra/runtime/` 或 `tools/bootstrap/` | 运行与自举脚本归位 | 待迁移 |
| `scripts/project/assets/docs/` | `docs/` 与 `governance/evidence/` | 人类文档和治理证据分流 | 待迁移 |
| `scripts/project/assets/tasks/` | `governance/tasks/` | 任务包迁移 | 待迁移 |
| `scripts/project/assets/vendor/` | `tools/reference-repos/` 或 `platform/supply-chain/vendor-snapshots/` | vendor 快照登记迁移，禁止改源码 | 已复制到 `tools/reference-repos/`；`node_modules` 不进入 canonical vendor |
| `scripts/project/runtime/` | `infra/runtime/local-state/` 或 ignored runtime root | 运行态骨架迁移 | 已建立本地运行态骨架；真实 `bazi.db` 留在旧 runtime/忽略运行态，不迁移 |
| `scripts/project/tests/` | `tests/` 或服务内 tests | 仓库级与服务级测试分流 | 已复制到 `tests/regression/`；service tests 位于 `domains/*/services/*/tests/` |
| `scripts/project/pyproject.toml` | `pyproject.toml` | Python 项目配置提升到企业仓库根 | root `pyproject.toml` 已成为 active Python 工程入口 |
| `scripts/project/README.md` | `docs/README.md` 或根 README 分段 | 产品说明迁移 | 待迁移 |
| `SKILL.md` | `ai/skills/fatecat/SKILL.md` 或保留根导出入口 | Agent 入口归位 | 待设计 |
| `references/` | `docs/references/` 或 `governance/context/` | skill 参考文档分流 | 待迁移 |
| `.github/workflows/acceptance.yml` | `.github/workflows/acceptance.yml` | 保留位置，改为复用新本地入口 | 待更新 |
| `scripts/*.sh` | `scripts/*.sh` | 保留本地执行入口，改为 enterprise runtime root | `resolve_runtime_root` 默认返回企业根；legacy root 只作为显式兼容 fallback |

## 当前 canonical 资产根

| 资产类型 | canonical root | 禁止进入 |
| --- | --- | --- |
| 命理契约 | `contracts/fate/` | 算法代码、运行输出、数据库 |
| 静态数据产品 | `domains/fate-analysis/data-products/` | raw 私有资料、大文件、未复核外部分发包 |
| 配置模板 | `infra/environments/local/` | 真实 `.env`、secret、token |
| 数据库 schema | `infra/databases/` | `*.db`、`*.sqlite`、备份 |
| 本地运行态 | `infra/runtime/local-state/` | 除 `.gitkeep` 外的运行数据 |
| 供应链参考仓 | `tools/reference-repos/` | `node_modules`、未登记 vendor、魔改 vendor 源码 |

## 临时兼容盒

| 兼容盒 | owner | 到期条件 | 删除条件 |
| --- | --- | --- | --- |
| `scripts/project/` | engineering | P0 脚本、CI、pyproject、路径常量已支持 enterprise roots | `rg -n 'scripts/project'` 只剩 compatibility 字段、migration ledger、historical evidence、negative tests 或 guard pattern |

## 禁止项

- 不在根目录创建第二套业务源码并同时保留 active `scripts/project` 多头写入。
- 不让 active code/config 继续优先读取旧路径。
- 不用 ignore/exclude 掩盖旧路径回潮。
- 不把 vendor 缺许可证问题通过复制改名隐藏。
