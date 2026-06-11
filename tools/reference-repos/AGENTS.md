# AGENTS.md - tools/reference-repos

## 目录用途

`tools/reference-repos/` 保存第三方开源仓库快照与 vendor manifest，是命理算法复用的供应链参考层。

## 目录结构

```text
tools/reference-repos/
├── AGENTS.md
├── README.md
├── vendor_sources.json
├── github/
└── web/
```

## 职责边界

- `vendor_sources.json`：所有 vendor 快照的来源、用途、许可证、revision 和 sha256 登记。
- `github/`：来自 GitHub 的只读参考实现；禁止直接魔改 vendor 源码。
- `web/`：网页参考快照，只能作为 fixture / 解析参考，不承载真实用户数据。
- 服务代码通过 adapter、manifest 和明确路径读取这里，不把供应商代码复制进业务模块。
