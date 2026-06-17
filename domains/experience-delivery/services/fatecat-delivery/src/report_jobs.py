"""报告生成任务队列。

该模块只负责进程内任务生命周期：排队、执行、状态查询、TTL 过期和指标。
免费公开 Space 使用有界内存队列；自部署多副本场景应升级到 Redis/RQ/Celery。
"""

from __future__ import annotations

import logging
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass
from queue import Full, Queue
from threading import Lock, Thread
from typing import Any, Literal

from utils.timezone import now_cn

logger = logging.getLogger(__name__)

ReportJobStatus = Literal["queued", "running", "succeeded", "failed", "expired"]


class ReportJobQueueFull(RuntimeError):
    """报告任务队列已满。"""


class ReportJobNotFound(KeyError):
    """报告任务不存在或已清理。"""


@dataclass(frozen=True)
class ReportJobSnapshot:
    job_id: str
    kind: str
    status: ReportJobStatus
    report_system: str
    created_at: str
    expires_at: str
    started_at: str | None
    finished_at: str | None
    queue_position: int | None
    error: str | None
    result: Any | None
    input_summary: dict[str, Any]


@dataclass
class _ReportJob:
    job_id: str
    kind: str
    report_system: str
    task: Callable[[], Any] | None
    input_summary: dict[str, Any]
    created_monotonic: float
    expires_monotonic: float
    created_at: str
    expires_at: str
    status: ReportJobStatus = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    error: str | None = None
    result: Any | None = None


class ReportJobManager:
    """有界进程内报告任务队列。

    ponytail: 该实现只覆盖单进程免费公开入口；当副本数 >1、需要跨重启保留任务、
    或需要真实横向扩容时，应替换为 Redis/RQ/Celery 后端。
    """

    def __init__(self, *, max_workers: int, queue_size: int, ttl_seconds: int) -> None:
        self.max_workers = max(1, max_workers)
        self.queue_size = max(1, queue_size)
        self.ttl_seconds = max(60, ttl_seconds)
        self._queue: Queue[str] = Queue(maxsize=self.queue_size)
        self._jobs: dict[str, _ReportJob] = {}
        self._lock = Lock()
        self._started = False

    def start(self) -> None:
        with self._lock:
            if self._started:
                return
            self._started = True
            worker_count = self.max_workers
        for index in range(worker_count):
            thread = Thread(target=self._worker_loop, name=f"fatecat-report-worker-{index + 1}", daemon=True)
            thread.start()

    def submit(
        self,
        *,
        kind: str,
        report_system: str,
        task: Callable[[], Any],
        input_summary: dict[str, Any] | None = None,
    ) -> ReportJobSnapshot:
        self.start()
        self.cleanup_expired()
        job_id = secrets.token_urlsafe(18)
        created = now_cn()
        expires = created.timestamp() + self.ttl_seconds
        job = _ReportJob(
            job_id=job_id,
            kind=kind,
            report_system=report_system,
            task=task,
            input_summary=dict(input_summary or {}),
            created_monotonic=time.monotonic(),
            expires_monotonic=time.monotonic() + self.ttl_seconds,
            created_at=created.isoformat(),
            expires_at=now_cn().fromtimestamp(expires, tz=created.tzinfo).isoformat(),
        )
        with self._lock:
            if self._queue.full():
                raise ReportJobQueueFull("报告队列已满，请稍后再试")
            self._jobs[job_id] = job
            try:
                self._queue.put_nowait(job_id)
            except Full as exc:
                self._jobs.pop(job_id, None)
                raise ReportJobQueueFull("报告队列已满，请稍后再试") from exc
            return self._snapshot_locked(job)

    def get(self, job_id: str) -> ReportJobSnapshot:
        self.cleanup_expired()
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                raise ReportJobNotFound(job_id)
            self._expire_job_if_needed_locked(job)
            return self._snapshot_locked(job)

    def stats(self) -> dict[str, int]:
        self.cleanup_expired()
        with self._lock:
            counts = {"queued": 0, "running": 0, "succeeded": 0, "failed": 0, "expired": 0}
            for job in self._jobs.values():
                counts[job.status] += 1
            counts["queue_size"] = counts["queued"]
            counts["queue_max"] = self.queue_size
            counts["worker_max"] = self.max_workers
            counts["ttl_seconds"] = self.ttl_seconds
            return counts

    def cleanup_expired(self) -> None:
        now = time.monotonic()
        with self._lock:
            for job in self._jobs.values():
                if job.status in {"queued", "succeeded", "failed"} and now >= job.expires_monotonic:
                    job.status = "expired"
                    job.task = None
                    job.result = None

    def _worker_loop(self) -> None:
        while True:
            job_id = self._queue.get()
            try:
                self._run_job(job_id)
            finally:
                self._queue.task_done()

    def _run_job(self, job_id: str) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job or job.status != "queued":
                return
            self._expire_job_if_needed_locked(job)
            if job.status != "queued":
                return
            task = job.task
            job.status = "running"
            job.started_at = now_cn().isoformat()

        if task is None:
            return
        try:
            result = task()
        except Exception as exc:  # noqa: BLE001 - 任务边界必须捕获并转成 failed 状态。
            logger.exception("报告任务执行失败 job_id=%s", job_id)
            with self._lock:
                job = self._jobs.get(job_id)
                if job:
                    job.status = "failed"
                    job.error = str(exc) or type(exc).__name__
                    job.finished_at = now_cn().isoformat()
                    job.task = None
            return

        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            job.status = "succeeded"
            job.result = result
            job.finished_at = now_cn().isoformat()
            job.task = None

    def _expire_job_if_needed_locked(self, job: _ReportJob) -> None:
        if job.status in {"queued", "succeeded", "failed"} and time.monotonic() >= job.expires_monotonic:
            job.status = "expired"
            job.task = None
            job.result = None

    def _snapshot_locked(self, job: _ReportJob) -> ReportJobSnapshot:
        return ReportJobSnapshot(
            job_id=job.job_id,
            kind=job.kind,
            status=job.status,
            report_system=job.report_system,
            created_at=job.created_at,
            expires_at=job.expires_at,
            started_at=job.started_at,
            finished_at=job.finished_at,
            queue_position=self._queue_position_locked(job.job_id) if job.status == "queued" else None,
            error=job.error,
            result=job.result,
            input_summary=dict(job.input_summary),
        )

    def _queue_position_locked(self, job_id: str) -> int | None:
        with self._queue.mutex:
            queued_ids = list(self._queue.queue)
        try:
            return queued_ids.index(job_id) + 1
        except ValueError:
            return None
