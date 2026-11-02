from __future__ import annotations

from datetime import datetime

from .config import BuilderConfig
from .sanitize import safe_join


def current_imported_note_count(state: dict) -> int:
    return sum(
        len(batch.get("created_files", []))
        for batch in state.get("batches", [])
        if not batch.get("rolled_back_at")
    )


def write_final_report(config: BuilderConfig, inventory_count: int, imported_count: int) -> object:
    output = safe_join(config.vault_path, "_System/FINAL_REPORT.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    enabled = [source.get("name", "") for source in config.sources if source.get("enabled") is True]
    next_steps = _next_steps(config, imported_count)
    lines = [
        "# Final Report",
        "",
        "## Generated At",
        "",
        f"- {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Current Sources",
        "",
    ]
    if enabled:
        lines.extend(f"- {name}" for name in enabled)
    else:
        lines.append("- None enabled.")
    lines.extend(
        [
            "",
            "## Counts",
            "",
            f"- Inventory records: {inventory_count}",
            f"- Imported notes: {imported_count}",
            "",
            "## Safety State",
            "",
            f"- Network allowed: {config.allow_network}",
            f"- Online AI allowed: {config.allow_online_ai}",
            f"- Read file contents: {config.read_file_contents}",
            "- Originals are not deleted, moved, renamed, or overwritten by this system.",
            "",
            "## Next Steps",
            "",
            *next_steps,
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def _next_steps(config: BuilderConfig, imported_count: int) -> list[str]:
    if imported_count and config.allow_network:
        return [
            "- Public URL source phase is active and current importable public records have been imported.",
            "- Private/local folders remain disabled until a separate folder-specific plan is approved.",
            "- Manual review queue remains available in `_System/MANUAL_REVIEW.md`.",
        ]
    return [
        "- Add a small approved source or URLs, then run dry-run.",
        "- Review scan and privacy reports before import planning.",
        "- Confirm Gate C before executing imports.",
    ]
