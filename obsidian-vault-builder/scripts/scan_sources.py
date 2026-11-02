#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.inventory import write_inventory
from vault_builder.preflight import validate_scan_scope
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
    parser.add_argument("--inventory", default="data/inventory.csv")
    parser.add_argument("--inventory-json", default="data/inventory.json")
    parser.add_argument("--scan-report", default=None)
    parser.add_argument("--privacy-output", default=None)
    parser.add_argument("--manual-output", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    preflight = validate_scan_scope(config)
    for warning in preflight.warnings:
        print(f"Warning: {warning}")
    if not preflight.ok:
        print("Blocked by safety preflight:")
        for error in preflight.errors:
            print(f"- {error}")
        return 2
    enabled = [source for source in config.sources if source.get("enabled") is True]
    if not enabled:
        print("No sources are enabled in config/sources.yaml.")
        print("Gate A is pending. Nothing was scanned.")
        write_inventory([], Path(args.inventory), Path(args.inventory_json))
        write_scan_report([], config, Path(args.scan_report) if args.scan_report else None)
        write_privacy_review([], config, Path(args.privacy_output) if args.privacy_output else None)
        write_manual_review([], config, Path(args.manual_output) if args.manual_output else None)
        append_scan_log("dry_run enabled_sources=0 records=0 read_file_contents=false allow_network=false")
        return 0

    print("Dry-run scan plan")
    print("- Reads enabled source metadata only.")
    print(f"- Read file contents: {config.read_file_contents}")
    print(f"- Network allowed: {config.allow_network}")
    print(f"- Online AI allowed: {config.allow_online_ai}")
    print(f"- Writes inventory: {args.inventory}, {args.inventory_json}")
    print("- Does not create imported notes or attachments.")
    records = dry_run_scan(config)
    write_inventory(records, Path(args.inventory), Path(args.inventory_json))
    scan_report = write_scan_report(records, config, Path(args.scan_report) if args.scan_report else None)
    privacy_review = write_privacy_review(records, config, Path(args.privacy_output) if args.privacy_output else None)
    manual_review = write_manual_review(records, config, Path(args.manual_output) if args.manual_output else None)
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
