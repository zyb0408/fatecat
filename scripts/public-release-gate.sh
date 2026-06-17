#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

output_dir="/tmp/fatecat-public-release-$(date +%Y%m%d%H%M%S)"
api_url=""
skip_local_ci="0"
skip_delivery_smoke="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/public-release-gate.sh [--output <dir>] [--api-url <url>]
                                      [--skip-local-ci] [--skip-delivery-smoke]

说明:
  - 面向公开 Web 工作台发布前的本地门禁，不调用 GitHub Actions。
  - 默认执行 local-ci quick、发布策略检查、API smoke 和生产静态准入。
  - 传入 --api-url 时，会额外验证线上 /health、/ready、/metrics。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      [[ $# -ge 2 ]] || usage_error "--output 缺少参数"
      output_dir="$2"
      shift 2
      ;;
    --api-url)
      [[ $# -ge 2 ]] || usage_error "--api-url 缺少参数"
      api_url="${2%/}"
      shift 2
      ;;
    --skip-local-ci)
      skip_local_ci="1"
      shift
      ;;
    --skip-delivery-smoke)
      skip_delivery_smoke="1"
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

runtime_root="$(resolve_runtime_root)"
mkdir -p "${output_dir}"
output_dir="$(cd "${output_dir}" && pwd)"

run_step() {
  local name="$1"
  shift
  echo "[public-release] ${name}"
  "$@"
}

if [[ "${skip_local_ci}" != "1" ]]; then
  run_step "local-ci quick" bash "${script_dir}/local-ci.sh" \
    --profile quick \
    --output "${output_dir}/local-ci-quick"
fi

run_step "public release policy" bash "${script_dir}/check-public-release-policy.sh"

if [[ "${skip_delivery_smoke}" != "1" ]]; then
  run_step "delivery web smoke" env FATE_RECORDS_ENABLED=0 bash "${script_dir}/delivery-smoke.sh" \
    --target api \
    --response-file "${output_dir}/health.json" \
    --log-file "${output_dir}/delivery-smoke.log"
fi

readiness_args=(--skip-bootstrap)
if [[ -n "${api_url}" ]]; then
  readiness_args+=(--api-url "${api_url}")
fi

run_step "production readiness" env \
  FATE_CORS_ALLOW_ORIGINS="${FATE_CORS_ALLOW_ORIGINS:-https://tradecatlabs-fatecat.hf.space}" \
  FATE_RECORDS_ENABLED="${FATE_RECORDS_ENABLED:-0}" \
  FATE_DEPLOYMENT_REPLICAS="${FATE_DEPLOYMENT_REPLICAS:-1}" \
  FATE_RATE_LIMIT_BACKEND="${FATE_RATE_LIMIT_BACKEND:-gateway}" \
  FATE_EDGE_BODY_LIMIT_ENABLED="${FATE_EDGE_BODY_LIMIT_ENABLED:-1}" \
  FATE_TRUST_PROXY_HEADERS="${FATE_TRUST_PROXY_HEADERS:-1}" \
  FATE_ENABLE_HSTS="${FATE_ENABLE_HSTS:-1}" \
  bash "${script_dir}/production-readiness.sh" "${readiness_args[@]}"

{
  printf 'runtime_root=%s\n' "${runtime_root}"
  printf 'commit=%s\n' "$(git -C "${runtime_root}" rev-parse --verify HEAD 2>/dev/null || true)"
  printf 'api_url=%s\n' "${api_url:-not-provided}"
  printf 'timestamp=%s\n' "$(date -Iseconds)"
} > "${output_dir}/summary.txt"

echo "[public-release] done evidence=${output_dir}"
