#!/usr/bin/env python3
"""测试 Bot 请求限流、队列背压与可选用户限制。"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import rate_limiter


def _reset_state(monkeypatch):
    monkeypatch.setattr(rate_limiter, "_queue_size", 0)
    monkeypatch.setattr(rate_limiter, "_user_last_request", {})
    monkeypatch.setattr(rate_limiter, "_user_daily_counts", {})


def test_user_limits_are_disabled_by_default(monkeypatch):
    _reset_state(monkeypatch)
    monkeypatch.setattr(rate_limiter, "USER_COOLDOWN_SECONDS", 0)
    monkeypatch.setattr(rate_limiter, "USER_DAILY_LIMIT", 0)

    rate_limiter.record_request(12345)
    allowed, reason = rate_limiter.check_rate_limit(12345)

    assert allowed is True
    assert reason == ""


def test_queue_limit_still_blocks_when_queue_full(monkeypatch):
    monkeypatch.setattr(rate_limiter, "_queue_size", rate_limiter.QUEUE_MAX_SIZE)

    allowed, reason = rate_limiter.check_rate_limit(12345)

    assert allowed is False
    assert "服务器繁忙" in reason


def test_acquire_slot_rejects_when_queue_full(monkeypatch):
    monkeypatch.setattr(rate_limiter, "_queue_size", rate_limiter.QUEUE_MAX_SIZE)

    async def run():
        try:
            await rate_limiter.acquire_slot()
        except rate_limiter.QueueFullError as exc:
            return str(exc)
        return ""

    assert "服务器繁忙" in asyncio.run(run())


def test_optional_user_cooldown_blocks_recent_request(monkeypatch):
    _reset_state(monkeypatch)
    monkeypatch.setattr(rate_limiter, "USER_COOLDOWN_SECONDS", 60)

    rate_limiter.record_request(12345)
    allowed, reason = rate_limiter.check_rate_limit(12345)

    assert allowed is False
    assert "请求过于频繁" in reason


def test_optional_daily_limit_blocks_after_quota(monkeypatch):
    _reset_state(monkeypatch)
    monkeypatch.setattr(rate_limiter, "USER_DAILY_LIMIT", 1)

    rate_limiter.record_request(12345)
    allowed, reason = rate_limiter.check_rate_limit(12345)

    assert allowed is False
    assert "今日排盘次数已达上限" in reason


def test_queue_status_exposes_product_limit_policy(monkeypatch):
    _reset_state(monkeypatch)
    monkeypatch.setattr(rate_limiter, "USER_COOLDOWN_SECONDS", 0)
    monkeypatch.setattr(rate_limiter, "USER_DAILY_LIMIT", 0)

    status = rate_limiter.get_queue_status()

    assert status["backend"] == "memory"
    assert status["scope"] == "single_process"
    assert status["queue_max"] == rate_limiter.QUEUE_MAX_SIZE
    assert status["user_cooldown_seconds"] == 0
    assert status["user_daily_limit"] == 0
