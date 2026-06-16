#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

require_live_bot="0"
api_url=""
skip_bootstrap="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/production-readiness.sh [--require-live-bot] [--api-url <url>] [--skip-bootstrap]

说明:
  - 检查生产配置是否具备最小安全边界：API 鉴权、CORS allowlist、真实 token 口径、.env 不入库
  - --require-live-bot 会调用 scripts/live-bot-smoke.sh，真实连接 Telegram Bot API
  - --api-url 会请求 <url>/health，验证已部署 API 的 live health
  - 不传真实凭证时不会伪造线上通过；需要外部环境的项会直接失败或标注未执行
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require-live-bot)
      require_live_bot="1"
      shift
      ;;
    --api-url)
      [[ $# -ge 2 ]] || usage_error "--api-url 缺少参数"
      api_url="${2%/}"
      shift 2
      ;;
    --skip-bootstrap)
      skip_bootstrap="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage_error "未知参数: $1"
      ;;
  esac
done

if [[ "${skip_bootstrap}" != "1" ]]; then
  bash "${script_dir}/bootstrap.sh" >/dev/null
fi

runtime_root="$(resolve_runtime_root)"
config_dir="$(runtime_config_dir "${runtime_root}")"
env_file="${config_dir}/.env"
env_rel="${env_file#${runtime_root}/}"

if git -C "${runtime_root}" ls-files --error-unmatch "${env_rel}" >/dev/null 2>&1; then
  die "生产 .env 已进入 Git 跟踪，必须移除并轮换所有相关凭证"
fi

"${runtime_root}/.venv/bin/python" - "${env_file}" <<'PY'
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import dotenv_values

env_path = Path(sys.argv[1])
file_values = dotenv_values(env_path) if env_path.exists() else {}


def value(name: str) -> str:
    return (os.getenv(name) or file_values.get(name) or "").strip()


def fail(message: str) -> None:
    print(f"[production-readiness] FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[production-readiness] OK: {message}")


def assert_real_secret(name: str, secret: str) -> None:
    if not secret:
        fail(f"缺少 {name}")
    lowered = secret.lower()
    blocked = ("placeholder", "smoke", "your_", "change-me", "changeme", "你的token", "测试")
    if any(marker in lowered for marker in blocked):
        fail(f"{name} 看起来是占位值")


def assert_int_setting(name: str, default: int, minimum: int, maximum: int | None = None) -> int:
    raw = value(name)
    text = raw or str(default)
    try:
        parsed = int(text)
    except ValueError:
        fail(f"{name} 必须是整数")
    if parsed < minimum:
        fail(f"{name} 必须 >= {minimum}")
    if maximum is not None and parsed > maximum:
        fail(f"{name} 必须 <= {maximum}")
    suffix = "默认值" if not raw else "显式配置"
    ok(f"{name}={parsed} ({suffix})")
    return parsed


cors = value("FATE_CORS_ALLOW_ORIGINS")
if not cors:
    fail("FATE_CORS_ALLOW_ORIGINS 为空；公网生产必须配置明确 allowlist")
origins = [item.strip() for item in cors.split(",") if item.strip()]
if "*" in origins:
    fail("FATE_CORS_ALLOW_ORIGINS 不允许包含 *")
ok(f"CORS allowlist 已配置 {len(origins)} 项")

admin_tokens = [value("FATE_API_TOKEN"), value("FATE_API_ADMIN_TOKEN")]
user_tokens_raw = value("FATE_API_USER_TOKENS")
records_enabled = value("FATE_RECORDS_ENABLED").lower() not in {"0", "false", "no", "off"}
has_auth = any(admin_tokens) or bool(user_tokens_raw)
if records_enabled and not has_auth:
    fail("记录接口已启用但缺少鉴权 token：FATE_API_TOKEN/FATE_API_ADMIN_TOKEN/FATE_API_USER_TOKENS 至少配置一个")
if not records_enabled:
    ok("FATE_RECORDS_ENABLED 已关闭；当前按无状态公共服务验收")

for token_name, token in (("FATE_API_TOKEN", admin_tokens[0]), ("FATE_API_ADMIN_TOKEN", admin_tokens[1])):
    if records_enabled and token:
        assert_real_secret(token_name, token)

if records_enabled and user_tokens_raw:
    user_pairs = [item.strip() for item in user_tokens_raw.split(",") if item.strip()]
    if not user_pairs:
        fail("FATE_API_USER_TOKENS 格式为空")
    for pair in user_pairs:
        user_id, sep, token = pair.partition(":")
        if not sep or not user_id.strip() or not token.strip():
            fail("FATE_API_USER_TOKENS 必须使用 user_id:token,user_id2:token2 格式")
        assert_real_secret(f"FATE_API_USER_TOKENS[{user_id.strip()}]", token.strip())
    ok(f"用户级 API token 已配置 {len(user_pairs)} 项")
elif records_enabled:
    ok("未配置用户级 API token；当前只使用 admin token")

bot_token = value("FATE_BOT_TOKEN")
if bot_token:
    assert_real_secret("FATE_BOT_TOKEN", bot_token)
    ok("FATE_BOT_TOKEN 已配置为非占位值")
else:
    print("[production-readiness] WARN: 未配置 FATE_BOT_TOKEN；Bot live 验收无法执行")

assert_int_setting("FATE_MAX_REQUEST_BYTES", 1_048_576, 1024, 10 * 1024 * 1024)
assert_int_setting("FATE_REQUEST_TIMEOUT_SECONDS", 30, 1, 120)
assert_int_setting("FATE_MAX_INFLIGHT_CALCULATIONS", 2, 1, 64)
rate_limit = assert_int_setting("FATE_RATE_LIMIT_PER_MINUTE", 120, 0, 10_000)
if rate_limit == 0:
    fail("FATE_RATE_LIMIT_PER_MINUTE=0 会关闭公网限流")

replicas = assert_int_setting("FATE_DEPLOYMENT_REPLICAS", 1, 1, 100)
rate_limit_backend = (value("FATE_RATE_LIMIT_BACKEND") or "memory").lower()
allowed_rate_limit_backends = {"memory", "gateway", "redis", "waf", "external"}
if rate_limit_backend not in allowed_rate_limit_backends:
    fail("FATE_RATE_LIMIT_BACKEND 必须是 memory/gateway/redis/waf/external")
if replicas > 1 and rate_limit_backend == "memory":
    fail("多副本公网部署不能使用单进程 memory 限流；请改用 gateway/redis/waf/external")
if rate_limit_backend == "memory":
    ok("当前使用单实例内存限流；仅适合单副本或前置网关已限流场景")
else:
    ok(f"已声明外部限流后端：{rate_limit_backend}")

if value("FATE_EDGE_BODY_LIMIT_ENABLED").lower() in {"1", "true", "yes"}:
    ok("已声明反向代理/CDN 层请求体上限；应用层仍保留流式兜底限制")
else:
    print("[production-readiness] WARN: 未声明 FATE_EDGE_BODY_LIMIT_ENABLED；公网最好在 Nginx/Traefik/Cloudflare 层限制请求体")

if value("FATE_TRUST_PROXY_HEADERS").lower() in {"1", "true", "yes"}:
    ok("已启用可信反向代理头解析；必须确保只有可信代理能访问服务直连端口")
else:
    print("[production-readiness] WARN: 未启用 FATE_TRUST_PROXY_HEADERS；反向代理后限流会按代理 IP 聚合")

if value("FATE_ENABLE_HSTS").lower() in {"1", "true", "yes"}:
    ok("已启用应用层 HSTS 响应头")
else:
    print("[production-readiness] WARN: 未启用 FATE_ENABLE_HSTS；若由反向代理设置 HSTS，可忽略此项")

ok("生产配置静态门禁通过")
PY

if [[ -n "${api_url}" ]]; then
  echo "[production-readiness] live API health: ${api_url}/health"
  curl -fsS "${api_url}/health" >/dev/null
  echo "[production-readiness] OK: live API health 通过"
  echo "[production-readiness] live API readiness: ${api_url}/ready"
  curl -fsS "${api_url}/ready" >/dev/null
  echo "[production-readiness] OK: live API readiness 通过"
  echo "[production-readiness] live API metrics: ${api_url}/metrics"
  curl -fsS "${api_url}/metrics" | grep -q 'fatecat_requests_total'
  echo "[production-readiness] OK: live API metrics 通过"
else
  echo "[production-readiness] SKIP: 未提供 --api-url，外部 API 连通验证待执行"
fi

if [[ "${require_live_bot}" == "1" ]]; then
  echo "[production-readiness] live Bot smoke"
  bash "${script_dir}/live-bot-smoke.sh"
else
  echo "[production-readiness] SKIP: 未提供 --require-live-bot，真实 Bot 连通验证待执行"
fi

echo "[production-readiness] done"
