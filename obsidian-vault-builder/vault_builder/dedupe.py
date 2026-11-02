from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
import re


FILENAME_SIMILARITY_THRESHOLD = 0.9
SUMMARY_SIMILARITY_THRESHOLD = 0.88
SIZE_RATIO_TOLERANCE = 0.03
MTIME_TOLERANCE_SECONDS = 120


def mark_duplicates(records: list[dict]) -> list[dict]:
    """Mark likely duplicates without deleting original files or generated notes."""
    result = [deepcopy(record) for record in records]
    seen_hash: dict[str, str] = {}
    seen_url: dict[str, str] = {}
    title_buckets: defaultdict[str, list[dict]] = defaultdict(list)
    filename_buckets: defaultdict[str, list[dict]] = defaultdict(list)

    for record in result:
        record.setdefault("duplicate_of", "")
        record_id = str(record.get("id") or "")
        file_hash = str(record.get("hash") or "")
        source_url = _normalize_url(str(record.get("source_url") or ""))
        if file_hash:
            if file_hash in seen_hash:
                record["duplicate_of"] = seen_hash[file_hash]
                _add_candidate(record, title_buckets, filename_buckets)
                continue
            seen_hash[file_hash] = record_id
        if source_url:
            if source_url in seen_url:
                record["duplicate_of"] = seen_url[source_url]
                _add_candidate(record, title_buckets, filename_buckets)
                continue
            seen_url[source_url] = record_id
        for candidate in _candidate_records(record, title_buckets, filename_buckets):
            if _is_probable_duplicate(record, candidate):
                record["duplicate_of"] = str(candidate.get("id") or "")
                break
        _add_candidate(record, title_buckets, filename_buckets)
    return result


def duplicate_summary(records: list[dict]) -> dict[str, int]:
    by_target: defaultdict[str, int] = defaultdict(int)
    for record in records:
        duplicate_of = str(record.get("duplicate_of") or "")
        if duplicate_of:
            by_target[duplicate_of] += 1
    return dict(by_target)


def _is_probable_duplicate(record: dict, candidate: dict) -> bool:
    return _filename_size_mtime_match(record, candidate) or _title_summary_match(record, candidate)


def _candidate_records(
    record: dict,
    title_buckets: dict[str, list[dict]],
    filename_buckets: dict[str, list[dict]],
) -> list[dict]:
    candidates: list[dict] = []
    seen: set[int] = set()
    for bucket_key, buckets in (
        (_normalize_text(_title(record)), title_buckets),
        (_filename_bucket_key(record), filename_buckets),
    ):
        if not bucket_key:
            continue
        for candidate in buckets.get(bucket_key, []):
            marker = id(candidate)
            if marker not in seen:
                candidates.append(candidate)
                seen.add(marker)
    return candidates


def _add_candidate(record: dict, title_buckets: dict[str, list[dict]], filename_buckets: dict[str, list[dict]]) -> None:
    title_key = _normalize_text(_title(record))
    if title_key:
        title_buckets[title_key].append(record)
    filename_key = _filename_bucket_key(record)
    if filename_key:
        filename_buckets[filename_key].append(record)


def _filename_bucket_key(record: dict) -> str:
    normalized = _normalize_filename(str(record.get("filename") or record.get("original_path") or ""))
    if not normalized:
        return ""
    return normalized[:16]


def _filename_size_mtime_match(record: dict, candidate: dict) -> bool:
    record_size = _int_value(record.get("size_bytes"))
    candidate_size = _int_value(candidate.get("size_bytes"))
    if record_size <= 0 or candidate_size <= 0:
        return False
    if not _sizes_close(record_size, candidate_size):
        return False
    record_time = _parse_time(record.get("modified_time"))
    candidate_time = _parse_time(candidate.get("modified_time"))
    if record_time is None or candidate_time is None:
        return False
    if abs((record_time - candidate_time).total_seconds()) > MTIME_TOLERANCE_SECONDS:
        return False
    record_name = _normalize_filename(str(record.get("filename") or record.get("original_path") or ""))
    candidate_name = _normalize_filename(str(candidate.get("filename") or candidate.get("original_path") or ""))
    if not record_name or not candidate_name:
        return False
    return _similarity(record_name, candidate_name) >= FILENAME_SIMILARITY_THRESHOLD


def _title_summary_match(record: dict, candidate: dict) -> bool:
    record_title = _normalize_text(_title(record))
    candidate_title = _normalize_text(_title(candidate))
    if not record_title or record_title != candidate_title:
        return False
    record_summary = _normalize_text(_summary(record))
    candidate_summary = _normalize_text(_summary(candidate))
    if len(record_summary) < 40 or len(candidate_summary) < 40:
        return False
    return _similarity(record_summary, candidate_summary) >= SUMMARY_SIMILARITY_THRESHOLD


def _title(record: dict) -> str:
    for key in ("title", "page_title", "filename"):
        value = str(record.get(key) or "").strip()
        if value:
            return value
    return ""


def _summary(record: dict) -> str:
    for key in ("content_summary", "summary", "abstract", "description", "import_reason"):
        value = str(record.get(key) or "").strip()
        if value:
            return value
    return ""


def _normalize_filename(value: str) -> str:
    name = Path(value).name if value else ""
    stem = Path(name).stem or name
    return _normalize_text(stem)


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _normalize_url(value: str) -> str:
    return value.strip().rstrip("/")


def _similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, left, right).ratio()


def _sizes_close(left: int, right: int) -> bool:
    larger = max(left, right)
    if larger <= 0:
        return False
    return abs(left - right) / larger <= SIZE_RATIO_TOLERANCE


def _int_value(value: object) -> int:
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return 0


def _parse_time(value: object) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None
