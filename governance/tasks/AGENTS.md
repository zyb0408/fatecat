# AGENTS.md - Governance Tasks

## 目录用途

`governance/tasks/` 是任务治理与历史交接根，保存任务包、执行证据、closeout 和候选 lessons。它只服务工程治理，不参与运行时加载。

## 目录结构

```text
tasks/
├── AGENTS.md
├── README.md
├── lessons.md
└── project-history/
    ├── INDEX.md
    ├── lessons.md
    ├── legacy-project-scripts/
    ├── 0001-comprehensive-bazi-statement-service-hardening/
    └── 0002-bazi-ziwei-benchmark-hardening/
```

## 职责边界

- `README.md`：说明任务治理目录的维护规则。
- `lessons.md`：当前任务级候选教训池；长期规则需要晋升到治理包对应目录。
- `project-history/`：旧任务包归档区，保留历史计划、验收、证据和 closeout。
- `project-history/legacy-project-scripts/`：旧布局工具与部署脚本归档，只作为迁移证据，不作为 active 执行入口。
- 禁止在这里放运行时配置、业务源码、依赖缓存或测试输出。

## 依赖方向

- `project-history/* -> governance/evidence/*`：历史证据可被治理证据引用。
- `lessons.md -> governance/evidence/lessons/* + governance/standards/* + governance/processes/*`：候选教训拆分后晋升。
- 运行时代码不得依赖 `governance/tasks/`。
