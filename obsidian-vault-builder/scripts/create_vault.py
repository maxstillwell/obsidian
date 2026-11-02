#!/usr/bin/env python3
from __future__ import annotations

import argparse

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.vault_writer import create_vault


def main() -> int:
    parser = argparse.ArgumentParser(description="Create FounderOS vault structure without scanning sources.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None, help="Override vault path for placing the scaffold in another Obsidian vault.")
    args = parser.parse_args()

    config = load_config(args.config)
    result = create_vault(args.vault or config.vault_path)
    print(f"Vault path: {result.vault_path}")
    print(f"Created directories: {len(result.created_dirs)}")
    print(f"Created files: {len(result.created_files)}")
    print(f"Skipped existing files: {len(result.skipped_files)}")
    print("No source folders were scanned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
