#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.completion_outputs import write_completion_outputs
from vault_builder.config import load_config


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate FounderOS operating manual and setup-complete outputs.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--inventory-json", default="data/inventory.json")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    inventory_path = Path(args.inventory_json)
    records = json.loads(inventory_path.read_text(encoding="utf-8")) if inventory_path.exists() else []
    source_count = sum(1 for path in (config.vault_path / "60 Resources").rglob("*.md") if "type: source" in path.read_text(encoding="utf-8", errors="ignore")[:400])
    manual_review_count = sum(1 for record in records if _as_bool(record.get("needs_manual_review")))
    written = write_completion_outputs(
        config,
        inventory_count=len(records),
        source_count=source_count,
        manual_review_count=manual_review_count,
    )
    print(f"Generated completion outputs in {config.vault_path}. Updated files: {len(written)}")
    for path in written:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
