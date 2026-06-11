#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

GOV_ROOT = Path("governance")

KINDS = {
    "adr": ("ADR", Path("decisions/adr"), "record"),
    "review": ("REVIEW", Path("evidence/reviews"), "record"),
    "postmortem": ("POSTMORTEM", Path("evidence/postmortems"), "record"),
    "lesson": ("LESSON", Path("evidence/lessons"), "record"),
    "workorder": ("WO", Path("evidence/workorders"), "record"),
    "debt": ("DEBT", Path("evidence/tech-debt"), "record"),
    "gate": ("GATE", Path("architecture-gates/rules"), "gate"),
    "qa": ("QA", Path("evidence/qa-plans"), "record"),
    "agent-feedback": ("AF", Path("agent-governance/agent-feedback"), "record"),
    "baseline": ("BASELINE", Path("evidence/baselines"), "record"),
    "control": ("CONTROL", Path("control-plane/controls"), "record"),
    "exception": ("EXCEPTION", Path("evidence/exceptions"), "record"),
    "risk": ("RISK", Path("risk-register"), "record"),
    "conformance": ("CONFORMANCE", Path("evidence/conformance"), "record"),
    "audit-export": ("AUDIT", Path("evidence/audit-exports"), "record"),
    "release": ("RELEASE", Path("evidence/releases"), "record"),
}


def slugify(title: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", "", title.strip())
    value = re.sub(r"\s+", "-", value)
    return value[:80] or "记录"


def next_id(directory: Path, prefix: str) -> str:
    highest = 0
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d{{4}})")
    if directory.exists():
        for path in directory.glob(f"{prefix}-*.md"):
            match = pattern.match(path.name)
            if match:
                highest = max(highest, int(match.group(1)))
    return f"{prefix}-{highest + 1:04d}"


def frontmatter(record_id: str, record_type: str, status: str, today: str) -> str:
    fields = {
        "id": record_id,
        "type": record_type,
        "status": status,
        "owner": "engineering",
        "created": today,
        "last_reviewed": today,
        "source": "",
    }
    if record_type == "gate":
        fields["severity"] = "BLOCK"
        fields["detectability"] = "manual"
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {value}")
    lines.append("related_gates: []")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def body(kind: str, record_id: str, title: str) -> str:
    heading = f"# {record_id} {title}\n\n"
    if kind == "gate":
        return heading + (
            "## 阻止条件\n\n待补充。\n\n"
            "## 原因\n\n待补充。\n\n"
            "## 检查方式\n\n- manual: 待补充。\n\n"
            "## 可操作错误提示\n\n待补充。\n\n"
            "## 最小修复\n\n- [ ] 待补充。\n"
        )
    if kind == "postmortem":
        return heading + (
            "## 事件背景\n\n待补充。\n\n"
            "## 影响范围\n\n待补充。\n\n"
            "## 根因\n\n待补充。\n\n"
            "## 修复过程\n\n待补充。\n\n"
            "## 防复发动作\n\n- [ ] 待补充。\n\n"
            "## 是否需要新增 Gate\n\n待判定。\n"
        )
    if kind == "qa":
        return heading + (
            "## 功能范围\n\n待补充。\n\n"
            "## 用户旅程\n\n待补充。\n\n"
            "## 验收场景\n\n- [ ] 成功路径。\n- [ ] 失败路径。\n- [ ] 边界输入。\n\n"
            "## 验证证据\n\n待补充。\n"
        )
    if kind == "agent-feedback":
        return heading + (
            "## 反馈来源\n\n待补充。\n\n"
            "## 代理失败模式\n\n待补充。\n\n"
            "## 期望行为\n\n待补充。\n\n"
            "## 处理状态\n\nnew\n\n"
            "## 转化结果\n\n- [ ] lesson\n- [ ] gate\n- [ ] rejected\n"
        )
    return heading + (
        "## 背景\n\n待补充。\n\n"
        "## 决策或结论\n\n待补充。\n\n"
        "## 证据\n\n待补充。\n\n"
        "## 影响范围\n\n待补充。\n\n"
        "## 后续动作\n\n- [ ] 待补充。\n"
    )


def ensure_index(directory: Path, title: str) -> Path:
    index = directory / "INDEX.md"
    if not index.exists():
        today = date.today().isoformat()
        index.write_text(
            "---\n"
            f"id: IDX-{slugify(title).upper()}\n"
            "type: index\n"
            "status: current\n"
            "owner: engineering\n"
            f"created: {today}\n"
            f"last_reviewed: {today}\n"
            "---\n\n"
            f"# {title}\n\n| ID | 标题 | 状态 |\n|---|---|---|\n",
            encoding="utf-8",
        )
    return index


def append_index(index: Path, record_id: str, title: str) -> None:
    content = index.read_text(encoding="utf-8")
    line = f"| `{record_id}` | {title} | draft |\n"
    if record_id not in content:
        index.write_text(content.rstrip() + "\n" + line, encoding="utf-8")


def append_gate_index(gov_root: Path, record_id: str, title: str) -> None:
    index = gov_root / "architecture-gates" / "GATE-INDEX.md"
    index.parent.mkdir(parents=True, exist_ok=True)
    if not index.exists():
        today = date.today().isoformat()
        index.write_text(
            "---\n"
            "id: GATE-INDEX\n"
            "type: gate-index\n"
            "status: current\n"
            "owner: engineering\n"
            f"created: {today}\n"
            f"last_reviewed: {today}\n"
            "---\n\n"
            "# Gate Index\n\n"
            "| Gate ID | 严重级别 | 类型 | 检测方式 | 来源 | 当前状态 |\n"
            "|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    content = index.read_text(encoding="utf-8")
    line = f"| `{record_id}` | BLOCK | 待补充 | manual | {title} | draft |\n"
    if record_id not in content:
        index.write_text(content.rstrip() + "\n" + line, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a numbered governance record.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--kind", choices=sorted(KINDS), required=True, help="Record kind.")
    parser.add_argument("--title", required=True, help="Record title.")
    parser.add_argument("--id", help="Explicit record id, e.g. ADR-0007.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    gov_root = project_root / GOV_ROOT
    if not gov_root.exists():
        raise SystemExit(f"Governance package not found: {gov_root}. Run init_governance_package.py first.")

    prefix, rel_dir, record_type = KINDS[args.kind]
    directory = gov_root / rel_dir
    directory.mkdir(parents=True, exist_ok=True)
    record_id = args.id or next_id(directory, prefix)
    filename = f"{record_id}-{slugify(args.title)}.md"
    path = directory / filename
    if path.exists():
        raise SystemExit(f"Record already exists: {path}")

    today = date.today().isoformat()
    content = frontmatter(record_id, record_type, "draft" if record_type != "gate" else "active", today)
    content += body(args.kind, record_id, args.title)

    if args.dry_run:
        print(path)
        return 0

    path.write_text(content, encoding="utf-8")
    index = ensure_index(directory, f"{args.kind} Index")
    append_index(index, record_id, args.title)
    if args.kind == "gate":
        append_gate_index(gov_root, record_id, args.title)

    print(path)
    print(f"updated: {index}")
    if args.kind == "gate":
        print(f"updated: {gov_root / 'architecture-gates' / 'GATE-INDEX.md'}")
    print("non_invasive: wrote only inside governance/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
