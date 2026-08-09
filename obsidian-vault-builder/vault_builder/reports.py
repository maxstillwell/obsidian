from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


def write_scan_report(records: list[dict], config: BuilderConfig, output: Path | None = None) -> Path:
    output = output or safe_join(config.vault_path, "_System/SCAN_REPORT.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    enabled = [source for source in config.sources if source.get("enabled") is True]
    by_type = Counter(record.get("guessed_type", "unknown") or "unknown" for record in records)
    skipped = [record for record in records if record.get("import_action") == "skip"]
    errors = [record for record in records if record.get("error")]
    large = [record for record in records if str(record.get("import_reason", "")).lower().find("large") >= 0]

    lines = [
        "# SCAN_REPORT",
        "",
        "## Status",
        "",
        "Dry-run scan completed. No import was executed.",
        "",
        "## Scan Time",
        "",
        f"- {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Scan Sources",
        "",
    ]
    for source in enabled:
        lines.append(f"- {source.get('name')}: `{source.get('path_or_url')}` ({source.get('type')})")
    if not enabled:
        lines.append("- No enabled sources.")
    lines.extend(
        [
            "",
            "## Counts",
            "",
            f"- Files or URL records: {len(records)}",
            f"- Skipped records: {len(skipped)}",
            f"- Error records: {len(errors)}",
            f"- Large records: {len(large)}",
            "",
            "## File Type Distribution",
            "",
        ]
    )
    if by_type:
        for key, value in sorted(by_type.items()):
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No records.")
    lines.extend(["", "## Errors", ""])
    if errors:
        for record in errors[:100]:
            lines.append(f"- `{record.get('original_path')}`: {record.get('error')}")
    else:
        lines.append("- None.")
    lines.extend(["", "## Next Step", "", "Review `_System/PRIVACY_REVIEW.md`, then confirm Gate B before import planning."])
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def write_manual_review(records: list[dict], config: BuilderConfig, output: Path | None = None) -> Path:
    output = output or safe_join(config.vault_path, "_System/MANUAL_REVIEW.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    manual = [record for record in records if bool(record.get("needs_manual_review"))]
    lines = [
        "# MANUAL_REVIEW",
        "",
        "## Status",
        "",
        f"- Manual review records: {len(manual)}",
        "",
        "## Queue",
        "",
    ]
    if manual:
        for record in manual[:200]:
            label = record.get("source_url") or record.get("original_path")
            detail = record.get("page_title") or record.get("filename") or ""
            status = record.get("http_status") or ""
            status_part = f" status={status}" if status else ""
            lines.append(f"- `{label}`{status_part}: {detail} - {record.get('import_reason')}")
        if len(manual) > 200:
            lines.append(f"- Truncated: {len(manual) - 200} additional records not shown.")
    else:
        lines.append("- None.")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def write_privacy_review(records: list[dict], config: BuilderConfig, output: Path | None = None) -> Path:
    target = output or safe_join(config.vault_path, "_System/PRIVACY_REVIEW.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter(record.get("pii_risk", "unknown") or "unknown" for record in records)
    manual = [record for record in records if _as_bool(record.get("needs_manual_review"))]
    critical = [record for record in records if str(record.get("pii_risk", "")).lower() == "critical"]
    high = [record for record in records if str(record.get("pii_risk", "")).lower() == "high"]
    secret_like = [record for record in records if _as_bool(record.get("secret_risk"))]
    skipped = [record for record in records if str(record.get("import_action") or "") == "skip"]

    lines = [
        "# PRIVACY_REVIEW",
        "",
        "## Summary",
        "",
        f"- Inventory rows: {len(records)}",
        f"- Manual review rows: {len(manual)}",
        f"- Critical rows: {len(critical)}",
        f"- High risk rows: {len(high)}",
        f"- Secret-like rows: {len(secret_like)}",
        f"- Skipped rows: {len(skipped)}",
        "",
        "## Risk Counts",
        "",
    ]
    for level in ("critical", "high", "medium", "low", "unknown"):
        lines.append(f"- {level}: {counts.get(level, 0)}")
    lines.extend(["", "## Critical Files", ""])
    _append_record_lines(lines, critical)
    lines.extend(["", "## High Risk Files", ""])
    _append_record_lines(lines, high)
    lines.extend(["", "## Secret-Like Files", ""])
    _append_record_lines(lines, secret_like)
    lines.extend(["", "## Skipped Files", ""])
    _append_record_lines(lines, skipped)
    lines.extend(["", "## Manual Review", ""])
    _append_record_lines(lines, manual)

    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def _append_record_lines(lines: list[str], records: list[dict], limit: int = 200) -> None:
    if not records:
        lines.append("- None.")
        return
    for record in records[:limit]:
        label = record.get("source_url") or record.get("original_path") or record.get("filename") or record.get("id") or ""
        lines.append(f"- `{label}`: {record.get('import_reason', '')}")
    if len(records) > limit:
        lines.append(f"- Truncated: {len(records) - limit} additional rows not shown.")


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y"}
