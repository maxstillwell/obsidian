from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


def write_gate_status(config: BuilderConfig, inventory_count: int, imported_count: int) -> Path:
    output = safe_join(config.vault_path, "_System/GATE_STATUS.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    enabled = [source for source in config.sources if source.get("enabled") is True]
    gate_b_status = (
        "- Scan, privacy review, and import plan exist for the current enabled sources."
        if inventory_count and imported_count
        else "- Confirm before generating a detailed import plan for real records."
    )
    gate_c_status = (
        "- Current importable public-source records have been imported."
        if imported_count
        else "- Non-empty imports require explicit confirmation."
    )
    lines = [
        "# GATE_STATUS",
        "",
        "## Generated At",
        "",
        f"- {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Gate A: sources.yaml",
        "",
        f"- Enabled sources: {len(enabled)}",
    ]
    for source in enabled:
        lines.append(f"- {source.get('name')}: `{source.get('path_or_url')}`")
    lines.extend(
        [
            "",
            "## Gate B: scan report and privacy review",
            "",
            f"- Inventory records: {inventory_count}",
            gate_b_status,
            "",
            "## Gate C: import plan",
            "",
            f"- Imported notes: {imported_count}",
            gate_c_status,
            "",
            "## Gate D: online/network",
            "",
            f"- Network allowed: {config.allow_network}",
            f"- Online AI allowed: {config.allow_online_ai}",
            f"- Read file contents: {config.read_file_contents}",
            f"- OCR allowed: {config.allow_ocr}",
            f"- Transcription allowed: {config.allow_transcription}",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
