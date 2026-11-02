#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.completion_audit import write_completion_audit
from vault_builder.config import load_config
from vault_builder.inventory import read_inventory


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the FounderOS completion audit.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--inventory", default="data/inventory.csv")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    records = read_inventory(Path(args.inventory))
    output = write_completion_audit(config, records, builder_root=Path.cwd())
    print(f"Wrote completion audit: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
