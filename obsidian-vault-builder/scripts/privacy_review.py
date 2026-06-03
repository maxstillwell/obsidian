#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.inventory import read_inventory
from vault_builder.reports import write_privacy_review


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate privacy review from inventory metadata.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--inventory", default="data/inventory.csv")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    rows = read_inventory(Path(args.inventory))
    output = write_privacy_review(rows, config, Path(args.output) if args.output else None)
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
