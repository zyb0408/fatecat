"""Telegram Bot 日志初始化。"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_bot_logger(logs_dir: Path) -> logging.Logger:
    """初始化 Bot 文件和标准输出日志。"""
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("fate.bot")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
    file_handler = RotatingFileHandler(logs_dir / "bot.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


__all__ = ["setup_bot_logger"]
