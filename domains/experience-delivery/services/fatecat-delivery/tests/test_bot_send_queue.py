#!/usr/bin/env python3
"""测试 Telegram Bot 本地补发 outbox。"""

import importlib
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import _paths

_ENV_PATH = Path(tempfile.mkdtemp(prefix="fatecat-bot-queue-test-")) / ".env"
_ENV_PATH.write_text("FATE_BOT_TOKEN=test-token\nFATE_BOT_DRY_RUN=1\n", encoding="utf-8")
_paths.startup_check = lambda: True
_paths.get_env_file = lambda: _ENV_PATH

bot = importlib.import_module("bot")


def _task() -> dict:
    return {
        "type": "media_group",
        "chat_id": 12345,
        "header": "报告见附件",
        "parse_mode": "Markdown",
        "files": [("/tmp/report.txt", "report.txt")],
    }


def test_send_queue_assigns_id_and_deduplicates(monkeypatch, tmp_path):
    queue_path = tmp_path / "send_queue.jsonl"
    monkeypatch.setattr(bot, "QUEUE_PATH", queue_path)

    bot._enqueue_send_task(_task())
    bot._enqueue_send_task(_task())

    tasks = bot._load_queue()
    assert len(tasks) == 1
    assert tasks[0]["id"]
    assert tasks[0]["attempts"] == 0
    assert tasks[0]["queued_at"]


def test_send_queue_save_is_atomic_and_ack_removes_file(monkeypatch, tmp_path):
    queue_path = tmp_path / "send_queue.jsonl"
    monkeypatch.setattr(bot, "QUEUE_PATH", queue_path)

    bot._save_queue([_task()])
    assert queue_path.exists()
    assert not queue_path.with_suffix(".jsonl.tmp").exists()

    bot._save_queue([])
    assert not queue_path.exists()
