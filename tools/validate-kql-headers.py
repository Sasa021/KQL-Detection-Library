#!/usr/bin/env python3
"""Check detection query headers and the index.

Run from anywhere:

    python3 tools/validate-kql-headers.py

The script exits 0 when every detections/**/*.kql file has the required
header and detections-index.md points at the same technique and table.
It exits 1 and prints one line per problem otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DETECTIONS = ROOT / "detections"
INDEX = ROOT / "detections-index.md"

REQUIRED = [
    "name",
    "attack_technique",
    "data_source",
    "description",
    "false_positives",
    "tuning_notes",
    "atomic_test",
    "status",
]

TABLES = {
    "SecurityEvent",
    "SigninLogs",
    "DeviceProcessEvents",
    "DeviceFileEvents",
    "DeviceRegistryEvents",
    "DeviceLogonEvents",
    "DeviceEvents",
    "DeviceNetworkEvents",
}

TECHNIQUE_RE = re.compile(r"^T\d{4}(\.\d{3})?$")
ATOMIC_RE = re.compile(r"^T\d{4}(\.\d{3})?-\d+$")
HEADER_RE = re.compile(r"^// ([a-z_]+): (.+)$")
INDEX_LINK_RE = re.compile(r"^\[([^\]]+)\]\(([^)]+)\)$")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_query(path: Path) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        errors.append(f"{rel(path)}: remove the byte order mark")
        text = text.lstrip("\ufeff")
    lines = text.splitlines()
    header: dict[str, str] = {}
    index = 0
    while index < len(lines) and lines[index].startswith("//"):
        match = HEADER_RE.match(lines[index])
        if not match:
            errors.append(f"{rel(path)}: header line is not '// field: value': {lines[index]}")
            index += 1
            continue
        key, value = match.group(1), match.group(2).strip()
        if key in header:
            errors.append(f"{rel(path)}: duplicate header field {key}")
        if not value:
            errors.append(f"{rel(path)}: empty header field {key}")
        header[key] = value
        index += 1

    if index >= len(lines) or lines[index].strip() != "":
        errors.append(f"{rel(path)}: expected a blank line after the header")
    else:
        index += 1

    body = "\n".join(lines[index:]).strip()
    if not body:
        errors.append(f"{rel(path)}: query body is empty")

    keys = list(header)
    if keys != REQUIRED:
        errors.append(
            f"{rel(path)}: header fields must be {', '.join(REQUIRED)} in that order"
        )

    technique = header.get("attack_technique", "")
    if technique and not TECHNIQUE_RE.match(technique):
        errors.append(f"{rel(path)}: attack_technique is not a technique ID: {technique}")

    atomic = header.get("atomic_test", "")
    if atomic and not ATOMIC_RE.match(atomic):
        errors.append(f"{rel(path)}: atomic_test is not a test ID such as T1082-1: {atomic}")

    table = header.get("data_source", "")
    if table and table not in TABLES:
        errors.append(f"{rel(path)}: data_source is not a known table: {table}")
    elif table and body and table not in body:
        errors.append(f"{rel(path)}: query body does not use {table}")

    status = header.get("status", "")
    if status and status not in {"untested", "tested"}:
        errors.append(f"{rel(path)}: status must be untested or tested, found {status}")

    notes = header.get("tuning_notes", "")
    if notes and "PLACEHOLDER" not in notes:
        errors.append(f"{rel(path)}: tuning_notes must keep the word PLACEHOLDER")

    return header, body, errors


def parse_index() -> tuple[dict[str, dict[str, str]], list[str]]:
    errors: list[str] = []
    rows: dict[str, dict[str, str]] = {}
    if not INDEX.is_file():
        return rows, ["detections-index.md is missing"]

    for line_no, line in enumerate(INDEX.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 5:
            continue
        if cells[0] in {"Query", "---"} or set(cells[0]) <= {"-", ":"}:
            continue
        if not cells[0].startswith("["):
            continue
        match = INDEX_LINK_RE.match(cells[0])
        if not match:
            errors.append(f"detections-index.md:{line_no}: query cell is not a markdown link")
            continue
        label, target = match.group(1), match.group(2)
        if label != target:
            errors.append(
                f"detections-index.md:{line_no}: link text and target differ ({label} vs {target})"
            )
        tested = cells[3].lower()
        fired = cells[4].lower()
        if tested not in {"", "yes", "no"}:
            errors.append(
                f"detections-index.md:{line_no}: Tested must be blank, yes, or no"
            )
        if fired not in {"", "yes", "no"}:
            errors.append(
                f"detections-index.md:{line_no}: Fired must be blank, yes, or no"
            )
        if target in rows:
            errors.append(f"detections-index.md:{line_no}: duplicate query {target}")
        rows[target] = {
            "technique": cells[1],
            "data_source": cells[2],
            "tested": tested,
            "fired": fired,
        }
    return rows, errors


def main() -> int:
    errors: list[str] = []
    files = sorted(DETECTIONS.rglob("*.kql"))
    if not files:
        print("No .kql files under detections/", file=sys.stderr)
        return 1

    headers: dict[str, dict[str, str]] = {}
    for path in files:
        header, _body, file_errors = parse_query(path)
        errors.extend(file_errors)
        headers[rel(path)] = header

    index_rows, index_errors = parse_index()
    errors.extend(index_errors)

    file_set = set(headers)
    index_set = set(index_rows)
    for missing in sorted(file_set - index_set):
        errors.append(f"detections-index.md does not list {missing}")
    for extra in sorted(index_set - file_set):
        errors.append(f"detections-index.md lists {extra} but that file does not exist")

    for path, row in sorted(index_rows.items()):
        header = headers.get(path)
        if not header:
            continue
        if row["technique"] != header.get("attack_technique"):
            errors.append(
                f"{path}: index technique {row['technique']} does not match header {header.get('attack_technique')}"
            )
        if row["data_source"] != header.get("data_source"):
            errors.append(
                f"{path}: index data source {row['data_source']} does not match header {header.get('data_source')}"
            )

    if errors:
        print(f"{len(errors)} problem(s):", file=sys.stderr)
        for item in errors:
            print(item, file=sys.stderr)
        return 1

    print(f"OK: {len(files)} query file(s), index matches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
