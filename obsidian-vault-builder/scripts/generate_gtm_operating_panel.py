#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.gtm_operating_panel import write_gtm_operating_panel


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the DocMind GTM operating panel.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    written = write_gtm_operating_panel(config)
    print(f"Generated DocMind GTM operating panel in {config.vault_path}. Updated files: {len(written)}")
    for path in written:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
