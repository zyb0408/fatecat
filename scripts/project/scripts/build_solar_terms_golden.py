#!/usr/bin/env python3
"""从本地 raw 交节时间表生成可提交的节气 golden fixture。"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "assets/data/calendar/solar_terms/raw/1900-2030年的交节时间.csv"
OUTPUT_FILE = ROOT / "assets/data/calendar/solar_terms/golden/solar_terms_1900_2030.json"

TERM_NAME_MAP = {
    "驚蟄": "惊蛰",
    "榖雨": "谷雨",
    "小滿": "小满",
    "芒種": "芒种",
    "處暑": "处暑",
}

SOURCE_SHA256 = "76585429b1af2d4b9b66bf06c6eaf7ce8696a76b47fd18b1f27497df8d4759e4"
SOURCE_NAME = "1900-2030年的交节时间.csv"


def normalize_term(name: str) -> str:
    """统一繁简节气名，避免测试口径被编码差异干扰。"""
    return TERM_NAME_MAP.get(name.strip(), name.strip())


def read_rows() -> list[dict[str, object]]:
    """读取 raw CSV 并转换为稳定 JSON 结构。"""
    rows: list[dict[str, object]] = []
    with RAW_FILE.open("r", encoding="gbk", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            term = normalize_term(row.get("節氣", ""))
            if not term:
                continue
            second_float = float(row["秒"])
            second = int(second_float)
            microsecond = int(round((second_float - second) * 1_000_000))
            when = datetime(
                int(row["西元"]),
                int(row["月"]),
                int(row["日"]),
                int(row["時"]),
                int(row["分"]),
                second,
                microsecond,
            )
            rows.append(
                {
                    "term": term,
                    "year": when.year,
                    "month": when.month,
                    "day": when.day,
                    "hour": when.hour,
                    "minute": when.minute,
                    "second": second_float,
                    "iso": when.isoformat(timespec="microseconds"),
                }
            )
    return rows


def main() -> int:
    rows = read_rows()
    payload = {
        "schemaVersion": 1,
        "timezone": "Asia/Shanghai",
        "source": {
            "name": SOURCE_NAME,
            "encoding": "gbk",
            "sha256": SOURCE_SHA256,
            "usage": "本 fixture 只做 lunar-python 节气边界 golden 回归，不替换生产历法算法。",
        },
        "coverage": {
            "startYear": min(int(row["year"]) for row in rows),
            "endYear": max(int(row["year"]) for row in rows),
            "termsPerYear": 24,
            "rowCount": len(rows),
        },
        "toleranceSeconds": 3660,
        "rows": rows,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"wrote {OUTPUT_FILE} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
