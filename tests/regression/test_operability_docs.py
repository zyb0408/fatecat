from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_public_service_operability_runbook_is_referenced_and_actionable():
    review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
    ops_pack = (ROOT / "references" / "ops-pack.md").read_text(encoding="utf-8")
    commands = (ROOT / "references" / "commands.md").read_text(encoding="utf-8")

    assert "references/ops-pack.md" in review
    assert "公共服务 SLO" in ops_pack
    assert "Prometheus / Grafana" in ops_pack
    assert "fatecat_request_latency_seconds_bucket" in ops_pack
    assert "fatecat_request_errors_total" in ops_pack
    assert "fatecat_calculation_slots_in_use" in ops_pack
    assert "fatecat_bot_queue_size" in ops_pack
    assert "fatecat_bot_queue_scope_info" in ops_pack
    assert "single_process" in ops_pack
    assert "X-Request-ID" in ops_pack
    assert "bash scripts/local-ci.sh --profile all" in ops_pack
    assert "bash scripts/container-release.sh" in ops_pack
    assert "bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot" in ops_pack
    assert "bash scripts/clean-runtime.sh" in ops_pack
    assert "fatecat_bot_queue_size" in commands
    assert "FATE_MAX_INFLIGHT_CALCULATIONS=2" in commands
    assert "FATE_RATE_LIMIT_BACKEND=memory" in commands
