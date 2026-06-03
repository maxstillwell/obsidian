#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.importer import create_import_plan, execute_import, importable_records
from vault_builder.inventory import read_inventory


def main() -> int:
    parser = argparse.ArgumentParser(description="Import planner and gated metadata-note importer.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--inventory", default="data/inventory.csv")
    parser.add_argument("--state", default="data/import_state.json")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirmed", action="store_true", help="Required for non-empty execute after Gate C approval.")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    records = read_inventory(Path(args.inventory))
    if args.plan_only or not args.execute:
        plan = create_import_plan(records, config)
        print("Import plan-only")
        print(f"- Vault: {config.vault_path}")
        print(f"- Inventory records: {len(records)}")
        print(f"- Wrote: {plan}")
        print("- Originals will not be deleted, moved, renamed, or overwritten.")
        return 0
    if args.execute:
        importable = importable_records(records)
        if importable and not args.confirmed:
            print("Blocked: non-empty import requires --confirmed after Gate C approval.")
            print(f"- Importable records: {len(importable)}")
            return 2
        batch = execute_import(records, config, state_path=Path(args.state))
        print("Import executed for importable metadata/source-note records only.")
        print(f"- Batch: {batch['batch_id']}")
        print(f"- Created files: {len(batch['created_files'])}")
        print(f"- Skipped records: {len(batch['skipped'])}")
        print("- Originals were not deleted, moved, renamed, or overwritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
