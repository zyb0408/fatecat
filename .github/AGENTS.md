# AGENTS.md - GitHub automation

## 目录用途

`.github/` 存放远端自动化配置，使 GitHub 能复现本地交付门禁。

## 目录结构

```text
.github/
├── AGENTS.md
└── workflows/
    ├── acceptance.yml
    └── container.yml
```

## 职责边界

- `workflows/acceptance.yml`：在 push / pull_request 时执行 FateCat skill 验收链。
- `workflows/container.yml`：构建 FateCat delivery 容器、运行容器 smoke，并在 push 到 main 或 tag 时推送 GHCR。
- 这里不放业务代码、不保存 secret、不生成运行态产物。

## 依赖方向

- `.github/workflows/* -> scripts/acceptance.sh -> scripts/common.sh runtime root resolution`
- `.github/workflows/container.yml -> scripts/container-build.sh + scripts/container-smoke.sh`
- CI 只调用仓库脚本；代码质量门禁以 `scripts/acceptance.sh` 为单一入口，容器发布门禁以 `scripts/container-smoke.sh` 为单一入口。
