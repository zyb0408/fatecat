# fatecat-delivery

FateCat 交付服务，负责把纯分析与独立 capability 结果输出到 Web、API、Telegram 和 Markdown 报告。

## 当前状态

- Lifecycle: `active-canonical`
- 当前源码根：`domains/experience-delivery/services/fatecat-delivery/src/`
- 运行资产：`contracts/fate/`、`infra/environments/local/`、`tools/reference-repos/`

## 验证入口

```bash
python -m pytest -q domains/experience-delivery/services/fatecat-delivery/tests
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target api
```

## 维护原则

- 不改变 API 路径和响应模型。
- 不改变 Web 表单语义和 Markdown 输出边界。
- 不把未来 capability 混入默认综合八字报告。
