#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

usage() {
  cat <<'EOF'
用法:
  FATE_BOT_TOKEN=<real-token> bash scripts/live-bot-smoke.sh

说明:
  - 真实连接 Telegram Bot API 并调用 get_me()
  - 不接受 delivery-smoke 的 placeholder token
  - 若未传环境变量，会读取 infra/environments/local/.env
EOF
}

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
  "")
    ;;
  *)
    usage_error "未知参数: $1"
    ;;
esac

bash "${script_dir}/bootstrap.sh" >/dev/null
runtime_root="$(resolve_runtime_root)"
config_dir="$(runtime_config_dir "${runtime_root}")"
env_file="${config_dir}/.env"

"${runtime_root}/.venv/bin/python" - "${env_file}" <<'PY'
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import dotenv_values
from telegram import Bot

env_path = Path(sys.argv[1])
env_values = dotenv_values(env_path) if env_path.exists() else {}

token = os.getenv("FATE_BOT_TOKEN") or env_values.get("FATE_BOT_TOKEN") or ""
token = token.strip()
if not token:
    print(f"缺少真实 FATE_BOT_TOKEN；请通过环境变量或 {env_path} 提供。", file=sys.stderr)
    raise SystemExit(2)

blocked_markers = ("placeholder", "smoke", "your_bot_token_here", "你的token")
if any(marker in token.lower() for marker in blocked_markers):
    print("拒绝使用 placeholder/smoke token 进行真实 Bot 验收。", file=sys.stderr)
    raise SystemExit(2)


async def main() -> None:
    bot = Bot(token=token)
    me = await bot.get_me()
    print(f"live bot smoke ok: id={me.id} username=@{me.username or ''}")


asyncio.run(main())
PY
