# FateCat Self Review

审查时间：2026-05-06 HKT +0800

## Verdict

`PASS` for repository handoff and third-party audit readiness. `WARN` for direct public production reuse until live Bot / production environment / real credential verification is completed.

当前 worktree 已完成本轮安全、报告体系、前端隐私和交付卫生修复；本地完整验收通过。远端 `main` 在提交 `ba10ede` 上的 GitHub Actions 已通过；包含本轮修复的新提交需 push 后再以远端 CI 为准。

## Current Evidence

| Item | Evidence |
|---|---|
| Branch | `main` |
| Base HEAD before this fix | `ba10edea76547c9239939017b4713c19c3f8e5e9` |
| Remote CI for base | success, `https://github.com/tukuaiai/fatecat/actions/runs/25407053025` |
| Local acceptance | `bash scripts/acceptance.sh --with-dev` passed |
| pytest | `40 passed in 7.52s` inside acceptance |
| ruff | `All checks passed!` |
| format | `87 files already formatted` |
| mypy | `Success: no issues found in 21 source files` |
| API smoke | passed, `http://127.0.0.1:8001/health` |
| Bot smoke | dry-run passed |
| Export hygiene | `export hygiene ok` before and after exported smoke |
| Old deploy pack smoke | `bash project/assets/deploy/pack.sh` passed; archive scan only allowed `.env.example` matches |

## Fixed In This Round

- API 记录接口增加 `FATE_API_TOKEN` 保护；支持 `X-FateCat-API-Key` 与 `Authorization: Bearer ...`。
- CORS 改为 `FATE_CORS_ALLOW_ORIGINS` allowlist，默认空列表，不再默认 `*`。
- API 未处理异常对外统一返回泛化错误，详细异常只进服务端日志。
- 默认 `bazi` 计算使用 `extensions=True`，不再为默认八字报告计算紫微扩展；`ziwei` 独立体系才开启。
- 新增 `/api/v1/report/markdown`，通过 `options.reportSystem` 输出 `bazi/ziwei/jianchu/bone` 独立 Markdown。
- Telegram 确认页新增四个体系选择按钮，输出文件名带体系标签。
- Web/API/Bot 生成用户可见报告时隐藏非北京类真实出生地区，真实地点只用于经纬度解析、计算和受控记录。
- 旧部署打包脚本清理 `.env`、私钥、证书、SQLite、日志和常见凭证 JSON，并在残留时拒绝打包。
- `scripts/bootstrap.sh` 使用 `requirements.lock.txt` 作为 constraints，降低依赖漂移。
- `project/.gitignore` 增加 `.dist/`，避免部署包产物进入未跟踪工作树。

## Remaining Risks

### Production Gaps

- Live Telegram Bot 未用真实 `FATE_BOT_TOKEN` 完成端到端发送验证。
- 真实 webhook / 生产服务器 / systemd / 容器部署 / 生产数据库权限仍需外部环境验证。
- `FATE_API_TOKEN` 是全局 token 保护，不是多租户 owner/admin 级认证；若要公网多用户生产，应接入成熟认证层。

### Supply Chain / Vendor

- `project/assets/vendor/vendor_sources.json` 仍缺少完整 license、commit/tag、sha256、retrievedAt、distributionAllowed 字段。
- 部分 vendor 来源说明仍需人工许可证复查，当前只能证明 vendor health 通过，不能替代法律审计。

### Product Follow-up

- 未来功能仍应按独立契约重建：健康预警、黄历、六爻、梅花、奇门、大六壬、择日、风水、占星、姓名合婚等不能回塞进默认八字报告。
- 前端地区隐藏策略已按“非北京不展示真实地区”实现；若未来要显示更多地区，需要先明确隐私规则和审计口径。

## Current Gate

- Local engineering gate: PASS
- Third-party audit readiness: PASS with remaining risks documented
- Public production release: WARN until live Bot / production network / real credentials / multi-user auth policy are verified
