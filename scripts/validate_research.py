#!/usr/bin/env python3
"""Validate JSON research records for an international macro news issue."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


REQUIRED = (
    "country", "category", "title", "event_date", "publication_date",
    "source_name", "source_url", "summary", "selection_reason",
    "cross_checked", "included",
)


def parse_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be YYYY-MM-DD, got {value!r}") from exc


def valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate dates, fields, URLs, and duplicates.")
    parser.add_argument("records", type=Path, help="UTF-8 JSON array of research records")
    parser.add_argument("--start", required=True, help="issue start date, YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="issue end date, YYYY-MM-DD")
    args = parser.parse_args()

    start = parse_date(args.start, "--start")
    end = parse_date(args.end, "--end")
    if start > end:
        parser.error("--start must not be after --end")

    try:
        records = json.loads(args.records.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(records, list):
        print("ERROR: top-level JSON value must be an array", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    seen: dict[tuple[str, str], int] = {}
    included_count = 0

    for number, record in enumerate(records, start=1):
        prefix = f"record {number}"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        missing = [key for key in REQUIRED if key not in record]
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(missing)}")
            continue
        try:
            publication_date = parse_date(record["publication_date"], "publication_date")
            parse_date(record["event_date"], "event_date")
        except ValueError as exc:
            errors.append(f"{prefix}: {exc}")
            continue
        if record["included"]:
            included_count += 1
            if not start <= publication_date <= end:
                errors.append(f"{prefix}: included publication_date {publication_date} is outside {start} to {end}")
            if not valid_http_url(str(record["source_url"])):
                errors.append(f"{prefix}: source_url is not an absolute HTTP(S) URL")
            if not str(record["selection_reason"]).strip():
                errors.append(f"{prefix}: included item needs a selection_reason")
            if not isinstance(record["cross_checked"], bool):
                errors.append(f"{prefix}: cross_checked must be true or false")
        key = (" ".join(str(record["title"]).lower().split()), str(record["publication_date"]))
        if key in seen:
            warnings.append(f"{prefix}: possible duplicate of record {seen[key]}")
        else:
            seen[key] = number

    if included_count == 0:
        warnings.append("no records are marked included")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"Checked {len(records)} records; {included_count} included; {len(errors)} errors; {len(warnings)} warnings.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
