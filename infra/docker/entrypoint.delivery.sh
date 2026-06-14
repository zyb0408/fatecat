#!/usr/bin/env sh
set -eu

: "${FATE_SERVICE_HOST:=0.0.0.0}"
: "${FATE_SERVICE_PORT:=8001}"

exec python -m uvicorn main:app --host "${FATE_SERVICE_HOST}" --port "${FATE_SERVICE_PORT}"
