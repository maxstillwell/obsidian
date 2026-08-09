from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from pathlib import Path
import mimetypes
import os
import uuid

from .classification import classify_metadata
from .config import BuilderConfig
from .privacy import assess_privacy
from .web_metadata import fetch_url_metadata


EXTENSION_ACTIONS = {
    ".md": "convert_to_note",
    ".txt": "convert_to_note",
    ".pdf": "extract_text_to_note",
    ".docx": "extract_text_to_note",
    ".pptx": "summary_note",
    ".xlsx": "metadata_note",
    ".csv": "metadata_note",
    ".html": "convert_to_note",
    ".htm": "convert_to_note",
    ".png": "index_only",
    ".jpg": "index_only",
    ".jpeg": "index_only",
    ".gif": "index_only",
    ".webp": "index_only",
    ".mp3": "index_only",
    ".wav": "index_only",
    ".mp4": "index_only",
    ".mov": "index_only",
}


def _iso_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _enabled_sources(config: BuilderConfig) -> list[dict]:
    return [source for source in config.sources if source.get("enabled") is True]


def _should_skip_dir(dirname: str, config: BuilderConfig) -> bool:
    return dirname in config.exclude_dirs


def dry_run_scan(config: BuilderConfig) -> list[dict]:
    records: list[dict] = []
    max_size = config.max_file_size_mb * 1024 * 1024

    for source in _enabled_sources(config):
        source_type = source.get("type")
        if source_type == "url_list":
            records.extend(_scan_url_list(source, config))
            continue
        if source_type == "file":
            path = Path(source["path_or_url"]).expanduser()
            if not path.is_absolute():
                path = Path.cwd() / path
            if not path.exists():
                records.append(_error_record(source, path, "Source file does not exist"))
                continue
            records.append(_file_record(source, path, config, max_size))
            continue
        if source_type != "folder":
            records.append(_error_record(source, Path(str(source.get("path_or_url", ""))), f"Unsupported source type: {source_type}"))
            continue
        root = Path(source["path_or_url"]).expanduser()
        if not root.exists():
            records.append(_error_record(source, root, "Source path does not exist"))
            continue
        for current_root, dirnames, filenames in os.walk(root, followlinks=False):
            dirnames[:] = [dirname for dirname in dirnames if not _should_skip_dir(dirname, config)]
            for filename in filenames:
                path = Path(current_root) / filename
                records.append(_file_record(source, path, config, max_size))
    return records


def _file_record(source: dict, path: Path, config: BuilderConfig, max_size: int) -> dict:
    try:
        stat = path.stat()
    except OSError as exc:
        return _error_record(source, path, str(exc))
    extension = path.suffix.lower()
    privacy = assess_privacy(str(path), source.get("privacy_level"))
    classification = classify_metadata(str(path), source.get("name", ""))
    too_large = stat.st_size > max_size
    action = privacy.import_action
    if action == "metadata_note":
        action = EXTENSION_ACTIONS.get(extension, "needs_review")
    if too_large:
        action = "index_only"
    can_read_content = bool(config.read_file_contents and not privacy.needs_manual_review and not too_large)
    return {
        "id": str(uuid.uuid5(uuid.NAMESPACE_URL, str(path))),
        "original_path": str(path),
        "filename": path.name,
        "extension": extension,
        "size_bytes": stat.st_size,
        "created_time": _iso_timestamp(stat.st_ctime),
        "modified_time": _iso_timestamp(stat.st_mtime),
        "hash": _sha256_file(path) if can_read_content else "",
        "source_name": source.get("name", ""),
        "source_type": source.get("type", ""),
        "guessed_type": _guess_type(extension),
        "mime_guess": mimetypes.guess_type(str(path))[0] or "",
        "suggested_area": classification.area,
        "suggested_project": classification.project,
        "suggested_destination": source.get("destination", ""),
        "pii_risk": privacy.level,
        "secret_risk": privacy.secret_risk,
        "import_action": action,
        "import_reason": privacy.reason if privacy.needs_manual_review else classification.reason,
        "needs_manual_review": privacy.needs_manual_review or classification.confidence == "low" or too_large,
        "can_read_content": can_read_content,
        "extracted_text_path": "",
        "obsidian_note_path": "",
        "attachment_path": "",
        "source_url": "",
        "http_status": "",
        "content_type": "",
        "page_title": "",
        "error": "",
    }


def _scan_url_list(source: dict, config: BuilderConfig) -> list[dict]:
    path = Path(source["path_or_url"]).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.exists():
        return [_error_record(source, path, "URL list file does not exist")]
    records = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return [_error_record(source, path, "URL list must be UTF-8 text")]
    for line in lines:
        url = line.strip()
        if not url or url.startswith("#"):
            continue
        classification = classify_metadata(url, source.get("name", ""))
        metadata = fetch_url_metadata(url, allow_network=config.allow_network)
        import_reason = "URL list dry-run; "
        if metadata.fetched:
            import_reason += f"fetched public metadata status={metadata.status_code}"
        else:
            import_reason += metadata.error or "no network metadata fetched"
        non_2xx = bool(metadata.status_code and not metadata.status_code.startswith("2"))
        needs_manual_review = classification.confidence == "low" or non_2xx
        records.append(
            {
                "id": str(uuid.uuid5(uuid.NAMESPACE_URL, url)),
                "original_path": str(path),
                "filename": path.name,
                "extension": path.suffix.lower(),
                "size_bytes": 0,
                "created_time": "",
                "modified_time": "",
                "hash": hashlib.sha256(url.encode("utf-8")).hexdigest(),
                "source_name": source.get("name", ""),
                "source_type": source.get("type", ""),
                "guessed_type": "url",
                "mime_guess": "",
                "suggested_area": classification.area,
                "suggested_project": classification.project,
                "suggested_destination": source.get("destination", ""),
                "pii_risk": source.get("privacy_level", "low"),
                "secret_risk": False,
                "import_action": "needs_review" if non_2xx else "metadata_note",
                "import_reason": import_reason,
                "needs_manual_review": needs_manual_review,
                "can_read_content": False,
                "extracted_text_path": "",
                "obsidian_note_path": "",
                "attachment_path": "",
                "source_url": url,
                "http_status": metadata.status_code,
                "content_type": metadata.content_type,
                "page_title": metadata.title,
                "error": "",
            }
        )
    return records


def _sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _guess_type(extension: str) -> str:
    if extension in {".md", ".txt"}:
        return "text"
    if extension == ".pdf":
        return "pdf"
    if extension in {".docx", ".pptx", ".xlsx", ".csv"}:
        return extension.lstrip(".")
    if extension in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        return "image"
    if extension in {".mp3", ".wav"}:
        return "audio"
    if extension in {".mp4", ".mov"}:
        return "video"
    return "unknown"


def _error_record(source: dict, path: Path, error: str) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "original_path": str(path),
        "filename": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": 0,
        "created_time": "",
        "modified_time": "",
        "hash": "",
        "source_name": source.get("name", ""),
        "source_type": source.get("type", ""),
        "guessed_type": "",
        "mime_guess": "",
        "suggested_area": "",
        "suggested_project": "",
        "suggested_destination": source.get("destination", ""),
        "pii_risk": "unknown",
        "secret_risk": False,
        "import_action": "skip",
        "import_reason": "Source error",
        "needs_manual_review": True,
        "can_read_content": False,
        "extracted_text_path": "",
        "obsidian_note_path": "",
        "attachment_path": "",
        "source_url": "",
        "http_status": "",
        "content_type": "",
        "page_title": "",
        "error": error,
    }
