"""Markdown 报告呈现基础工具。

这里不计算命理事实，只处理报告文本的表格、安全转义和行内压缩。
"""

from __future__ import annotations


def normalize_present_text(text: str) -> str:
    """清理呈现层提示词，不改变上游计算字段。"""
    if not text:
        return text
    return (
        text.replace("（依据，展开）", "（依据）")
        .replace("（全展开）", "")
        .replace("（全量）", "")
        .replace("（展开）", "")
    )


def table_escape(value: object) -> str:
    """保护 Markdown 表格分隔符。"""
    text = "" if value is None else str(value)
    return text.replace("|", "｜")


def render_markdown_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    """渲染 Markdown 表格。"""
    if not headers:
        return []
    output: list[str] = []
    output.append("| " + " | ".join(table_escape(header) for header in headers) + " |")
    output.append("| " + " | ".join([":--"] * len(headers)) + " |")
    for row in rows:
        cells = row if isinstance(row, list) else [row]
        cells = list(cells) + [""] * (len(headers) - len(cells))
        output.append("| " + " | ".join(table_escape(cell) for cell in cells[: len(headers)]) + " |")
    output.append("")
    return output


def compact_inline_text(value: str) -> str:
    """将多行文本压成单行，便于表格呈现。"""
    if not value:
        return ""
    return " ".join(item.strip() for item in str(value).splitlines() if item.strip())


__all__ = ["compact_inline_text", "normalize_present_text", "render_markdown_table", "table_escape"]
