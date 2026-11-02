#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.importer import rollback_batch


def main() -> int:
    parser = argparse.ArgumentParser(description="Rollback generated import batches only.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--state", default="data/import_state.json")
    parser.add_argument("--batch-id", default=None)
    parser.add_argument("--last", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    removed = rollback_batch(config, state_path=Path(args.state), batch_id=args.batch_id)
    print(f"Removed generated files: {len(removed)}")
    print("Original files were not touched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
