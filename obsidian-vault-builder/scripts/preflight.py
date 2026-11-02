#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import platform
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.preflight import validate_scan_scope


def main() -> int:
    parser = argparse.ArgumentParser(description="FounderOS preflight check. No source scan is performed.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    print("Preflight")
    print(f"- OS: {platform.system()} {platform.release()}")
    print(f"- Home: {Path.home()}")
    print(f"- Current working directory: {Path.cwd()}")
    print(f"- Builder directory: {Path.cwd() if Path.cwd().name == 'obsidian-vault-builder' else Path.cwd() / 'obsidian-vault-builder'}")
    print(f"- Vault path: {config.vault_path}")
    print(f"- Vault exists: {config.vault_path.exists()}")
    print(f"- Network allowed: {config.allow_network}")
    print(f"- Online AI allowed: {config.allow_online_ai}")
    print(f"- Read file contents: {config.read_file_contents}")
    enabled_count = sum(1 for source in config.sources if source.get('enabled') is True)
    print(f"- Enabled sources: {enabled_count}")
    print("")
    print("No source folders were scanned by preflight.")
    if enabled_count:
        print("Gate A source selection is present. Dry-run will only use enabled sources.")
    else:
        print("Gate A remains pending until config/sources.yaml is confirmed.")
    result = validate_scan_scope(config)
    for warning in result.warnings:
        print(f"Warning: {warning}")
    if not result.ok:
        print("")
        print("Blocked by safety preflight:")
        for error in result.errors:
            print(f"- {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
