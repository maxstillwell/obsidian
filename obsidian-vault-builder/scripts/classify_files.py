#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.inventory import read_inventory, write_inventory
from vault_builder.processing import classify_inventory_records


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify inventory records by filename/path/source metadata.")
    parser.add_argument("--inventory", default="data/inventory.csv")
    parser.add_argument("--json", default="data/inventory.json")
    args = parser.parse_args()

    records = read_inventory(Path(args.inventory))
    updated = classify_inventory_records(records)
    write_inventory(updated, Path(args.inventory), Path(args.json))
    print(f"Classified records: {len(updated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
