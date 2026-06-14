#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

infer_ghcr_owner() {
  local origin_url
  local slug

  if [[ -n "${GITHUB_REPOSITORY_OWNER:-}" ]]; then
    echo "${GITHUB_REPOSITORY_OWNER}"
    return
  fi
  if [[ -n "${GITHUB_REPOSITORY:-}" && "${GITHUB_REPOSITORY}" == */* ]]; then
    echo "${GITHUB_REPOSITORY%%/*}"
    return
  fi

  origin_url="$(git -C "${enterprise_project_root}" config --get remote.origin.url 2>/dev/null || true)"
  case "${origin_url}" in
    https://github.com/*/*)
      slug="${origin_url#https://github.com/}"
      ;;
    git@github.com:*)
      slug="${origin_url#git@github.com:}"
      ;;
    *)
      slug=""
      ;;
  esac
  slug="${slug%.git}"
  if [[ "${slug}" == */* ]]; then
    echo "${slug%%/*}"
    return
  fi

  echo "tradecatlabs"
}

image="ghcr.io/$(infer_ghcr_owner)/fatecat-delivery"
tag="$(git -C "${enterprise_project_root}" rev-parse --short=12 HEAD)"
push="0"
smoke="1"

usage() {
  cat <<'EOF'
用法:
  bash scripts/container-release.sh [--image <registry/repo>] [--tag <tag>] [--push] [--skip-smoke]

说明:
  - 构建 <image>:<tag>。
  - 默认先运行容器 smoke；只有显式 --push 才推送到 registry。
  - 推送前请先完成 docker login，例如：
    echo "$GHCR_TOKEN" | docker login ghcr.io -u <user> --password-stdin
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image)
      [[ $# -ge 2 ]] || usage_error "--image 缺少参数"
      image="${2%:}"
      shift 2
      ;;
    --tag)
      [[ $# -ge 2 ]] || usage_error "--tag 缺少参数"
      tag="$2"
      shift 2
      ;;
    --push)
      push="1"
      shift
      ;;
    --skip-smoke)
      smoke="0"
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

full_image="${image}:${tag}"
bash "${script_dir}/container-build.sh" --image "${full_image}"

if [[ "${smoke}" == "1" ]]; then
  bash "${script_dir}/container-smoke.sh" --image "${full_image}" --skip-build
fi

if [[ "${push}" == "1" ]]; then
  docker push "${full_image}"
  echo "[container-release] pushed ${full_image}"
else
  echo "[container-release] built ${full_image}; skip push"
fi
