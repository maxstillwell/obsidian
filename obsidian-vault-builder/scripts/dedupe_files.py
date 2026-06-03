#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.config import load_config
from vault_builder.dedupe import duplicate_summary, mark_duplicates
from vault_builder.inventory import write_inventory, read_inventory
from vault_builder.sanitize import safe_join


def main() -> int:
    parser = argparse.ArgumentParser(description="Mark duplicate inventory records without deleting files.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--inventory", default="data/inventory.csv")
    parser.add_argument("--json", default="data/inventory.json")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.vault:
        config.vault_path = Path(args.vault).expanduser()
    records = read_inventory(Path(args.inventory))
    marked = mark_duplicates(records)
    write_inventory(marked, Path(args.inventory), Path(args.json))
    summary = duplicate_summary(marked)
    report = safe_join(config.vault_path, "_System/DEDUPE_REPORT.md")
    lines = [
        "# DEDUPE_REPORT",
        "",
        "## Summary",
        "",
        f"- Inventory records: {len(marked)}",
        f"- Duplicate records: {sum(summary.values())}",
        "",
        "## Duplicate Groups",
        "",
    ]
    if summary:
        for target, count in summary.items():
            lines.append(f"- `{target}`: {count} duplicate(s)")
    else:
        lines.append("- None.")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Marked duplicates: {sum(summary.values())}")
    print(f"Wrote report: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
