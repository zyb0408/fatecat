# AGENTS.md - scripts

## 目录用途

`scripts/` 是本地可重复执行入口。GitHub Actions 只触发这些入口，不复制另一套流水线逻辑。

## 目录结构

```text
scripts/
├── AGENTS.md
├── acceptance.sh
├── check-public-release-policy.sh
├── container-build.sh
├── container-release.sh
├── container-smoke.sh
├── hf-space-deploy.sh
├── local-ci.sh
├── preflight.sh
├── public-release-gate.sh
├── export-runtime.sh
├── generate-mingli-predictions.sh
├── run-mingli-bench.sh
└── ...
```

## 职责边界

- 根脚本负责 bootstrap、preflight、acceptance、delivery smoke、容器 smoke、导出卫生和生产就绪检查。
- `container-build.sh`：构建 FateCat delivery 镜像。
- `container-smoke.sh`：启动临时容器并验证 `/health` 与真实排盘 API。
- `container-release.sh`：构建、smoke，并在显式 `--push` 时推送 registry。
- `check-public-release-policy.sh`：检查公开 Web 工作台发布策略，防止 GitHub 自动验收回潮、HF 免费 Space 误开记录存储或文档口径缺失。
- `hf-space-deploy.sh`：生成 Hugging Face Docker Space 分发包，并通过 `hf` CLI 上传到指定 Space；默认目标 `tradecatlabs/fatecat`，默认拒绝非 `tradecatlabs` 认证。
- `local-ci.sh`：本地 CI/CD 调度入口；只编排本仓脚本，不调用 GitHub Actions。
- `public-release-gate.sh`：公开 Web 工作台发布前本地门禁；串联 quick CI、发布策略、delivery smoke 和生产静态准入，可选验证线上 HF URL。
- `common.sh` 负责解析 runtime root；只允许已就绪的企业根作为运行根。
- `generate-mingli-predictions.sh` 是 `fate_core.evaluation.mingli_baseline` 的薄封装，不承载领域评测规则。
- `run-mingli-bench.sh` 负责离线 FortuneTellingBench 统计、提示词生成和预测结果评估，不调用外部模型 API。
- 脚本不得保活退役路径；任何旧路径只能出现在防回潮门禁、历史证据或迁移账本中。

## Principle Gate Evidence

- target end state: scripts are thin local CI/CD and runtime entrypoints around canonical roots.
- real constraints: container smoke uses short-lived containers and local ports for self-host checks.
- inertia constraints: historical script names and smoke helpers must not become alternate platforms.
- kill list: hidden old root fallback, secret persistence, and live-production claims without inputs.
- proof point: `local-ci.sh --profile all` passes through shell, pytest, export, Docker, and readiness.
- falsifier: any script writes secrets, hides runtime state, or claims live API/Bot without real inputs.
- migration slice: keep root scripts as stable wrappers while domains/contracts own implementation logic.

## 依赖方向

- `scripts -> domains + contracts + infra + governance`
- `scripts/generate-mingli-predictions.sh -> fate_core.evaluation.mingli_baseline`
- `scripts/hf-space-deploy.sh -> infra/huggingface-space + hf CLI`
- 禁止脚本直接隐藏 secret、运行态或旧路径 fallback。
