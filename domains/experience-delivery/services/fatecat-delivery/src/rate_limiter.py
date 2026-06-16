"""
请求限流与队列机制
- 全局并发限制
- 有界请求队列
- 可选用户冷却与每日限额
"""

# Ponytail existence: current consumer is Telegram Bot flow; owner is fatecat-delivery.
# Verification: tests cover queue limits and slot release; ceiling is single-process deployment.

import asyncio
import os
import time
from datetime import datetime
from functools import wraps
from zoneinfo import ZoneInfo

# ========== 配置 ==========
MAX_CONCURRENT = int(os.getenv("FATE_BOT_MAX_CONCURRENT", "1") or "1")
QUEUE_MAX_SIZE = int(os.getenv("FATE_BOT_QUEUE_MAX_SIZE", "20") or "20")
USER_COOLDOWN_SECONDS = int(os.getenv("FATE_BOT_USER_COOLDOWN_SECONDS", "0") or "0")
USER_DAILY_LIMIT = int(os.getenv("FATE_BOT_USER_DAILY_LIMIT", "0") or "0")
_LOCAL_TZ = ZoneInfo("Asia/Shanghai")


class QueueFullError(RuntimeError):
    """Bot 计算队列已满。"""


# ========== 状态 ==========
_semaphore = asyncio.Semaphore(MAX_CONCURRENT)
_queue_size = 0
_user_last_request: dict[int, float] = {}
_user_daily_counts: dict[tuple[int, str], int] = {}


def _today_key(user_id: int) -> tuple[int, str]:
    return user_id, datetime.now(_LOCAL_TZ).date().isoformat()


def _busy_message() -> str:
    return "服务器繁忙，请稍后再试"


def check_rate_limit(user_id: int) -> tuple[bool, str]:
    """
    检查用户是否可以发起请求。
    返回: (是否允许, 拒绝原因)
    """
    if _queue_size >= QUEUE_MAX_SIZE:
        return False, _busy_message()

    now = time.time()
    if USER_COOLDOWN_SECONDS > 0:
        last_request = _user_last_request.get(user_id)
        if last_request is not None:
            wait_seconds = int(USER_COOLDOWN_SECONDS - (now - last_request))
            if wait_seconds > 0:
                return False, f"请求过于频繁，请 {wait_seconds} 秒后再试"

    if USER_DAILY_LIMIT > 0:
        used_today = _user_daily_counts.get(_today_key(user_id), 0)
        if used_today >= USER_DAILY_LIMIT:
            return False, "今日排盘次数已达上限，请明日再试"

    return True, ""


def record_request(user_id: int):
    """记录已接受的用户请求；用户冷却/每日限额默认关闭。"""
    _user_last_request[user_id] = time.time()
    if USER_DAILY_LIMIT > 0:
        today_key = _today_key(user_id)
        _user_daily_counts[today_key] = _user_daily_counts.get(today_key, 0) + 1


async def acquire_slot():
    """获取计算槽位；队列已满时立即失败，不无限等待。"""
    global _queue_size
    if _queue_size >= QUEUE_MAX_SIZE:
        raise QueueFullError(_busy_message())
    _queue_size += 1
    try:
        await _semaphore.acquire()
    except Exception:
        _queue_size = max(0, _queue_size - 1)
        raise


def release_slot():
    """释放计算槽位。"""
    global _queue_size
    _queue_size = max(0, _queue_size - 1)
    _semaphore.release()


def get_queue_status() -> dict:
    """获取队列状态。"""
    return {
        "backend": "memory",
        "scope": "single_process",
        "concurrent": MAX_CONCURRENT - _semaphore._value,
        "max_concurrent": MAX_CONCURRENT,
        "queue_size": _queue_size,
        "queue_max": QUEUE_MAX_SIZE,
        "user_cooldown_seconds": USER_COOLDOWN_SECONDS,
        "user_daily_limit": USER_DAILY_LIMIT,
    }


def rate_limit(func):
    """装饰器：自动限流。"""

    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id

        allowed, reason = check_rate_limit(user_id)
        if not allowed:
            await update.message.reply_text(f"⏳ {reason}")
            return

        try:
            await acquire_slot()
        except QueueFullError as exc:
            await update.message.reply_text(f"⏳ {exc}")
            return

        record_request(user_id)

        try:
            return await func(update, context, *args, **kwargs)
        finally:
            release_slot()

    return wrapper
