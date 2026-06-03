#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.obsidian_app_config import configure_obsidian_ui


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure FounderOS Obsidian bookmarks, daily notes, and templates.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()

    result = configure_obsidian_ui(config)
    print(f"Configured Obsidian UI for {config.vault_path}. Updated files: {len(result.written)}")
    for path in result.written:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
