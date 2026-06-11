#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path

GOV_ROOT = Path("governance")
TOOL_NAMES = [
    "init_governance_package.py",
    "new_governance_record.py",
    "validate_governance_package.py",
    "rebuild_governance_index.py",
    "new_module_context.py",
    "governance_health_report.py",
    "governance_context_bundle.py",
]


def fm(doc_id: str, doc_type: str, status: str = "current") -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        f"id: {doc_id}\n"
        f"type: {doc_type}\n"
        f"status: {status}\n"
        "owner: engineering\n"
        f"created: {today}\n"
        f"last_reviewed: {today}\n"
        "review_cycle: P90D\n"
        "---\n\n"
    )


def doc(doc_id: str, doc_type: str, title: str, body: str, status: str = "current") -> str:
    return fm(doc_id, doc_type, status) + f"# {title}\n\n{body.strip()}\n"


def index_doc(title: str, rows: list[tuple[str, str]]) -> str:
    safe_id = "IDX-" + re.sub(r"[^A-Z0-9]+", "-", title.upper()).strip("-")
    lines = [
        f"# {title}",
        "",
        "| 名称 | 说明 |",
        "|---|---|",
    ]
    for name, desc in rows:
        lines.append(f"| `{name}` | {desc} |")
    return fm(safe_id, "index") + "\n".join(lines) + "\n"


