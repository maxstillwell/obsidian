from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


INVENTORY_FIELDS = [
    "id",
    "original_path",
    "filename",
    "extension",
    "size_bytes",
    "created_time",
    "modified_time",
    "hash",
    "source_name",
    "source_type",
    "guessed_type",
    "mime_guess",
    "suggested_area",
    "suggested_project",
    "suggested_destination",
    "pii_risk",
    "secret_risk",
    "import_action",
    "import_reason",
    "needs_manual_review",
    "can_read_content",
    "extracted_text_path",
    "obsidian_note_path",
    "attachment_path",
    "source_url",
    "http_status",
    "content_type",
    "page_title",
    "duplicate_of",
    "error",
]


def write_inventory(records: Iterable[dict], csv_path: Path, json_path: Path) -> None:
    rows = list(records)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INVENTORY_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in INVENTORY_FIELDS})
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def read_inventory(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
