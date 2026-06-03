#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.inventory import write_inventory
from vault_builder.reports import write_manual_review, write_privacy_review, write_scan_report
from vault_builder.scanner import dry_run_scan


def append_scan_log(message: str) -> None:
    log_path = Path("logs/scan.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{datetime.now().isoformat(timespec='seconds')} {message}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run source scanner. Reads metadata for enabled sources only.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--dry-run", action="store_true", default=True)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    enabled = [source for source in config.sources if source.get("enabled") is True]
    if not enabled:
        print("No sources are enabled in config/sources.yaml.")
        print("Gate A is pending. Nothing was scanned.")
        write_inventory([], Path("data/inventory.csv"), Path("data/inventory.json"))
        write_scan_report([], config)
        write_privacy_review([], config)
        write_manual_review([], config)
        append_scan_log("dry_run enabled_sources=0 records=0 read_file_contents=false allow_network=false")
        return 0

    print("Dry-run scan plan")
    print("- Reads enabled source metadata only.")
    print(f"- Read file contents: {config.read_file_contents}")
    print(f"- Network allowed: {config.allow_network}")
    print(f"- Online AI allowed: {config.allow_online_ai}")
    print("- Writes: data/inventory.csv, data/inventory.json, and vault _System dry-run reports")
    print("- Does not create imported notes or attachments.")
    records = dry_run_scan(config)
    write_inventory(records, Path("data/inventory.csv"), Path("data/inventory.json"))
    scan_report = write_scan_report(records, config)
    privacy_review = write_privacy_review(records, config)
    manual_review = write_manual_review(records, config)
    print(f"Dry-run records: {len(records)}")
    print(f"Wrote scan report: {scan_report}")
    print(f"Wrote privacy review: {privacy_review}")
    print(f"Wrote manual review: {manual_review}")
    append_scan_log(
        "dry_run "
        f"enabled_sources={len(enabled)} records={len(records)} "
        f"read_file_contents={str(config.read_file_contents).lower()} "
        f"allow_network={str(config.allow_network).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