def minimal_files() -> dict[str, str]:
    return {
        "README.md": doc(
            "GOV-README",
            "index",
            "工程治理包",
            """
本目录是项目级工程治理包，固定落点为 `governance/`。

它只新增独立治理资产，不改写、不覆盖、不迁移项目原有 `README.md`、`AGENTS.md`、`CLAUDE.md`、模块文档、CI 配置或脚本。

使用入口：

1. 先读 `INDEX.md`。
2. 再读 `context/AGENT-ENTRY.md`。
3. 按 `context/CONTEXT-ROUTER.md` 选择最小上下文。
4. 需要模块事实时，通过 `context/CONTEXT-MAP.md` 找到对应 module context。
            """,
        ),
        "INDEX.md": doc(
            "GOV-INDEX",
            "index",
            "治理包索引",
            """
## 启动入口

- `context/AGENT-ENTRY.md`：代理启动协议。
- `context/CONTEXT-MAP.md`：项目上下文地图。
- `context/CONTEXT-ROUTER.md`：任务类型到上下文包的路由。
- `context/PROJECT-TOPOLOGY.md`：项目结构和边界说明。

## 当前标准

- `standards/工程质量标准.md`
- `standards/劣质代码定义.md`
- `standards/非功能性需求标准.md`

## 流程

- `processes/代理协作协议.md`
- `processes/RPI研究计划实施流程.md`
- `processes/QA计划标准.md`
- `processes/本地工具与验证入口.md`

## 门禁

- `architecture-gates/门禁与护栏.md`
- `architecture-gates/GATE-INDEX.md`
            """,
        ),
        "CHANGELOG.md": doc(
            "GOV-CHANGELOG",
            "changelog",
            "治理包变更记录",
            "- 初始化治理包。\n",
        ),
        "context/AGENT-ENTRY.md": doc(
            "GOV-AGENT-ENTRY",
            "process",
            "Agent Entry",
            """
## 项目工作协议

1. 不要在没有验证证据的情况下声明“已完成”或“已测试”。
2. 开始任务前先读取 `governance/INDEX.md`。
3. 根据 `governance/context/CONTEXT-ROUTER.md` 选择最小上下文。
4. 涉及架构边界时必须读取相关 ADR。
5. 涉及用户功能时必须产出 QA 计划或验证证据。
6. 高风险变更必须说明回滚路径。
7. 如果发现重复错误或标准缺失，记录到 `agent-governance/agent-feedback/`。
            """,
        ),
        "context/CONTEXT-MAP.md": doc(
            "GOV-CONTEXT-MAP",
            "index",
            "Context Map",
            """
## 领域上下文

| 领域 | 代码目录 | 上下文文件 | 相关 ADR | 常用验证 |
|---|---|---|---|---|
| 项目根 | `.` | `context/PROJECT-TOPOLOGY.md` | `decisions/adr/INDEX.md` | governance strict validate |
| 治理包 | `governance/` | `context/AGENT-ENTRY.md` | `decisions/adr/INDEX.md` | governance health report |
| 任务容器 | `governance/tasks/` | `tasks/INDEX.md` | `decisions/adr/INDEX.md` | task tree validation |

## 维护规则

- 不把模块上下文散落到代码目录。
- 模块上下文统一放在 `context/module-contexts/`。
- 原有模块 README 只被引用，不被治理包覆盖。
- 新增稳定模块后，再创建 `context/module-contexts/<module>/CONTEXT.md` 并更新本表。
            """,
        ),
        "context/CONTEXT-ROUTER.md": doc(
            "GOV-CONTEXT-ROUTER",
            "process",
            "Context Router",
            """
## 默认入口

所有任务先读：

1. `governance/INDEX.md`
2. `governance/context/PROJECT-TOPOLOGY.md`
3. `governance/context/CONTEXT-MAP.md`

## 任务类型路由

| 任务类型 | 必读文档 | 可选文档 | 必须产出 |
|---|---|---|---|
| 新功能 | 工程质量标准、非功能性需求标准、QA计划标准、代理协作协议 | 相关 ADR、术语表 | QA 计划或验证证据 |
| Bug 修复 | 劣质代码定义、本地工具与验证入口 | postmortems、lessons | 复现步骤、回归测试 |
| 性能优化 | 性能效率优化标准、门禁与护栏 | 历史性能复盘 | benchmark/profile 证据 |
| 架构变更 | 架构设计原则、ADR 索引、非功能性需求标准 | tech-debt | ADR 或 ADR 更新 |
| Review | 代码评审标准、门禁与护栏 | lessons、agent-feedback | PASS/WARN/BLOCK finding |
| 复盘 | 文档治理规则、门禁与护栏 | postmortems/INDEX.md | 防复发动作 |
            """,
        ),
        "context/PROJECT-TOPOLOGY.md": doc(
            "GOV-PROJECT-TOPOLOGY",
            "index",
            "Project Topology",
            """
## 项目结构

| 路径 | 职责 | 禁止事项 | 主要验证 |
|---|---|---|---|
| `governance/` | 项目工程治理包、上下文路由、标准、门禁和证据记录 | 不覆盖项目原有 README、AGENTS、CI 或模块文档 | `validate_governance_package.py --strict` |
| `governance/tasks/` | 任务树、任务包和执行状态 | 不把任务临时状态直接当成长期标准 | `validate_tasks_tree.py` |
| 源代码目录 | 项目业务实现与测试 | 不绕过既有模块边界和公共接口 | 使用项目实际 test/lint/typecheck 命令 |

## 依赖方向

治理包只提供项目记忆和执行护栏；源代码目录保持业务实现职责；任务容器记录执行过程，长期有效经验再晋升到 standards、processes、architecture-gates 或 evidence。
            """,
        ),
        "standards/工程质量标准.md": doc(
            "STD-ENGINEERING-QUALITY",
            "standard",
            "工程质量标准",
            """
## 基本要求

- 正确性优先。
- 行为可验证。
- 边界清晰。
- 依赖合理。
- 错误处理完整。
- 性能和成本可解释。

## 不合格信号

- 没有验证证据。
- 改动范围失控。
- 重复实现既有能力。
- 引入无法解释的复杂度。
            """,
        ),
        "standards/劣质代码定义.md": doc(
            "STD-CODE-BAD",
            "standard",
            "劣质代码定义",
            """
不可接受模式：

- 临时补丁替代根因修复。
- 吞异常或假成功。
- 无测试的高风险改动。
- N+1、无界循环、无界并发、全量加载大数据。
- 无 timeout、无限重试、无背压。
- 硬编码业务规则。
- 绕过架构边界。
- 双真相源。
            """,
        ),
        "standards/非功能性需求标准.md": doc(
            "STD-NFR",
            "standard",
            "非功能性需求标准",
            """
默认检查：

- 性能
- 可靠性
- 安全
- 可观测性
- 可扩展性
- 兼容性
- 成本
- 可维护性
- 可测试性
            """,
        ),
        "processes/代理协作协议.md": doc(
            "PROC-AGENT-COLLAB",
            "process",
            "代理协作协议",
            """
代理执行任务时必须：

1. 读取治理包入口。
2. 按上下文路由加载最小文档。
3. 保留关键证据。
4. 不伪造验证结果。
5. 发现重复错误时写入 agent feedback。
6. 高风险变更说明回滚路径。
            """,
        ),
        "processes/RPI研究计划实施流程.md": doc(
            "PROC-RPI",
            "process",
            "RPI 研究-计划-实施流程",
            """
## Research

- 相关文件
- 当前事实
- 数据流/调用流
- 风险点
- 未确认问题

## Plan

- 修改文件列表
- 每个文件修改意图
- 测试策略
- 回滚策略
- 需要更新的治理资产

## Implement

- 严格执行计划。
- 不扩大范围。
- 偏离计划必须记录原因。
- 完成后输出验证证据。
            """,
        ),
        "processes/QA计划标准.md": doc(
            "PROC-QA-STANDARD",
            "process",
            "QA 计划标准",
            """
关键用户功能应包含：

- 功能清单
- 关键用户旅程
- 成功路径
- 失败路径
- 边界输入
- 验收证据
- PR 应附材料
            """,
        ),
        "processes/本地工具与验证入口.md": doc(
            "PROC-LOCAL-VERIFY",
            "process",
            "本地工具与验证入口",
            """
## 治理包校验

```bash
python3 skills/auto-governance/scripts/validate_governance_package.py --project-root . --strict
python3 skills/auto-governance/scripts/governance_health_report.py --project-root . --strict
```

## 任务树校验

```bash
python3 skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown
```

## 项目自身验证

使用项目已有的 package manager、test、lint、typecheck、benchmark 或 CI 命令；治理包不发明项目不存在的验证入口。
            """,
        ),
        "architecture-gates/门禁与护栏.md": doc(
            "GATE-GUARDRAILS",
            "gate-index",
            "门禁与护栏",
            """
初版门禁：

- 不接受无验证证据的高风险代码。
- 不接受明显性能放大问题。
- 不接受吞异常、假成功、无 timeout、无限重试。
- 不接受绕过架构边界、双真相源、重复实现已有工具。
- 不接受未说明回滚方式的高风险迁移。
- 不接受复发的历史错误未更新护栏。
            """,
        ),
        "architecture-gates/GATE-INDEX.md": doc(
            "GATE-INDEX",
            "gate-index",
            "Gate Index",
            """
| Gate ID | 严重级别 | 类型 | 检测方式 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| 无 active gate | - | - | - | 当前最小治理包尚未沉淀阻塞门禁 | current |
            """,
        ),
        "architecture-gates/rules/INDEX.md": index_doc("GATE Index", []),
        "decisions/adr/INDEX.md": index_doc("ADR Index", []),
        "evidence/postmortems/INDEX.md": index_doc("Postmortem Index", []),
        "evidence/lessons/INDEX.md": index_doc("Lesson Index", []),
        "evidence/qa-plans/INDEX.md": index_doc("QA Plan Index", []),
        "agent-governance/agent-feedback/INDEX.md": index_doc("Agent Feedback Index", []),
        "templates/ADR.template.md": template("ADR"),
        "templates/GATE.template.md": template("GATE"),
        "templates/QA.template.md": template("QA"),
        "templates/AGENT-FEEDBACK.template.md": template("AF"),
        "tools/README.md": doc(
            "TOOLS-GOVERNANCE",
            "tooling",
            "Governance Tools",
            """
这里放治理包自身维护脚本或接入说明。默认不修改项目外部 CI、lint 或 hook。

默认内置工具：

- `init_governance_package.py`：初始化或补齐治理包。
- `new_governance_record.py`：新增 ADR/Gate/QA/Postmortem/Lesson/Agent Feedback 等编号记录。
- `new_module_context.py`：新增治理包内模块上下文，并更新 `CONTEXT-MAP.md`。
- `rebuild_governance_index.py`：重建根索引、记录索引、`architecture-gates/rules/INDEX.md` 和 `GATE-INDEX.md`。
- `validate_governance_package.py`：校验治理包结构、frontmatter 和 gate 必填项。
- `governance_health_report.py`：输出治理包健康度、占位内容、过期文档、open feedback 和下一步动作。
- `governance_context_bundle.py`：按任务类型输出 agent 本次应读取的治理文档、模块上下文和必须产出。

这些脚本只写入 `governance/` 内部；外部 CI、lint、hook 接入必须单独 opt-in。
            """,
        ),
        "tasks/README.md": doc(
            "TASKS-GOVERNANCE",
            "tasks",
            "Governance Tasks",
            "这里放项目任务包、任务树、执行波次、closeout 和任务级候选 lessons。长期有效规则应拆分后晋升到 `evidence/`、`architecture-gates/`、`processes/` 或 `standards/`。",
        ),
        "runtime/README.md": doc(
            "RUNTIME-GOVERNANCE",
            "runtime",
            "Runtime Records",
            "这里放代理运行记录和临时材料。任务包统一放在 `governance/tasks/`，长期价值内容应沉淀到 `evidence/`。",
        ),
        "archive/README.md": doc(
            "ARCHIVE-GOVERNANCE",
            "archive",
            "Archive",
            "这里归档失效、被替代或过期的治理资产。",
        ),
    }


