from __future__ import annotations

from pathlib import Path
import re


INVALID_FILENAME_CHARS = r'<>:"/\\|?*'
CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f]")


def sanitize_filename(name: str, max_length: int = 120) -> str:
    cleaned = CONTROL_CHARS_RE.sub("", name.strip())
    cleaned = "".join("-" if char in INVALID_FILENAME_CHARS else char for char in cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip(" .-")
    if not cleaned:
        cleaned = "untitled"
    path = Path(cleaned)
    suffix = "".join(path.suffixes)
    if suffix:
        stem = cleaned[: -len(suffix)].strip(" .-")
        cleaned = f"{stem or 'untitled'}{suffix}"
    if len(cleaned) <= max_length:
        return cleaned
    path = Path(cleaned)
    suffix = "".join(path.suffixes)
    stem = cleaned[: -len(suffix)] if suffix else cleaned
    keep = max(1, max_length - len(suffix))
    return f"{stem[:keep].rstrip()}{suffix}"


def unique_filename(name: str, existing: set[str], content_hash: str = "") -> str:
    safe = sanitize_filename(name)
    existing_folded = {item.casefold() for item in existing}
    if safe.casefold() not in existing_folded:
        return safe
    digest = (content_hash or "duplicate")[:8]
    path = Path(safe)
    suffix = "".join(path.suffixes)
    stem = safe[: -len(suffix)] if suffix else safe
    return sanitize_filename(f"{stem}-{digest}{suffix}")


def safe_join(base: Path | str, *parts: str) -> Path:
    base_path = Path(base).expanduser().resolve()
    candidate = base_path.joinpath(*parts).resolve()
    try:
        candidate.relative_to(base_path)
    except ValueError as exc:
        raise ValueError(f"Refusing to write outside base path: {candidate}") from exc
    return candidate
