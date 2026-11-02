from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import BuilderConfig


REQUIRED_BROAD_SCAN_EXCLUDES = {
    "Library",
    ".ssh",
    ".gnupg",
    ".1password",
    ".Trash",
    "Mail",
    "Messages",
    "Keychains",
    "Application Support",
    ".codex",
    ".claude",
    ".claudian",
    ".gemini",
    ".antigravity",
    ".antigravity_cockpit",
    "codex_home",
    "User Data",
}


@dataclass(frozen=True)
class PreflightResult:
    ok: bool
    errors: list[str]
    warnings: list[str]


def validate_scan_scope(config: BuilderConfig) -> PreflightResult:
    errors: list[str] = []
    warnings: list[str] = []
    enabled_sources = [source for source in config.sources if source.get("enabled") is True]

    if config.allow_online_ai:
        errors.append("Online AI must be disabled for broad local scans.")
    if config.allow_ocr:
        errors.append("OCR must be disabled for broad local scans.")
    if config.allow_transcription:
        errors.append("Transcription must be disabled for broad local scans.")

    broad_sources = [source for source in enabled_sources if _is_broad_local_source(source)]
    if broad_sources:
        if not config.dry_run:
            errors.append("Broad local scans must run with dry_run: true.")
        if config.read_file_contents:
            errors.append("Broad local scans must keep read_file_contents: false.")
        if config.copy_attachments:
            errors.append("Broad local scans must keep copy_attachments: false.")
        missing = sorted(REQUIRED_BROAD_SCAN_EXCLUDES - set(config.exclude_dirs))
        if missing:
            errors.append(f"Broad local scans must exclude sensitive directories: {', '.join(missing)}.")
        warnings.append("Broad local scan is metadata-only: filenames, paths, sizes, and timestamps may still be sensitive.")

    return PreflightResult(ok=not errors, errors=errors, warnings=warnings)


def _is_broad_local_source(source: dict) -> bool:
    if source.get("type") != "folder":
        return False
    path_text = str(source.get("path_or_url") or "").strip()
    if path_text in {"/", "~", "$HOME"}:
        return True
    try:
        path = Path(path_text).expanduser().resolve()
    except OSError:
        return False
    home = Path.home().resolve()
    return path == home or path == Path("/").resolve()