def full_extra_files() -> dict[str, str]:
    return {
        "standards/优质代码定义.md": doc(
            "STD-CODE-GOOD",
            "standard",
            "优质代码定义",
            "优质代码必须正确、清晰、边界明确、可测试、可维护、性能可解释，并优先复用成熟能力。",
        ),
        "standards/性能效率优化标准.md": doc(
            "STD-PERFORMANCE",
            "standard",
            "性能效率优化标准",
            "默认检查复杂度、hot path、数据库/API/I/O、缓存、内存、并发、成本、benchmark/profile 和 p95/p99。",
        ),
        "standards/可靠性标准.md": doc(
            "STD-RELIABILITY",
            "standard",
            "可靠性标准",
            "默认检查 timeout、retry budget、熔断、降级、幂等、背压、资源池、队列容量、恢复路径和可观测性。",
        ),
        "standards/架构设计原则.md": doc(
            "STD-ARCHITECTURE",
            "standard",
            "架构设计原则",
            "默认检查模块边界、依赖方向、单一真相源、信息隐藏、深模块、禁止旁路和数据所有权。",
        ),
        "standards/术语表.md": doc(
            "STD-GLOSSARY",
            "standard",
            "术语表",
            "记录项目领域词、模块名、缩写、状态名和关键概念。",
        ),
        "processes/代码评审标准.md": doc(
            "PROC-REVIEW",
            "process",
            "代码评审标准",
            "评审输出必须包含 PASS/WARN/BLOCK、证据、影响、最小修复和验证方式。",
        ),
        "processes/文档治理规则.md": doc(
            "PROC-DOC-GOVERNANCE",
            "process",
            "文档治理规则",
            "定义文档何时更新、如何归档、如何复核、如何从复盘生成护栏。",
        ),
        "evidence/reviews/INDEX.md": index_doc("Review Index", []),
        "evidence/workorders/INDEX.md": index_doc("Workorder Index", []),
        "evidence/tech-debt/INDEX.md": index_doc("Tech Debt Index", []),
        "evidence/baselines/INDEX.md": index_doc("Baseline Evidence Index", []),
        "evidence/releases/INDEX.md": index_doc("Release Evidence Index", []),
        "evidence/verification/INDEX.md": index_doc("Verification Evidence Index", []),
        "evidence/compatibility/INDEX.md": index_doc("Compatibility Evidence Index", []),
        "evidence/adoption/INDEX.md": index_doc("Adoption Evidence Index", []),
        "evidence/support/INDEX.md": index_doc("Support Evidence Index", []),
        "evidence/release-trains/INDEX.md": index_doc("Release Train Evidence Index", []),
        "evidence/communications/INDEX.md": index_doc("Communication Evidence Index", []),
        "evidence/rollback/INDEX.md": index_doc("Rollback Evidence Index", []),
        "evidence/conformance/INDEX.md": index_doc("Conformance Evidence Index", []),
        "evidence/exceptions/INDEX.md": index_doc("Exception Evidence Index", []),
        "evidence/audit-exports/INDEX.md": index_doc("Audit Export Index", []),
        "control-plane/README.md": doc(
            "GOV-CONTROL-PLANE",
            "control-plane",
            "Control Plane",
            "这里放控制项覆盖、发布准入、版本治理、标准基线、例外放行和机器可读控制面资产。",
        ),
        "control-plane/controls/INDEX.md": index_doc("Control Index", []),
        "ownership/README.md": doc(
            "GOV-OWNERSHIP",
            "ownership",
            "Ownership",
            "这里放 owner、RACI、on-call、升级路径和责任边界。",
        ),
        "risk-register/INDEX.md": index_doc("Risk Register Index", []),
        "slo/README.md": doc(
            "GOV-SLO",
            "slo",
            "SLO",
            "这里放可靠性分级、SLO、错误预算、演练和升级策略。",
        ),
        "migration/README.md": doc(
            "GOV-MIGRATION",
            "migration",
            "Migration",
            "这里放弃用策略、迁移窗口、兼容策略和退役计划。",
        ),
        "ai-governance/README.md": doc(
            "GOV-AI",
            "ai-governance",
            "AI Governance",
            "这里放 AI 产品、模型风险、prompt、微调、Agent 工具、AI 证据账本和 AI 事件响应治理。",
        ),
        "data-governance/README.md": doc(
            "GOV-DATA",
            "data-governance",
            "Data Governance",
            "这里放数据产品评审、PII、权限、保留期限、血缘和数据质量治理。",
        ),
        "agent-governance/review-agents/INDEX.md": index_doc("Review Agents Index", []),
        "agent-governance/prompts/INDEX.md": index_doc("Prompts Index", []),
        "agent-governance/skills/INDEX.md": index_doc("Embedded Skills Index", []),
        "templates/REVIEW.template.md": template("REVIEW"),
        "templates/POSTMORTEM.template.md": template("POSTMORTEM"),
        "templates/LESSON.template.md": template("LESSON"),
        "templates/WORKORDER.template.md": template("WO"),
        "templates/DEBT.template.md": template("DEBT"),
        "templates/BASELINE.template.md": template("BASELINE"),
        "templates/CONTROL.template.md": template("CONTROL"),
        "templates/EXCEPTION.template.md": template("EXCEPTION"),
        "templates/RISK.template.md": template("RISK"),
        "templates/CONFORMANCE.template.md": template("CONFORMANCE"),
        "templates/AUDIT-EXPORT.template.md": template("AUDIT"),
    }


