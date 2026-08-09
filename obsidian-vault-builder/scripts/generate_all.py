#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.completion_audit import write_completion_audit
from vault_builder.completion_outputs import write_completion_outputs
from vault_builder.config import load_config
from vault_builder.daily_operating_layer import write_daily_operating_layer
from vault_builder.dedupe import duplicate_summary, mark_duplicates
from vault_builder.docmind_execution_pack import write_docmind_execution_pack
from vault_builder.final_report import current_imported_note_count, write_final_report
from vault_builder.gates import write_gate_status
from vault_builder.gtm_operating_panel import write_gtm_operating_panel
from vault_builder.importer import create_import_plan, execute_import, importable_records
from vault_builder.inventory import read_inventory, write_inventory
from vault_builder.obsidian_app_config import configure_obsidian_ui
from vault_builder.obsidian_visibility import ensure_obsidian_visibility
from vault_builder.public_workbench import write_public_workbench
from vault_builder.reports import write_manual_review, write_privacy_review, write_scan_report
from vault_builder.sanitize import safe_join
from vault_builder.scanner import dry_run_scan
from vault_builder.source_indexes import write_source_indexes
from vault_builder.strategy_outputs import write_strategy_outputs
from vault_builder.vault_writer import create_vault


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the safe FounderOS regeneration pipeline.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--inventory", default="data/inventory.csv")
    parser.add_argument("--inventory-json", default="data/inventory.json")
    parser.add_argument("--state", default="data/import_state.json")
    parser.add_argument("--refresh-scan", action="store_true", help="Refresh enabled-source dry-run inventory. May use network if config allows it.")
    parser.add_argument("--execute-import", action="store_true", help="Create missing import notes from the current import plan.")
    parser.add_argument("--confirmed", action="store_true", help="Required with --execute-import when there are importable records.")
    args = parser.parse_args()

    builder_root = Path(__file__).resolve().parents[1]
    os.chdir(builder_root)

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()

    created = create_vault(config.vault_path)
    print(f"Ensured vault scaffold: {created.vault_path}")

    inventory_path = Path(args.inventory)
    inventory_json_path = Path(args.inventory_json)
    if args.refresh_scan:
        records = dry_run_scan(config)
        write_inventory(records, inventory_path, inventory_json_path)
        write_scan_report(records, config)
        print(f"Refreshed dry-run inventory records: {len(records)}")
    else:
        records = read_inventory(inventory_path)
        write_scan_report(records, config)
        print(f"Using existing inventory records: {len(records)}")

    records = mark_duplicates(records)
    write_inventory(records, inventory_path, inventory_json_path)
    write_dedupe_report(config, records)
    write_privacy_review(records, config)
    write_manual_review(records, config)
    create_import_plan(records, config)

    if args.execute_import:
        importable = importable_records(records)
        if importable and not args.confirmed:
            print("Blocked: --execute-import requires --confirmed when importable records exist.")
            print(f"- Importable records: {len(importable)}")
            return 2
        batch = execute_import(records, config, state_path=Path(args.state))
        print(f"Executed import batch: {batch['batch_id']} created={len(batch['created_files'])} skipped={len(batch['skipped'])}")
    else:
        print("Import execution skipped. Use --execute-import --confirmed after Gate C when needed.")

    write_source_indexes(config)
    write_strategy_outputs(config)
    write_public_workbench(config)
    write_docmind_execution_pack(config)
    write_gtm_operating_panel(config)
    write_daily_operating_layer(config)
    ensure_obsidian_visibility(config)
    configure_obsidian_ui(config)

    inventory_count = len(records)
    source_count = source_note_count(config)
    manual_count = manual_review_count(records)
    write_completion_outputs(config, inventory_count=inventory_count, source_count=source_count, manual_review_count=manual_count)

    state = load_state(Path(args.state))
    imported_count = current_imported_note_count(state)
    write_final_report(config, inventory_count=inventory_count, imported_count=imported_count)
    write_gate_status(config, inventory_count=inventory_count, imported_count=imported_count)
    audit = write_completion_audit(config, records, builder_root=builder_root)
    print(f"Wrote completion audit: {audit}")
    return 0


def write_dedupe_report(config, records: list[dict]) -> Path:
    summary = duplicate_summary(records)
    report = safe_join(config.vault_path, "_System/DEDUPE_REPORT.md")
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DEDUPE_REPORT",
        "",
        "## Summary",
        "",
        f"- Inventory records: {len(records)}",
        f"- Duplicate records: {sum(summary.values())}",
        "",
        "## Duplicate Groups",
        "",
    ]
    if summary:
        for target, count in summary.items():
            lines.append(f"- `{target}`: {count} duplicate(s)")
    else:
        lines.append("- None.")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def source_note_count(config) -> int:
    root = safe_join(config.vault_path, "60 Resources")
    if not root.exists():
        return 0
    count = 0
    for path in root.rglob("*.md"):
        try:
            if "type: source" in path.read_text(encoding="utf-8", errors="ignore")[:500]:
                count += 1
        except OSError:
            continue
    return count


def manual_review_count(records: list[dict]) -> int:
    return sum(1 for record in records if as_bool(record.get("needs_manual_review")))


def as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"batches": [], "last_batch_id": None}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"batches": [], "last_batch_id": None}


if __name__ == "__main__":
    raise SystemExit(main())
