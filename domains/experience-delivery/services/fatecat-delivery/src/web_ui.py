"""原生 HTML Web 报告页。

该模块只负责 FastAPI 交付层的 HTML 呈现，不定义新的命理字段契约。
页面遵循零美化语义界面规范：服务端直出、原生表单、psql ASCII 表格、Markdown 原文可复制。
Web 生产空间复用 pdf 工作台的黄金三块全屏布局契约；CSS 只服务该操作结构。
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from html import escape
from typing import Any

from fastapi.responses import HTMLResponse
from tabulate import tabulate

from branding import get_branding_payload
from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from location import get as get_location
from prediction_systems import PREDICTION_SYSTEMS, report_system_allowed_text
from report_generator import REPORT_SYSTEM_LABELS, build_report_hide, generate_full_report, public_birth_place
from utils.timezone import now_cn

logger = logging.getLogger(__name__)


@dataclass
class WebReportForm:
    birth_date: str = ""
    birth_time: str = ""
    birth_place: str = ""
    gender: str = ""
    name: str = ""
    report_system: str = "bazi"
    submitted: bool = False

    @classmethod
    def from_query(
        cls,
        *,
        birth_date: str | None = None,
        birth_time: str | None = None,
        birth_place: str | None = None,
        gender: str | None = None,
        name: str | None = None,
        report_system: str | None = None,
        submitted: str | None = None,
    ) -> WebReportForm:
        return cls(
            birth_date=(birth_date or "").strip(),
            birth_time=(birth_time or "").strip(),
            birth_place=(birth_place or "").strip(),
            gender=(gender or "").strip(),
            name=(name or "").strip(),
            report_system=(report_system or "bazi").strip() or "bazi",
            submitted=(submitted or "").strip() == "1",
        )

    def has_input(self) -> bool:
        return any([self.birth_date, self.birth_time, self.birth_place, self.gender, self.name])


@dataclass
class WebReportResult:
    markdown: str
    resolved_longitude: float
    resolved_latitude: float
    normalized_time: str
    input_payload: dict[str, Any]
    report_system: str
    report_system_label: str
    workbench: dict[str, Any]


def render_web_report_page(
    *,
    birth_date: str | None = None,
    birth_time: str | None = None,
    birth_place: str | None = None,
    gender: str | None = None,
    name: str | None = None,
    report_system: str | None = None,
    submitted: str | None = None,
) -> HTMLResponse:
    """渲染 Web 版标准 Markdown 报告页面。"""
    form = WebReportForm.from_query(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_place=birth_place,
        gender=gender,
        name=name,
        report_system=report_system,
        submitted=submitted,
    )

    errors: list[str] = []
    result: WebReportResult | None = None
    if form.submitted or form.has_input():
        try:
            result = _build_report(form)
        except ValueError as exc:
            errors.append(str(exc))
        except Exception:
            logger.exception("Web 报告生成失败")
            errors.append("生成报告失败")

    html = _render_document(form=form, result=result, errors=errors)
    return HTMLResponse(content=html)


def _build_report(form: WebReportForm) -> WebReportResult:
    missing = []
    if not form.birth_date:
        missing.append("出生日期")
    if not form.birth_time:
        missing.append("出生时间")
    if not form.birth_place:
        missing.append("出生地区")
    if not form.gender:
        missing.append("性别")
    if missing:
        raise ValueError(f"缺少必填字段: {'、'.join(missing)}")

    birth_dt, normalized_time = _parse_birth_datetime(form.birth_date, form.birth_time)
    gender = _normalize_gender(form.gender)
    report_system = _normalize_report_system(form.report_system)
    try:
        longitude, latitude = get_location(form.birth_place)
    except ValueError as exc:
        if str(exc).startswith("地点无法识别"):
            raise ValueError("地点无法识别") from exc
        raise
    display_birth_place = public_birth_place(form.birth_place)

    report_hide = build_report_hide(report_system)
    capability_id = report_system
    calc_result = (
        CapabilityExecutor()
        .execute(
            CapabilityInput(
                capability_id=capability_id,
                payload={
                    "birthDateTime": birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "gender": gender,
                    "longitude": longitude,
                    "latitude": latitude,
                    "birthPlace": display_birth_place if capability_id == "bazi" else form.birth_place,
                    "name": form.name,
                    "useTrueSolarTime": True,
                },
            )
        )
        .data
    )
    markdown = generate_full_report(calc_result, hide=report_hide, report_system=report_system)
    payload = {
        "birthDate": form.birth_date,
        "birthTime": normalized_time,
        "birthPlace": display_birth_place,
        "gender": gender,
        "name": form.name,
        "reportSystem": report_system,
        "reportSystemLabel": REPORT_SYSTEM_LABELS[report_system],
        "longitude": longitude,
        "latitude": latitude,
        "useTrueSolarTime": True,
    }
    return WebReportResult(
        markdown=markdown,
        resolved_longitude=longitude,
        resolved_latitude=latitude,
        normalized_time=normalized_time,
        input_payload=payload,
        report_system=report_system,
        report_system_label=REPORT_SYSTEM_LABELS[report_system],
        workbench=_build_workbench_payload(calc_result, report_system),
    )


def _parse_birth_datetime(birth_date: str, birth_time: str) -> tuple[datetime, str]:
    normalized_time = birth_time.strip()
    if len(normalized_time) == 5:
        normalized_time = f"{normalized_time}:00"
    try:
        birth_dt = datetime.strptime(f"{birth_date.strip()} {normalized_time}", "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise ValueError("出生日期或出生时间格式无效；日期使用 YYYY-MM-DD，时间使用 HH:MM 或 HH:MM:SS。") from exc
    return birth_dt, normalized_time


def _normalize_gender(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"male", "m", "男"}:
        return "male"
    if normalized in {"female", "f", "女"}:
        return "female"
    raise ValueError("性别必须为 male/female，或中文 男/女。")


def _normalize_report_system(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in REPORT_SYSTEM_LABELS:
        return normalized
    raise ValueError(f"报告体系必须为: {report_system_allowed_text()}。未来体系需等独立功能实现后启用。")


def _render_document(*, form: WebReportForm, result: WebReportResult | None, errors: list[str]) -> str:
    generated_at = now_cn().isoformat()
    body_parts = [
        "<!doctype html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>FateCat Web Markdown 报告</title>",
        _render_workspace_style(),
        "</head>",
        "<body>",
        _render_production_workspace(form=form, result=result, errors=errors, generated_at=generated_at),
    ]

    body_parts.extend(
        [
            _render_copy_script(),
            "</body>",
            "</html>",
        ]
    )
    return "\n".join(body_parts)


def _render_workspace_style() -> str:
    """渲染 Web 生产空间的黄金比例三块布局；对齐 pdf 工作台全屏结构。"""
    return "\n".join(
        [
            "<style>",
            ":root {",
            "  --phi-major: 61.8034%;",
            "  --phi-minor: 38.1966%;",
            "  --phi-major-fr: 1.61803398875fr;",
            "  --phi-minor-fr: 1fr;",
            "  --web-production-panel-gap: 0;",
            "  --web-production-panel-border: #3a3a3a;",
            "  --web-production-panel-bg: #202020;",
            "  --web-production-body-bg: #111;",
            "  --web-production-text: #f2f2f2;",
            "  --web-production-link: #9db5ff;",
            "}",
            "html { height: 100%; overflow: hidden; }",
            "body {",
            "  margin: 0;",
            "  padding: 1rem;",
            "  box-sizing: border-box;",
            "  height: 100%;",
            "  overflow: hidden;",
            "  color: var(--web-production-text);",
            "  background: var(--web-production-body-bg);",
            '  font-family: "Noto Sans SC", "Microsoft YaHei", Arial, sans-serif;',
            "}",
            "a { color: var(--web-production-link); }",
            "h1, h2, h3 { margin: 0 0 0.75rem; }",
            "p { margin: 0 0 0.75rem; }",
            "form { margin: 0; }",
            "fieldset {",
            "  border: 1px solid #555;",
            "  margin: 0;",
            "  padding: 0.75rem;",
            "}",
            "label {",
            "  display: block;",
            "  margin-bottom: 0.25rem;",
            "  font-weight: 700;",
            "}",
            "input, select, textarea, button {",
            "  box-sizing: border-box;",
            "  max-width: 100%;",
            "  font: inherit;",
            "}",
            'input[type="text"], input[type="date"], input[type="time"], select, textarea {',
            "  width: 100%;",
            "  border: 1px solid #777;",
            "  border-radius: 0;",
            "  padding: 0.55rem;",
            "  color: #111;",
            "  background: #fff;",
            "}",
            "button {",
            "  width: 100%;",
            "  border: 1px solid #f2f2f2;",
            "  border-radius: 0;",
            "  padding: 0.8rem 1rem;",
            "  color: #111;",
            "  background: #f2f2f2;",
            "  font-weight: 700;",
            "  cursor: pointer;",
            "}",
            "pre {",
            "  overflow: auto;",
            "  padding: 0.75rem;",
            "  background: #050505;",
            "  color: #f2f2f2;",
            "  border: 1px solid #444;",
            "}",
            "details {",
            "  margin-top: 1rem;",
            "  border-top: 1px solid #333;",
            "  padding-top: 0.75rem;",
            "}",
            "summary { cursor: pointer; font-weight: 700; }",
            ".web-production-grid {",
            "  height: calc(100vh - 2rem);",
            "  display: grid;",
            "  grid-template-columns:",
            "    minmax(0, min(var(--phi-minor), calc((100vh - 2rem) * 0.618034)))",
            "    minmax(0, 1fr);",
            "  grid-template-rows: minmax(0, var(--phi-major-fr)) minmax(0, var(--phi-minor-fr));",
            "  gap: var(--web-production-panel-gap);",
            "  min-height: 0;",
            "}",
            ".web-production-panel {",
            "  min-width: 0;",
            "  min-height: 0;",
            "  overflow: auto;",
            "  padding: 0.9rem;",
            "  border: 1px solid var(--web-production-panel-border);",
            "  background: var(--web-production-panel-bg);",
            "  color: var(--web-production-text);",
            "}",
            ".web-production-brand {",
            "  grid-column: 1;",
            "  grid-row: 1;",
            "  display: grid;",
            "  align-content: start;",
            "}",
            ".web-production-report {",
            "  grid-column: 2;",
            "  grid-row: 1;",
            "}",
            ".web-production-report-header {",
            "  display: flex;",
            "  align-items: center;",
            "  justify-content: space-between;",
            "  gap: 0.75rem;",
            "  margin-bottom: 0.75rem;",
            "}",
            ".web-production-report-header h2 { margin: 0; }",
            ".web-production-submit-button {",
            "  flex: 0 0 auto;",
            "  width: auto;",
            "  min-width: 10rem;",
            "}",
            ".web-production-input {",
            "  grid-column: 1 / span 2;",
            "  grid-row: 2;",
            "}",
            ".web-production-control-grid {",
            "  display: grid;",
            "  grid-template-columns: repeat(6, minmax(0, 1fr));",
            "  gap: 0.75rem;",
            "  align-items: end;",
            "}",
            ".web-production-control-grid p { margin: 0; }",
            ".web-production-control-wide { grid-column: span 2; }",
            "@media (max-width: 56rem) {",
            "  html, body { height: auto; overflow: auto; }",
            "  .web-production-grid {",
            "    display: block;",
            "    height: auto;",
            "    min-height: 0;",
            "  }",
            "  .web-production-panel {",
            "    overflow: visible;",
            "  }",
            "  .web-production-control-grid {",
            "    grid-template-columns: 1fr;",
            "  }",
            "  .web-production-control-wide {",
            "    grid-column: auto;",
            "  }",
            "}",
            "</style>",
        ]
    )


def _render_production_workspace(
    *, form: WebReportForm, result: WebReportResult | None, errors: list[str], generated_at: str
) -> str:
    return "\n".join(
        [
            '<form class="web-production-grid" method="get" action="/web">',
            '<section class="web-production-panel web-production-brand" aria-labelledby="project-brand">',
            _render_branding_panel(),
            "</section>",
            '<section class="web-production-panel web-production-report" aria-labelledby="production-report">',
            _render_report_panel(result=result, errors=errors),
            "</section>",
            '<section class="web-production-panel web-production-input" aria-labelledby="input-form">',
            _render_input_panel(form=form, result=result, errors=errors, generated_at=generated_at),
            "</section>",
            "</form>",
        ]
    )


def _render_report_panel(*, result: WebReportResult | None, errors: list[str]) -> str:
    parts = [
        '<div class="web-production-report-header">',
        '<h2 id="production-report">生成报告</h2>',
        '<button class="web-production-submit-button" type="submit">生成 Markdown 报告</button>',
        "</div>",
    ]
    if errors:
        parts.append(_render_errors(errors))
    if result:
        parts.append(_render_report(result))
    if not errors and result is None:
        parts.append("<p>尚未生成报告。提交底部参数后，服务端会在这里写入 Markdown 输出。</p>")
    return "\n".join(parts)


def _render_branding_panel() -> str:
    branding = get_branding_payload()
    links = [
        ("DEX Screener", branding["dexScreenerUrl"]),
        ("X", branding["xUrl"]),
        ("GitHub", branding["githubUrl"]),
        ("Hugging Face", branding["huggingFaceUrl"]),
    ]
    link_items = "\n".join(f'<li><a href="{_attr(url)}">{_h(label)}</a></li>' for label, url in links)
    return "\n".join(
        [
            '<h2 id="project-brand">项目归属</h2>',
            f"<p>{_h(branding['heroTitle'])}</p>",
            f"<p>{_h(branding['sponsorText'])}</p>",
            f"<p>{_h(branding['tagline'])}</p>",
            f"<ul>\n{link_items}\n</ul>",
        ]
    )


def _render_page_nav(*, has_result: bool, has_errors: bool) -> str:
    links = [
        ("#project-brand", "项目"),
        ("#production-report", "报告"),
        ("#input-form", "参数"),
        ("#field-contract", "字段契约"),
    ]
    if has_errors:
        links.append(("#errors", "错误"))
    if has_result:
        links.extend(
            [
                ("#workbench", "工作台"),
                ("#markdown-output", "Markdown"),
            ]
        )
    links.append(("#page-info", "页面信息"))
    items = "\n".join(f'<li><a href="{href}">{label}</a></li>' for href, label in links)
    return f'<nav aria-label="页面导航">\n<ul>\n{items}\n</ul>\n</nav>'


def _render_page_info(generated_at: str) -> str:
    return "\n".join(
        [
            '<details id="page-info">',
            "<summary>页面说明与元信息</summary>",
            "<p>该页面使用原生 HTML 表单生成标准命理排盘 Markdown 报告。核心结果由服务端直接写入页面。</p>",
            _render_meta(generated_at),
            _render_navigation(),
            "</details>",
        ]
    )


def _render_meta(generated_at: str) -> str:
    rows = [
        ("入口", "GET /web"),
        ("输出", "Markdown 文本"),
        ("报告模板", "report_generator.generate_full_report(report_system)"),
        ("地区解析", "location.get"),
        ("时间", generated_at),
        ("时区", "Asia/Hong_Kong"),
    ]
    items = "\n".join(f"<dt>{_h(k)}</dt><dd>{_h(v)}</dd>" for k, v in rows)
    return f"<h2>页面元信息</h2>\n<dl>\n{items}\n</dl>"


def _render_navigation() -> str:
    return "\n".join(
        [
            "<h2>相关入口</h2>",
            "<nav>",
            "<ul>",
            '<li><a href="/health">GET /health</a></li>',
            '<li><a href="/docs">FastAPI /docs</a></li>',
            '<li><a href="/web">GET /web 空表单</a></li>',
            "</ul>",
            "</nav>",
        ]
    )


def _render_field_contract() -> str:
    rows = [
        ["birthDate", "出生日期", "是", "YYYY-MM-DD", "HTML date；例 1990-01-01"],
        ["birthTime", "出生时间", "是", "HH:MM 或 HH:MM:SS", "HTML time；例 08:00"],
        ["birthPlace", "出生地区", "是", "中文地点或 lng,lat", "例 北京 / 116.4074,39.9042"],
        ["gender", "性别", "是", "male/female", "计算必需；不能默认猜测"],
        ["reportSystem", "输出体系", "否", report_system_allowed_text(), "默认 bazi；每次只输出一个已实现体系"],
        ["name", "姓名", "否", "文本", "为空时报告标题使用命主"],
    ]
    table = tabulate(rows, headers=["参数", "字段", "必填", "格式", "说明"], tablefmt="psql", missingval="")
    return f'<h2 id="field-contract">字段契约</h2>\n<pre><code>{_h(table)}</code></pre>'


def _render_input_panel(
    form: WebReportForm, result: WebReportResult | None, errors: list[str], generated_at: str
) -> str:
    parts = [
        '<h2 id="input-form">参数控件</h2>',
        '<input type="hidden" name="submitted" value="1">',
        '<div class="web-production-control-grid">',
        "<p>",
        '<label for="birthDate">出生日期（必填）</label><br>',
        f'<input id="birthDate" name="birthDate" type="date" value="{_attr(form.birth_date)}">',
        "</p>",
        "<p>",
        '<label for="birthTime">出生时间（必填）</label><br>',
        f'<input id="birthTime" name="birthTime" type="time" value="{_attr(_time_value(form.birth_time))}">',
        "</p>",
        '<p class="web-production-control-wide">',
        '<label for="birthPlace">出生地区（必填）</label><br>',
        (
            '<input id="birthPlace" name="birthPlace" type="text" '
            f'value="{_attr(public_birth_place(form.birth_place))}" '
            'placeholder="北京 或 116.4074,39.9042">'
        ),
        "</p>",
        "<p>",
        '<label for="gender">性别（必填）</label><br>',
        '<select id="gender" name="gender">',
        f'<option value=""{_selected(form.gender, "")}>请选择</option>',
        f'<option value="male"{_selected(form.gender, "male")}>男 male</option>',
        f'<option value="female"{_selected(form.gender, "female")}>女 female</option>',
        "</select>",
        "</p>",
        '<p class="web-production-control-wide">',
        '<label for="reportSystem">输出体系</label><br>',
        '<select id="reportSystem" name="reportSystem">',
        *_render_report_system_options(form.report_system),
        "</select>",
        "</p>",
        '<p class="web-production-control-wide">',
        '<label for="name">姓名（非必填）</label><br>',
        f'<input id="name" name="name" type="text" value="{_attr(form.name)}" placeholder="可为空">',
        "</p>",
        "</div>",
        _render_field_contract(),
        _render_page_nav(has_result=result is not None, has_errors=bool(errors)),
        _render_page_info(generated_at),
    ]
    if form.submitted or form.has_input():
        parts.append(_render_submitted_input(form, result))
    return "\n".join(parts)


def _render_submitted_input(form: WebReportForm, result: WebReportResult | None) -> str:
    rows = [
        ["birthDate", form.birth_date, "query"],
        ["birthTime", form.birth_time, "query"],
        ["birthPlace", public_birth_place(form.birth_place), "query"],
        ["gender", form.gender, "query"],
        ["reportSystem", form.report_system or "bazi", "query"],
        ["name", form.name, "query"],
    ]
    if result:
        rows.extend(
            [
                ["selectedReportSystem", result.report_system_label, "server"],
                ["normalizedBirthTime", result.normalized_time, "server"],
                ["longitude", result.resolved_longitude, "location.get"],
                ["latitude", result.resolved_latitude, "location.get"],
            ]
        )
    table = tabulate(rows, headers=["字段", "值", "来源"], tablefmt="psql", missingval="")
    return f'<h2 id="submitted-input">当前输入</h2>\n<pre><code>{_h(table)}</code></pre>'


def _render_errors(errors: list[str]) -> str:
    items = "\n".join(f"<li>{_h(error)}</li>" for error in errors)
    return f'<h2 id="errors">错误</h2>\n<ul>\n{items}\n</ul>'


def _render_report(result: WebReportResult) -> str:
    raw_json = json.dumps(result.input_payload, ensure_ascii=False, indent=2)
    return "\n".join(
        [
            _render_workbench(result),
            '<h2 id="markdown-output">Markdown 输出</h2>',
            f"<p>当前输出体系：{_h(result.report_system_label)}</p>",
            '<p><button type="button" id="copy-report">复制 Markdown</button></p>',
            '<p id="copy-status">尚未复制</p>',
            '<pre><code id="report-markdown">' + _h(result.markdown) + "</code></pre>",
            "<details>",
            "<summary>机器可读输入</summary>",
            "<pre><code>" + _h(raw_json) + "</code></pre>",
            "</details>",
        ]
    )


def _build_workbench_payload(calc_result: dict[str, Any], report_system: str) -> dict[str, Any]:
    """构建 Web 工作台数据；只消费后端结构化结果，不定义命理规则。"""
    if report_system == "ziwei":
        return {
            "system": "ziwei",
            "palaces": calc_result.get("palaceAnalysis", []),
            "starTaxonomy": calc_result.get("ziweiStarTaxonomy", {}),
            "mutagenFlow": calc_result.get("ziweiMutagenFlow", {}),
            "palaceTopics": calc_result.get("ziweiPalaceTopics", []),
            "goldenGuards": calc_result.get("ziweiGoldenGuards", {}),
            "ruleDepth": calc_result.get("ziweiRuleDepth", {}),
        }
    return {
        "system": "bazi",
        "fourPillars": calc_result.get("fourPillars", {}),
        "tenGods": calc_result.get("tenGods", {}),
        "hiddenStems": calc_result.get("hiddenStems", {}),
        "wuxingScores": calc_result.get("wuxingScores", {}),
        "geju": calc_result.get("geju", {}),
        "yongShen": calc_result.get("yongShen", {}),
        "majorFortune": calc_result.get("majorFortune", {}),
        "annualFortune": calc_result.get("annualFortune", []),
        "baziBenchmark": calc_result.get("baziBenchmark", {}),
        "ruleDepth": calc_result.get("baziRuleDepth", {}),
    }


def _render_workbench(result: WebReportResult) -> str:
    if result.report_system == "ziwei":
        return _render_ziwei_workbench(result.workbench)
    return _render_bazi_workbench(result.workbench)


def _render_bazi_workbench(workbench: dict[str, Any]) -> str:
    pillars = workbench.get("fourPillars", {}) if isinstance(workbench.get("fourPillars"), dict) else {}
    pillar_rows = []
    for key, label in [("year", "年柱"), ("month", "月柱"), ("day", "日柱"), ("hour", "时柱")]:
        item = pillars.get(key, {}) if isinstance(pillars.get(key), dict) else {}
        pillar_rows.append([label, item.get("fullName", ""), item.get("stem", ""), item.get("branch", "")])
    benchmark = workbench.get("baziBenchmark", {}) if isinstance(workbench.get("baziBenchmark"), dict) else {}
    strength = benchmark.get("strengthScore", {}) if isinstance(benchmark.get("strengthScore"), dict) else {}
    renyuan = benchmark.get("renYuanSiling", {}) if isinstance(benchmark.get("renYuanSiling"), dict) else {}
    yongshen = workbench.get("yongShen", {}) if isinstance(workbench.get("yongShen"), dict) else {}
    geju = workbench.get("geju", {}) if isinstance(workbench.get("geju"), dict) else {}
    rule_depth = workbench.get("ruleDepth", {}) if isinstance(workbench.get("ruleDepth"), dict) else {}
    trigger_rows = []
    for item in benchmark.get("fortuneTriggers", [])[:12] if isinstance(benchmark.get("fortuneTriggers"), list) else []:
        if isinstance(item, dict):
            trigger_rows.append([item.get("year", ""), item.get("ganZhi", ""), "；".join(item.get("reasons", []))])
    if not trigger_rows:
        trigger_rows.append(["-", "-", "当前样本未命中已登记触发项"])
    return "\n".join(
        [
            '<h2 id="workbench">八字工作台</h2>',
            "<p>该区域只展示后端结构化字段；复制 Markdown 内容不受工作台影响。</p>",
            "<details open><summary>四柱 / 十神 / 藏干</summary>",
            "<pre><code>"
            + _h(tabulate(pillar_rows, headers=["柱位", "干支", "天干", "地支"], tablefmt="psql"))
            + "</code></pre>",
            "</details>",
            "<details><summary>五行强弱与人元司令</summary>",
            "<pre><code>"
            + _h(
                json.dumps(
                    {
                        "strengthScore": strength,
                        "renYuanSiling": renyuan,
                        "wuxingScores": workbench.get("wuxingScores", {}),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            + "</code></pre>",
            "</details>",
            "<details><summary>格局与用神策略</summary>",
            "<pre><code>"
            + _h(
                json.dumps(
                    {
                        "geju": geju,
                        "yongShen": yongshen,
                        "yongShenStrategies": benchmark.get("yongShenStrategies", []),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            + "</code></pre>",
            "</details>",
            "<details><summary>大运流年触发</summary>",
            "<pre><code>"
            + _h(tabulate(trigger_rows, headers=["年份", "干支", "触发依据"], tablefmt="psql"))
            + "</code></pre>",
            "</details>",
            "<details><summary>规则深度 / 冲突策略</summary>",
            "<pre><code>" + _h(json.dumps(rule_depth, ensure_ascii=False, indent=2)) + "</code></pre>",
            "</details>",
        ]
    )


def _render_ziwei_workbench(workbench: dict[str, Any]) -> str:
    palaces = workbench.get("palaces", []) if isinstance(workbench.get("palaces"), list) else []
    palace_rows = []
    for palace in palaces:
        if not isinstance(palace, dict):
            continue
        palace_rows.append(
            [
                palace.get("name", ""),
                palace.get("earthlyBranch", ""),
                "、".join(_star_name_list(palace.get("majorStars"))),
                "命" if palace.get("isOriginalPalace") else "",
                "身" if palace.get("isBodyPalace") else "",
            ]
        )
    taxonomy = workbench.get("starTaxonomy", {}) if isinstance(workbench.get("starTaxonomy"), dict) else {}
    mutagen_flow = workbench.get("mutagenFlow", {}) if isinstance(workbench.get("mutagenFlow"), dict) else {}
    rule_depth = workbench.get("ruleDepth", {}) if isinstance(workbench.get("ruleDepth"), dict) else {}
    return "\n".join(
        [
            '<h2 id="workbench">紫微工作台</h2>',
            "<p>该区域只展示后端 iztro 结构化字段与解释索引；紫微仍为 standalone 输出。</p>",
            "<details open><summary>十二宫 / 星曜</summary>",
            "<pre><code>"
            + _h(tabulate(palace_rows, headers=["宫位", "地支", "主星", "命宫", "身宫"], tablefmt="psql"))
            + "</code></pre>",
            "</details>",
            "<details><summary>星曜分类 / 庙旺利陷</summary>",
            "<pre><code>" + _h(json.dumps(taxonomy, ensure_ascii=False, indent=2)) + "</code></pre>",
            "</details>",
            "<details><summary>四化飞入 / 运限</summary>",
            "<pre><code>" + _h(json.dumps(mutagen_flow, ensure_ascii=False, indent=2)) + "</code></pre>",
            "</details>",
            "<details><summary>规则深度 / 冲突策略</summary>",
            "<pre><code>" + _h(json.dumps(rule_depth, ensure_ascii=False, indent=2)) + "</code></pre>",
            "</details>",
        ]
    )


def _star_name_list(stars: object) -> list[str]:
    if not isinstance(stars, list):
        return []
    names = []
    for star in stars:
        if isinstance(star, dict) and star.get("name"):
            names.append(str(star.get("name")))
    return names


def _render_copy_script() -> str:
    return "\n".join(
        [
            "<script>",
            "(() => {",
            '  const button = document.getElementById("copy-report");',
            '  const source = document.getElementById("report-markdown");',
            '  const status = document.getElementById("copy-status");',
            "  if (!button || !source || !status) { return; }",
            '  button.addEventListener("click", async () => {',
            "    try {",
            '      await navigator.clipboard.writeText(source.textContent || "");',
            '      status.textContent = "已复制 Markdown";',
            "    } catch (error) {",
            '      status.textContent = "复制失败；请手动选择 Markdown 输出区域复制。";',
            "    }",
            "  });",
            "})();",
            "</script>",
            "<noscript><p>当前浏览器未执行 JavaScript；请手动选择 Markdown 输出区域复制。</p></noscript>",
        ]
    )


def _selected(current: str, expected: str) -> str:
    return " selected" if current == expected else ""


def _render_report_system_options(current: str) -> list[str]:
    normalized = current if current in REPORT_SYSTEM_LABELS else "bazi"
    lines: list[str] = []
    current_group = ""
    for system in PREDICTION_SYSTEMS:
        if system.group != current_group:
            if current_group:
                lines.append("</optgroup>")
            current_group = system.group
            lines.append(f'<optgroup label="{_attr(current_group)}">')
        selected = _selected(normalized, system.id) if system.enabled else ""
        disabled = "" if system.enabled else " disabled"
        suffix = (
            "" if system.enabled else "（结构化 capability 已可用）" if system.status == "production" else "（待实现）"
        )
        lines.append(
            f'<option value="{_attr(system.id)}"{selected}{disabled}>{_h(system.label)} {system.id}{suffix}</option>'
        )
    if current_group:
        lines.append("</optgroup>")
    return lines


def _time_value(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 5:
        return stripped[:5]
    return stripped


def _h(value: object) -> str:
    return escape("" if value is None else str(value), quote=False)


def _attr(value: object) -> str:
    return escape("" if value is None else str(value), quote=True)
