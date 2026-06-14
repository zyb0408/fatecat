# AGENTS.md - scripts

## 目录用途

`scripts/` 是本地可重复执行入口。GitHub Actions 只触发这些入口，不复制另一套流水线逻辑。

## 目录结构

```text
scripts/
├── AGENTS.md
├── acceptance.sh
├── container-build.sh
├── container-release.sh
├── container-smoke.sh
├── preflight.sh
├── export-runtime.sh
├── run-mingli-bench.sh
└── ...
```

## 职责边界

- 根脚本负责 bootstrap、preflight、acceptance、delivery smoke、容器 smoke、导出卫生和生产就绪检查。
- `container-build.sh`：构建 FateCat delivery 镜像。
- `container-smoke.sh`：启动临时容器并验证 `/health` 与真实排盘 API。
- `container-release.sh`：构建、smoke，并在显式 `--push` 时推送 registry。
- `common.sh` 负责解析 runtime root；只允许已就绪的企业根作为运行根。
- `run-mingli-bench.sh` 负责离线 FortuneTellingBench 统计、提示词生成和预测结果评估，不调用外部模型 API。
- 脚本不得保活退役路径；任何旧路径只能出现在防回潮门禁、历史证据或迁移账本中。

## 依赖方向

- `scripts -> domains + contracts + infra + governance`
- 禁止脚本直接隐藏 secret、运行态或旧路径 fallback。
