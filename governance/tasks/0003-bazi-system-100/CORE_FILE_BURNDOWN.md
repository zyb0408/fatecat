# Core File Burndown

任务节点：`TP-09.01`

## 结论

当前不做大爆炸重写。拆分路线必须遵守三条线：

- 领域算法留在 `domains/fate-analysis/services/fate-core/src/fate_core`。
- delivery 只做 API/Web/Bot 交付，不承载新领域算法。
- 每个拆分候选必须先绑定行为保持测试，再移动代码。

## 当前核心文件体量

```text
2500 domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py
1941 domains/experience-delivery/services/fatecat-delivery/src/report_generator.py
1375 domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py
1152 domains/experience-delivery/services/fatecat-delivery/src/bot.py
1015 domains/experience-delivery/services/fatecat-delivery/src/main.py
 782 domains/experience-delivery/services/fatecat-delivery/src/web_ui.py
  30 domains/experience-delivery/services/fatecat-delivery/src/bazi_calculator.py
  25 domains/fate-analysis/services/fate-core/src/fate_core/adapters/lunar_calendar.py
```

## 拆分候选

### `fate_core/kernel/bazi_calculator.py`

职责：八字 kernel 主体。

候选切片：

- calendar/time boundary：节气、真太阳时、子时、起运。
- strength：日主强弱、月令、通根、透干。
- pattern：常规格局、高级格局、从格、化气、专旺。
- relation：天干合化、地支冲合刑害破。
- yongshen：调候、扶抑、通关、病药、策略裁决。
- fortune/topic：大运流年流月触发与专题 profile。
- evidence：规则证据装配、riskBoundary、ruleIds。

行为保持测试：

- `tests/regression/test_bazi_golden_coverage_matrix.py`
- `tests/regression/test_bazi_ziwei_rule_depth.py`
- `tests/regression/test_solar_terms_golden.py`
- `tests/regression/test_calendar_oracle_contract.py`
- `tests/regression/test_strength_mapping.py`

回滚路径：

- 保留 `BaziCalculator` public facade。
- 每次只迁移一个纯函数/策略模块。
- 新模块输出先与旧 facade golden 对齐。
- 若任一 golden 或 rule-depth 回归失败，回退该切片，不回滚其他已验证切片。

### `fate_core/usecases/calculate_pure_analysis.py`

职责：纯分析用例编排与输出契约装配。

候选切片：

- payload normalization。
- field registry/filter。
- capability projection。
- evidence/rule-depth projection。
- topic profile projection。

行为保持测试：

- `tests/regression/fate_core/test_pure_analysis_usecase.py`
- `tests/regression/test_api_contracts.py`
- `tests/regression/test_capability_protocol.py`
- `domains/fate-analysis/services/fate-core/tests/test_service_contract.py`

回滚路径：

- 保留 `calculate_pure_analysis` 入口签名。
- 提取只读 helper，不改变返回 schema。
- 任何 schema diff 必须先进入 contracts 测试。

### `fatecat-delivery/src/report_generator.py`

职责：Markdown 报告生成与内容边界。

候选切片：

- bazi section renderer。
- ziwei/liuyao/xingming section renderer。
- disclaimer/riskBoundary renderer。
- evidence fold renderer。
- report hide/filter policy。

行为保持测试：

- `tests/regression/test_bazi_statement_golden.py`
- `tests/regression/test_api_contracts.py`
- `tests/regression/test_web_html.py`
- `domains/experience-delivery/services/fatecat-delivery/tests/test_service_contract.py`

回滚路径：

- 保留 `generate_full_report(report_system)` 入口。
- 先提取纯渲染函数，比较 Markdown golden。
- 不在拆分过程中改报告语义。

### `fatecat-delivery/src/main.py`

职责：FastAPI 入口、middleware、API routing、health/readiness/metrics。

候选切片：

- middleware：request id、body limit、timeout、error mapping。
- routers：bazi/pure-analysis/web/health。
- observability：metrics、ready、runtime metadata。
- validation：输入错误统一 4xx。

行为保持测试：

- `tests/regression/test_api_contracts.py`
- `tests/regression/test_web_html.py`
- `domains/experience-delivery/services/fatecat-delivery/tests/test_rate_limiter.py`
- `domains/experience-delivery/services/fatecat-delivery/tests/test_service_contract.py`

回滚路径：

- 保留 FastAPI app factory/入口。
- 先 router extract，不改变路径和状态码。
- 每次切片后跑 API contract。

### `fatecat-delivery/src/web_ui.py`

职责：原生 HTML `/web` 页面与服务端 Markdown 输出。

候选切片：

- layout renderer。
- input form renderer。
- report output renderer。
- details/meta renderer。
- TradeCat Labs attribution renderer。

行为保持测试：

- `tests/regression/test_web_html.py`
- `tests/regression/test_api_contracts.py`

回滚路径：

- 保留 `/web` 入口和原生 HTML 表单。
- 不引入重前端。
- 每次只变一块 HTML renderer 并截图/HTML 断言。

### `fatecat-delivery/src/bot.py`

职责：Telegram Bot 交付、队列、重试与命令处理。

候选切片：

- command parser。
- send queue/outbox。
- retry/backoff。
- report delivery adapter。

行为保持测试：

- `domains/experience-delivery/services/fatecat-delivery/tests/test_bot_send_queue.py`
- `domains/experience-delivery/services/fatecat-delivery/tests/test_complete_integration.py`
- `scripts/live-bot-smoke.sh` 仅在有真实 token 时使用。

回滚路径：

- 保留 bot 对外命令行为。
- 先把队列/发送抽成 adapter。
- dry-run 和 fake bot 测试通过前不接生产 token。

## 不拆对象

- `fatecat-delivery/src/bazi_calculator.py` 当前只有 30 行，定位为 delivery 到 fate-core 的薄兼容入口；不在这里新增领域算法。
- `fate_core/adapters/lunar_calendar.py` 当前只有 25 行，定位为 `lunar-python` provider adapter；不拆。

## Gate 判定

- `每个拆分候选有行为保持测试和回滚路径`：`PASS`
- `不做大爆炸重写`：`PASS`

本文件只建立拆分路线和验收边界，不执行结构迁移。真正拆分必须进入后续 `TP-09.02` 和对应领域任务节点。
