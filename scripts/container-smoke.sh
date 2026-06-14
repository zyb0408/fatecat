#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

image="fatecat-delivery:local"
host="127.0.0.1"
port="8002"
startup_timeout="60"
container_name="fatecat-delivery-smoke-$(date +%Y%m%d%H%M%S)"
container_id=""
response_file=""
skip_build="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/container-smoke.sh [--image <name:tag>] [--host <host>] [--port <port>]
                                  [--startup-timeout <seconds>] [--skip-build]

说明:
  - 可选构建镜像后启动一次临时容器。
  - 验证 /health 与 /api/v1/bazi/pure-analysis，结束后自动清理容器。
EOF
}

cleanup() {
  if [[ -n "${container_id}" ]]; then
    docker rm -f "${container_id}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${response_file}" && -f "${response_file}" ]]; then
    rm -f "${response_file}"
  fi
}

trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image)
      [[ $# -ge 2 ]] || usage_error "--image 缺少参数"
      image="$2"
      shift 2
      ;;
    --host)
      [[ $# -ge 2 ]] || usage_error "--host 缺少参数"
      host="$2"
      shift 2
      ;;
    --port)
      [[ $# -ge 2 ]] || usage_error "--port 缺少参数"
      port="$2"
      shift 2
      ;;
    --startup-timeout)
      [[ $# -ge 2 ]] || usage_error "--startup-timeout 缺少参数"
      startup_timeout="$2"
      shift 2
      ;;
    --skip-build)
      skip_build="1"
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

ensure_command docker

case "${startup_timeout}" in
  ''|*[!0-9]*)
    usage_error "--startup-timeout 必须是正整数秒"
    ;;
esac

if [[ "${skip_build}" != "1" ]]; then
  bash "${script_dir}/container-build.sh" --image "${image}"
fi

container_id="$(
  docker run -d \
    --name "${container_name}" \
    -p "${host}:${port}:8001" \
    -e FATE_SERVICE_HOST=0.0.0.0 \
    -e FATE_SERVICE_PORT=8001 \
    "${image}"
)"

health_url="http://${host}:${port}/health"
ready_url="http://${host}:${port}/ready"
deadline=$((SECONDS + startup_timeout))
until curl -fsS "${health_url}" >/dev/null 2>&1; do
  if ! docker inspect -f '{{.State.Running}}' "${container_id}" 2>/dev/null | grep -q true; then
    echo "[container-smoke] 容器提前退出，日志如下：" >&2
    docker logs "${container_id}" >&2 || true
    exit 1
  fi
  if (( SECONDS >= deadline )); then
    echo "[container-smoke] ${startup_timeout}s 内未通过 health，日志如下：" >&2
    docker logs "${container_id}" >&2 || true
    exit 1
  fi
  sleep 1
done

curl -fsS "${ready_url}" >/dev/null

payload='{"name":"测试样本","gender":"male","birthDate":"1990-01-01","birthTime":"08:00:00","birthPlace":{"name":"北京市","longitude":116.4074,"latitude":39.9042,"timezone":"Asia/Shanghai"},"options":{"useTrueSolarTime":true,"daylightSaving":"auto","midnightMode":"early","calendarType":"solar"}}'
api_url="http://${host}:${port}/api/v1/bazi/pure-analysis"
response_file="$(mktemp)"
curl -fsS \
  -H 'Content-Type: application/json' \
  -d "${payload}" \
  "${api_url}" \
  > "${response_file}"

python3 - "${response_file}" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

body = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if body.get("success") is not True:
    raise SystemExit("pure-analysis response success != true")
data = body.get("data") or {}
if (data.get("input") or {}).get("gender") != "男":
    raise SystemExit("pure-analysis response gender normalization failed")
PY

echo "[container-smoke] ok image=${image} url=http://${host}:${port}/web"
