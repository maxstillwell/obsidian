#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.final_report import current_imported_note_count, write_final_report
from vault_builder.gates import write_gate_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate FounderOS final/current-state report.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--inventory-json", default="data/inventory.json")
    parser.add_argument("--state", default="data/import_state.json")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    inventory = json.loads(Path(args.inventory_json).read_text(encoding="utf-8")) if Path(args.inventory_json).exists() else []
    state = json.loads(Path(args.state).read_text(encoding="utf-8")) if Path(args.state).exists() else {"batches": []}
    imported_count = current_imported_note_count(state)
    report = write_final_report(config, inventory_count=len(inventory), imported_count=imported_count)
    gate_status = write_gate_status(config, inventory_count=len(inventory), imported_count=imported_count)
    print(f"Wrote final report: {report}")
    print(f"Wrote gate status: {gate_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
