#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.obsidian_visibility import ensure_obsidian_visibility


def main() -> int:
    parser = argparse.ArgumentParser(description="Ensure FounderOS is visible from the current Obsidian vault and optionally registered as a standalone vault.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--register", action="store_true", help="Register the configured vault in Obsidian's local vault registry.")
    parser.add_argument("--registry", default=None, help="Override Obsidian registry path for testing or advanced use.")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    result = ensure_obsidian_visibility(
        config,
        register=args.register,
        registry_path=Path(args.registry).expanduser() if args.registry else None,
    )
    print(f"Ensured Obsidian visibility for {config.vault_path}. Updated files: {len(result.written)}")
    for path in result.written:
        print(f"- {path}")
    if args.register:
        print(f"Registry: {result.registry_path}")
        print(f"Registered new vault entry: {result.registered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
