#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.importer import execute_import, importable_records
from vault_builder.inventory import read_inventory


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Obsidian source notes from importable inventory records.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--inventory", default="data/inventory.csv")
    parser.add_argument("--state", default="data/import_state.json")
    parser.add_argument("--confirmed", action="store_true", help="Required when there are importable records.")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    records = read_inventory(Path(args.inventory))
    importable = importable_records(records)
    if importable and not args.confirmed:
        print("Blocked: creating notes requires --confirmed after Gate C approval.")
        print(f"- Importable records: {len(importable)}")
        return 2
    batch = execute_import(records, config, state_path=Path(args.state))
    print(f"Created notes: {len(batch['created_files'])}")
    print(f"Batch: {batch['batch_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
