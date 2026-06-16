"""交付服务环境配置读取。"""

from __future__ import annotations

import os


def env_int(name: str, default: int, *, minimum: int = 0) -> int:
    """读取整数环境变量，非法值回落到默认值。"""
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(value, minimum)


def env_flag(name: str) -> bool:
    """读取布尔环境变量。"""
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes"}


def cors_allow_origins() -> list[str]:
    """读取 CORS allowlist；默认不放开公网跨域。"""
    raw = os.getenv("FATE_CORS_ALLOW_ORIGINS", "").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


__all__ = ["cors_allow_origins", "env_flag", "env_int"]
