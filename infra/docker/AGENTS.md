# AGENTS.md - infra/docker

## 目录用途

`infra/docker/` 承载 FateCat 容器镜像的期望状态：镜像构建、容器入口、运行用户和健康检查都在这里定义。

## 目录结构

```text
infra/docker/
├── AGENTS.md
├── Dockerfile.delivery
└── entrypoint.delivery.sh
```

## 职责边界

- `Dockerfile.delivery`：构建 FateCat FastAPI / Web 交付层镜像，保留企业源码树资产作为当前运行真相源。
- `entrypoint.delivery.sh`：容器启动入口，只负责读取环境变量并启动 ASGI 服务。
- 这里不保存 secret、运行时数据库、镜像 tarball 或 registry 凭证。

## 依赖方向

- `infra/docker -> domains + contracts + tools/reference-repos + infra/environments`
- 容器运行态写入 `/app/infra/runtime/local-state`，不得写回配置模板或源码目录。
