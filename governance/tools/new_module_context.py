#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

GOV_ROOT = Path("governance")


def slug_from_code_path(code_path: str) -> str:
    value = code_path.strip().strip("/").replace("\\", "/")
    value = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", value).strip("-")
    return value or "module"


def frontmatter(module_id: str, today: str, code_path: str) -> str:
    return (
        "---\n"
        f"id: {module_id}\n"
        "type: module-context\n"
        "status: current\n"
        "owner: engineering\n"
        f"created: {today}\n"
        f"last_reviewed: {today}\n"
        f"code_path: {code_path}\n"
        "---\n\n"
    )


def context_body(name: str, code_path: str, validations: list[str], adrs: list[str]) -> str:
    validation_lines = "\n".join(f"- `{item}`" for item in validations) or "- 待补充。"
    adr_lines = "\n".join(f"- `{item}`" for item in adrs) or "- 待补充。"
    return f"""# {name} Context

## 代码路径

`{code_path}`

## 模块职责

待补充。

## 非职责

待补充。

## 禁止事项

- 待补充。

## 单一真相源

待补充。

## 常用验证

{validation_lines}

## 相关治理文档

{adr_lines}

## Agent Rules

- 不要把本模块上下文散落到代码目录。
- 如需引用原模块 README，只在这里链接，不复制覆盖。
"""


def ensure_context_map(gov_root: Path) -> Path:
    path = gov_root / "context" / "CONTEXT-MAP.md"
    if not path.exists():
        today = date.today().isoformat()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            "id: GOV-CONTEXT-MAP\n"
            "type: index\n"
            "status: current\n"
            "owner: engineering\n"
            f"created: {today}\n"
            f"last_reviewed: {today}\n"
            "---\n\n"
            "# Context Map\n\n"
            "| 领域 | 代码目录 | 上下文文件 | 相关 ADR | 常用验证 |\n"
            "|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    return path


def append_context_map(
    path: Path, name: str, code_path: str, context_rel: str, validations: list[str], adrs: list[str]
) -> None:
    content = path.read_text(encoding="utf-8")
    if code_path in content or context_rel in content:
        return
    validation_text = "<br>".join(f"`{item}`" for item in validations) if validations else "待补充"
    adr_text = "<br>".join(f"`{item}`" for item in adrs) if adrs else "待补充"
    line = f"| {name} | `{code_path}` | `{context_rel}` | {adr_text} | {validation_text} |\n"
    path.write_text(content.rstrip() + "\n" + line, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a governance-owned module context.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--code-path", required=True, help="Code module path, e.g. src/domains/payment.")
    parser.add_argument("--name", help="Human-readable module/domain name.")
    parser.add_argument("--validation", action="append", default=[], help="Validation command. Repeatable.")
    parser.add_argument("--adr", action="append", default=[], help="Related ADR path. Repeatable.")
    parser.add_argument("--dry-run", action="store_true", help="Preview target without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    gov_root = project_root / GOV_ROOT
    if not gov_root.exists():
        raise SystemExit(f"Governance package not found: {gov_root}. Run init_governance_package.py first.")
    slug = slug_from_code_path(args.code_path)
    name = args.name or slug.replace("-", " ")
    rel = Path("context") / "module-contexts" / slug / "CONTEXT.md"
    path = gov_root / rel
    if path.exists():
        raise SystemExit(f"Module context already exists: {path}")
    if args.dry_run:
        print(path)
        return 0
    today = date.today().isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        frontmatter(f"CTX-{slug.upper()}", today, args.code_path)
        + context_body(name, args.code_path, args.validation, args.adr),
        encoding="utf-8",
    )
    context_map = ensure_context_map(gov_root)
    append_context_map(context_map, name, args.code_path, str(rel), args.validation, args.adr)
    print(path)
    print(f"updated: {context_map}")
    print("non_invasive: wrote only inside governance/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
