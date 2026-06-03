from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import uuid

from .config import BuilderConfig
from .sanitize import safe_join, sanitize_filename, unique_filename


def create_import_plan(records: list[dict], config: BuilderConfig) -> Path:
    output = safe_join(config.vault_path, "_System/IMPORT_PLAN.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    importable = importable_records(records)
    review = [record for record in records if _as_bool(record.get("needs_manual_review"))]
    lines = [
        "# IMPORT_PLAN",
        "",
        "## Status",
        "",
        "Gate C is required before `run_import.py --execute` can create notes or copy attachments.",
        "",
        "## Summary",
        "",
        f"- Inventory records: {len(records)}",
        f"- Planned importable records: {len(importable)}",
        f"- Manual review records: {len(review)}",
        "",
        "## Planned Actions",
        "",
    ]
    if importable:
        for record in importable[:200]:
            lines.append(
                f"- `{record.get('import_action')}` -> `{record.get('suggested_destination')}`: "
                f"{record.get('source_url') or record.get('original_path')}"
            )
        if len(importable) > 200:
            lines.append(f"- Truncated: {len(importable) - 200} additional records not shown.")
    else:
        lines.append("- No records are currently importable.")
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "- Originals will not be deleted, moved, renamed, or overwritten.",
            "- Critical or high-risk records remain blocked or manual-review only.",
            "- This plan does not allow network, OCR, transcription, online AI, or embeddings.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def execute_import(records: list[dict], config: BuilderConfig, state_path: Path | str = Path("data/import_state.json")) -> dict:
    batch_id = datetime.now().strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:8]
    created_files: list[str] = []
    skipped: list[dict] = []
    existing: set[str] = set()

    for record in records:
        if not _is_importable(record):
            skipped.append({"id": record.get("id", ""), "reason": "not importable or needs manual review"})
            continue
        destination = str(record.get("suggested_destination") or "60 Resources")
        note_dir = safe_join(config.vault_path, destination)
        note_dir.mkdir(parents=True, exist_ok=True)
        existing_keys = _existing_source_keys(note_dir)
        if _record_already_imported(record, existing_keys):
            skipped.append({"id": record.get("id", ""), "reason": "source_url or hash already imported"})
            continue
        title = _record_title(record)
        filename = unique_filename(f"{title}.md", existing | {path.name for path in note_dir.glob("*.md")}, str(record.get("hash") or record.get("id") or ""))
        note_path = safe_join(note_dir, filename)
        note_path.write_text(_source_note(record, title), encoding="utf-8")
        existing.add(filename)
        created_files.append(str(note_path))

    batch = {
        "batch_id": batch_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "created_files": created_files,
        "skipped": skipped,
    }
    state_file = Path(state_path)
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state = _load_state(state_file)
    state.setdefault("batches", []).append(batch)
    state["last_batch_id"] = batch_id
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    _append_import_log(config, batch)
    return batch


def rollback_batch(config: BuilderConfig, state_path: Path | str = Path("data/import_state.json"), batch_id: str | None = None) -> list[str]:
    state_file = Path(state_path)
    state = _load_state(state_file)
    target_id = batch_id or state.get("last_batch_id")
    if not target_id:
        return []
    removed: list[str] = []
    for batch in state.get("batches", []):
        if batch.get("batch_id") != target_id:
            continue
        for file_path in batch.get("created_files", []):
            path = Path(file_path)
            try:
                path.resolve().relative_to(config.vault_path.expanduser().resolve())
            except ValueError:
                continue
            if path.exists() and path.is_file():
                path.unlink()
                removed.append(str(path))
        batch["rolled_back_at"] = datetime.now().isoformat(timespec="seconds")
        batch["removed_files"] = removed
        break
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return removed


def importable_records(records: list[dict]) -> list[dict]:
    return [record for record in records if _is_importable(record)]


def _is_importable(record: dict) -> bool:
    if _as_bool(record.get("needs_manual_review")):
        return False
    if str(record.get("import_action") or "") in {"skip", "needs_review", ""}:
        return False
    if _as_bool(record.get("secret_risk")):
        return False
    if str(record.get("pii_risk") or "").lower() in {"critical", "high"}:
        return False
    return True


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _record_title(record: dict) -> str:
    page_title = str(record.get("page_title") or "")
    if page_title:
        return sanitize_filename(page_title)
    source_url = str(record.get("source_url") or "")
    if source_url:
        return sanitize_filename(source_url.replace("https://", "").replace("http://", ""))
    return sanitize_filename(str(record.get("filename") or "Source Note"))


def _record_already_imported(record: dict, existing_keys: set[str]) -> bool:
    source_url = str(record.get("source_url") or "").strip()
    file_hash = str(record.get("hash") or "").strip()
    return bool((source_url and f"url:{source_url}" in existing_keys) or (file_hash and f"hash:{file_hash}" in existing_keys))


def _existing_source_keys(note_dir: Path) -> set[str]:
    keys: set[str] = set()
    for note in note_dir.glob("*.md"):
        try:
            text = note.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.splitlines()[:80]:
            if line.startswith("source_url:"):
                value = line.split(":", 1)[1].strip()
                if value:
                    keys.add(f"url:{value}")
            elif line.startswith("hash:"):
                value = line.split(":", 1)[1].strip()
                if value:
                    keys.add(f"hash:{value}")
    return keys


def _source_note(record: dict, title: str) -> str:
    imported_at = datetime.now().isoformat(timespec="seconds")
    source_url = str(record.get("source_url") or "")
    source_path = str(record.get("original_path") or "")
    return f"""---
type: source
title: {title}
created:
modified:
imported_at: {imported_at}
source_path: {source_path}
source_url: {source_url}
source_type: {record.get('source_type', '')}
project: {record.get('suggested_project', '')}
area: {record.get('suggested_area', '')}
tags:
related:
status: imported
confidence:
pii_level: {record.get('pii_risk', '')}
secret_risk: {str(record.get('secret_risk', False)).lower()}
hash: {record.get('hash', '')}
import_action: {record.get('import_action', '')}
---

# {title}

## Summary

Content was not extracted because of privacy, size, unsupported format, or configuration limits.

## Key Points

## Why This Matters

## Related Projects

## Related Notes

## Original Reference

- Original path: {source_path}
- Source URL: {source_url}
- HTTP status: {record.get('http_status', '')}
- Content type: {record.get('content_type', '')}
- Page title: {record.get('page_title', '')}

## Import Metadata
- Imported at: {imported_at}
- Hash: {record.get('hash', '')}
- Import action: {record.get('import_action', '')}
- Privacy risk: {record.get('pii_risk', '')}
"""


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {"batches": [], "last_batch_id": None}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"batches": [], "last_batch_id": None}


def _append_import_log(config: BuilderConfig, batch: dict) -> None:
    log_path = safe_join(config.vault_path, "_System/IMPORT_LOG.md")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write("\n")
        handle.write(f"## Batch {batch['batch_id']}\n\n")
        handle.write(f"- Created files: {len(batch['created_files'])}\n")
        handle.write(f"- Skipped records: {len(batch['skipped'])}\n")
