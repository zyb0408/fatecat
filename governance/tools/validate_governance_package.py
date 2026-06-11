#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

GOV_ROOT = Path("governance")

REQUIRED = [
    "README.md",
    "INDEX.md",
    "CHANGELOG.md",
    "context/AGENT-ENTRY.md",
    "context/CONTEXT-MAP.md",
    "context/CONTEXT-ROUTER.md",
    "context/PROJECT-TOPOLOGY.md",
    "standards/工程质量标准.md",
    "standards/劣质代码定义.md",
    "standards/非功能性需求标准.md",
    "processes/代理协作协议.md",
    "processes/RPI研究计划实施流程.md",
    "processes/QA计划标准.md",
    "processes/本地工具与验证入口.md",
    "architecture-gates/门禁与护栏.md",
    "architecture-gates/GATE-INDEX.md",
    "architecture-gates/rules/INDEX.md",
    "decisions/adr/INDEX.md",
    "evidence/postmortems/INDEX.md",
    "evidence/lessons/INDEX.md",
    "evidence/qa-plans/INDEX.md",
    "agent-governance/agent-feedback/INDEX.md",
    "templates/ADR.template.md",
    "templates/GATE.template.md",
    "templates/QA.template.md",
    "templates/AGENT-FEEDBACK.template.md",
    "tools/README.md",
    "tasks/README.md",
    "runtime/README.md",
    "archive/README.md",
]

REQUIRED_DIRS = [
    "context/module-contexts",
    "architecture-gates/rules",
    "tasks",
    "runtime/runs",
    "runtime/tmp",
]

EMBEDDED_TOOLS = [
    "tools/init_governance_package.py",
    "tools/new_governance_record.py",
    "tools/new_module_context.py",
    "tools/rebuild_governance_index.py",
    "tools/validate_governance_package.py",
    "tools/governance_health_report.py",
    "tools/governance_context_bundle.py",
]

FRONTMATTER_REQUIRED = {"id", "type", "status", "owner", "last_reviewed"}
DATE_FIELDS = {"created", "last_reviewed"}
VALID_STATUSES = {"draft", "active", "current", "deprecated", "archived", "converted", "rejected"}
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TASKS_DOC_ROOTS = {"tasks"}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    raw = text[4:end].splitlines()
    data: dict[str, str] = {}
    for line in raw:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def check_gate(path: Path, text: str, issues: list[dict[str, str]]) -> None:
    required_sections = ["阻止条件", "原因", "检查方式", "可操作错误提示", "最小修复"]
    for section in required_sections:
        if f"## {section}" not in text:
            issues.append({"severity": "BLOCK", "path": str(path), "message": f"gate missing section: {section}"})
    fm = parse_frontmatter(text) or {}
    for field in ["severity", "detectability", "source"]:
        if field not in fm:
            issues.append({"severity": "WARN", "path": str(path), "message": f"gate missing field: {field}"})


def is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def check_frontmatter_values(path: Path, fm: dict[str, str], issues: list[dict[str, str]]) -> None:
    doc_id = fm.get("id", "")
    if not doc_id:
        issues.append({"severity": "WARN", "path": str(path), "message": "frontmatter id is empty"})
    elif not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", doc_id):
        issues.append(
            {"severity": "WARN", "path": str(path), "message": f"frontmatter id has unstable characters: {doc_id}"}
        )

    status = fm.get("status", "")
    if status and status not in VALID_STATUSES:
        issues.append({"severity": "WARN", "path": str(path), "message": f"unknown status: {status}"})

    for field in DATE_FIELDS:
        value = fm.get(field)
        if value and not is_valid_date(value):
            issues.append({"severity": "WARN", "path": str(path), "message": f"{field} must use YYYY-MM-DD"})

    review_cycle = fm.get("review_cycle")
    if review_cycle and not re.fullmatch(r"P\d+D", review_cycle):
        issues.append(
            {"severity": "WARN", "path": str(path), "message": "review_cycle must use ISO day duration like P90D"}
        )


def target_is_external(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)) or target.startswith("#")


def resolve_markdown_link(project_root: Path, root: Path, current_file: Path, target: str) -> Path | None:
    target = unquote(target.strip())
    if not target or target_is_external(target):
        return None
    target = target.split("#", 1)[0].strip()
    if not target:
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if target.startswith(str(GOV_ROOT) + "/"):
        return (project_root / target).resolve()
    if target.startswith("/"):
        return (project_root / target.lstrip("/")).resolve()
    return (current_file.parent / target).resolve()


