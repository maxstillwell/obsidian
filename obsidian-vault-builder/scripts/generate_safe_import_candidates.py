#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.safe_import_candidates import load_records, write_safe_import_candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local safe-import candidate report from full-home metadata inventory.")
    parser.add_argument("--inventory-json", default="data/full_home_inventory.json")
    parser.add_argument("--output", default="../FounderOS/_System/SAFE_IMPORT_CANDIDATES.md")
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--max-groups", type=int, default=50)
    args = parser.parse_args()

    records = load_records(Path(args.inventory_json))
    output = write_safe_import_candidates(
        records,
        Path(args.output),
        home_path=Path(args.home),
        max_groups=args.max_groups,
    )
    print(f"Generated safe import candidates: {output}")
    print(f"- Full-home inventory records reviewed: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
