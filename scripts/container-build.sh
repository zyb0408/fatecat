#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

image="fatecat-delivery:local"
dockerfile="infra/docker/Dockerfile.delivery"
progress="auto"

usage() {
  cat <<'EOF'
用法:
  bash scripts/container-build.sh [--image <name:tag>] [--dockerfile <path>] [--progress auto|plain]

说明:
  - 构建 FateCat delivery 容器镜像。
  - 默认镜像名：fatecat-delivery:local
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image)
      [[ $# -ge 2 ]] || usage_error "--image 缺少参数"
      image="$2"
      shift 2
      ;;
    --dockerfile)
      [[ $# -ge 2 ]] || usage_error "--dockerfile 缺少参数"
      dockerfile="$2"
      shift 2
      ;;
    --progress)
      [[ $# -ge 2 ]] || usage_error "--progress 缺少参数"
      progress="$2"
      shift 2
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

case "${progress}" in
  auto|plain|tty|rawjson)
    ;;
  *)
    usage_error "--progress 只支持 auto、plain、tty 或 rawjson"
    ;;
esac

docker build --progress="${progress}" -f "${dockerfile}" -t "${image}" "${enterprise_project_root}"
echo "[container-build] built ${image}"