def check_markdown_links(project_root: Path, root: Path, rel: Path, text: str, issues: list[dict[str, str]]) -> None:
    current_file = root / rel
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw_target = match.group(1).strip()
        target_path = resolve_markdown_link(project_root, root, current_file, raw_target)
        if target_path is None:
            continue
        try:
            target_path.relative_to(project_root.resolve())
        except ValueError:
            issues.append(
                {"severity": "WARN", "path": str(rel), "message": f"markdown link escapes project root: {raw_target}"}
            )
            continue
        if not target_path.exists():
            issues.append({"severity": "WARN", "path": str(rel), "message": f"broken markdown link: {raw_target}"})


def check_duplicate_ids(ids: dict[str, list[str]], issues: list[dict[str, str]]) -> None:
    for doc_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            issues.append(
                {"severity": "WARN", "path": ", ".join(paths), "message": f"duplicate frontmatter id: {doc_id}"}
            )


def is_task_doc(rel: Path) -> bool:
    return bool(rel.parts) and rel.parts[0] in TASKS_DOC_ROOTS


def validate(project_root: Path, strict: bool) -> dict[str, object]:
    root = project_root / GOV_ROOT
    issues: list[dict[str, str]] = []
    ids: dict[str, list[str]] = {}
    if not root.exists():
        return {
            "decision": "BLOCK",
            "root": str(root),
            "issues": [{"severity": "BLOCK", "path": str(root), "message": "governance package missing"}],
        }

    for rel in REQUIRED:
        path = root / rel
        if not path.exists():
            issues.append({"severity": "BLOCK", "path": str(path), "message": "required file missing"})

    for rel in REQUIRED_DIRS:
        path = root / rel
        if not path.exists():
            issues.append({"severity": "WARN", "path": str(path), "message": "recommended directory missing"})

    if strict:
        for rel in EMBEDDED_TOOLS:
            path = root / rel
            if not path.exists():
                issues.append({"severity": "WARN", "path": str(path), "message": "embedded maintenance tool missing"})

    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        if is_task_doc(rel):
            if strict:
                check_markdown_links(project_root, root, rel, text, issues)
            continue
        fm = parse_frontmatter(text)
        if fm is None:
            severity = "WARN" if "template" in path.name.lower() or path.name == "INDEX.md" else "BLOCK"
            issues.append({"severity": severity, "path": str(rel), "message": "missing frontmatter"})
        elif strict:
            if fm.get("id"):
                ids.setdefault(fm["id"], []).append(str(rel))
            missing = sorted(FRONTMATTER_REQUIRED - set(fm))
            if missing:
                issues.append(
                    {"severity": "WARN", "path": str(rel), "message": f"frontmatter missing: {', '.join(missing)}"}
                )
            check_frontmatter_values(rel, fm, issues)
            check_markdown_links(project_root, root, rel, text, issues)
        if "/architecture-gates/rules/" in f"/{rel.as_posix()}/" and path.name.startswith("GATE-"):
            check_gate(rel, text, issues)

    if strict:
        check_duplicate_ids(ids, issues)

    index = root / "INDEX.md"
    if index.exists():
        content = index.read_text(encoding="utf-8")
        for rel in ["context/AGENT-ENTRY.md", "architecture-gates/GATE-INDEX.md", "standards/工程质量标准.md"]:
            if rel not in content:
                issues.append({"severity": "WARN", "path": "INDEX.md", "message": f"index does not mention {rel}"})

    gate_index = root / "architecture-gates" / "GATE-INDEX.md"
    if gate_index.exists() and "Gate ID" not in gate_index.read_text(encoding="utf-8"):
        issues.append(
            {
                "severity": "WARN",
                "path": str(gate_index.relative_to(root)),
                "message": "GATE-INDEX missing table header",
            }
        )

    decision = "PASS"
    if any(issue["severity"] == "BLOCK" for issue in issues):
        decision = "BLOCK"
    elif issues:
        decision = "WARN"
    return {"decision": decision, "root": str(root), "issue_count": len(issues), "issues": issues}


def render_markdown(result: dict[str, object]) -> str:
    lines = [
        "# Governance Package Validation",
        "",
        f"- `decision`: {result['decision']}",
        f"- `root`: {result['root']}",
        f"- `issue_count`: {result.get('issue_count', len(result['issues']))}",
        "",
        "## Issues",
    ]
    issues = result["issues"]
    if not issues:
        lines.append("- none")
    else:
        for issue in issues:
            lines.append(f"- `{issue['severity']}` `{issue['path']}`: {issue['message']}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an governance package.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--strict", action="store_true", help="Enable stricter frontmatter checks.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate(Path(args.project_root).resolve(), args.strict)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))
    return 1 if result["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