def template(prefix: str) -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        f"id: {prefix}-0000\n"
        "type: template\n"
        "status: current\n"
        "owner: engineering\n"
        f"created: {today}\n"
        f"last_reviewed: {today}\n"
        "---\n\n"
        f"# {prefix}-0000 标题\n\n"
        "## 背景\n\n待补充。\n\n"
        "## 结论\n\n待补充。\n\n"
        "## 证据\n\n待补充。\n\n"
        "## 后续动作\n\n- [ ] 待补充。\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a governance package.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--mode", choices=("minimal", "full"), default="minimal", help="Scaffold mode.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing governance files.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument(
        "--no-embed-tools",
        action="store_true",
        help="Do not copy governance maintenance scripts into governance/tools/.",
    )
    return parser.parse_args()


def embed_tools(root: Path, force: bool, dry_run: bool) -> tuple[list[str], list[str], list[str]]:
    source_dir = Path(__file__).resolve().parent
    created: list[str] = []
    skipped: list[str] = []
    overwritten: list[str] = []
    for name in TOOL_NAMES:
        src = source_dir / name
        if not src.exists():
            skipped.append(str(GOV_ROOT / "tools" / name) + " (source missing)")
            continue
        dst = root / "tools" / name
        display = str(GOV_ROOT / "tools" / name)
        if dst.exists() and not force:
            skipped.append(display)
            continue
        if dry_run:
            created.append(display if not dst.exists() else f"{display} (overwrite)")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        existed = dst.exists()
        if src.resolve() != dst.resolve():
            shutil.copy2(src, dst)
        if existed:
            overwritten.append(display)
        else:
            created.append(display)
    return created, skipped, overwritten


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    root = project_root / GOV_ROOT
    files = minimal_files()
    if args.mode == "full":
        files.update(full_extra_files())

    created: list[str] = []
    skipped: list[str] = []
    overwritten: list[str] = []

    for rel, content in files.items():
        path = root / rel
        display = str(GOV_ROOT / rel)
        if path.exists() and not args.force:
            skipped.append(display)
            continue
        if args.dry_run:
            created.append(display if not path.exists() else f"{display} (overwrite)")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        existed = path.exists()
        path.write_text(content, encoding="utf-8")
        if existed:
            overwritten.append(display)
        else:
            created.append(display)

    if not args.no_embed_tools:
        tool_created, tool_skipped, tool_overwritten = embed_tools(root, args.force, args.dry_run)
        created.extend(tool_created)
        skipped.extend(tool_skipped)
        overwritten.extend(tool_overwritten)

    if not args.dry_run:
        for dirname in [
            "context/module-contexts",
            "architecture-gates/rules",
            "tasks",
            "runtime/runs",
            "runtime/tmp",
        ]:
            (root / dirname).mkdir(parents=True, exist_ok=True)

    print(f"project_root: {project_root}")
    print(f"governance_root: {root}")
    print(f"mode: {args.mode}")
    print(f"embedded_tools: {not args.no_embed_tools}")
    print(f"created: {len(created)}")
    for item in created:
        print(f"  + {item}")
    if overwritten:
        print(f"overwritten: {len(overwritten)}")
        for item in overwritten:
            print(f"  ! {item}")
    if skipped:
        print(f"skipped_existing: {len(skipped)}")
        for item in skipped:
            print(f"  = {item}")
    print("non_invasive: did not modify files outside governance/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
