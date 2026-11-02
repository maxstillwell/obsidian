#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.strategy_outputs import write_strategy_outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate managed FounderOS strategy decisions, SEO briefs, and workflows.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    written = write_strategy_outputs(config)
    print(f"Generated strategy outputs in {config.vault_path}. Updated files: {len(written)}")
    for path in written:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
