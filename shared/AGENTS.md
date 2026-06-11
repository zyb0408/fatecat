# AGENTS.md - shared

## 目录用途

`shared/` 只承载真实复用后的薄 SDK 或共享库暂存，不是 `common` 垃圾桶。

## 目录结构

```text
shared/
└── AGENTS.md
```

## 职责边界

- 只有两个以上服务稳定复用且有明确 owner 的代码才能进入这里。
- 当前 FateCat 不新增 shared 代码；优先把能力保留在领域服务内。

## 依赖方向

- `domains/apps/ai -> shared`
- 禁止 `shared` 依赖具体领域服务。
