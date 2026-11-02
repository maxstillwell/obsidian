#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.vault_writer import create_vault


parser = argparse.ArgumentParser(description="Regenerate missing context pack scaffold files.")
parser.add_argument("--config", default="config/sources.yaml")
parser.add_argument("--vault", default=None)
args = parser.parse_args()
config = load_config(args.config)
vault = Path(args.vault).expanduser() if args.vault else config.vault_path
result = create_vault(vault)
print(f"Ensured context pack scaffold in {result.vault_path}. Created files: {len(result.created_files)}")
