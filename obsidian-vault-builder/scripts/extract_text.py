#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401
from vault_builder.inventory import read_inventory, write_inventory
from vault_builder.processing import extract_text_file
from vault_builder.sanitize import sanitize_filename


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text for inventory rows that explicitly allow content reading.")
    parser.add_argument("--inventory", default="data/inventory.csv")
    parser.add_argument("--json", default="data/inventory.json")
    parser.add_argument("--output-dir", default="data/extracted_text")
    parser.add_argument("--max-chars", type=int, default=12000)
    args = parser.parse_args()

    records = read_inventory(Path(args.inventory))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted = 0
    skipped = 0
    for record in records:
        if not _as_bool(record.get("can_read_content")):
            skipped += 1
            continue
        source = Path(record.get("original_path", "")).expanduser()
        result = extract_text_file(source, max_chars=args.max_chars)
        if result.text:
            out = output_dir / sanitize_filename(f"{record.get('id', source.stem)}.txt")
            out.write_text(result.text, encoding="utf-8")
            record["extracted_text_path"] = str(out)
            record["import_reason"] = (record.get("import_reason") or "") + ("; extracted text truncated" if result.truncated else "; extracted text")
            extracted += 1
        elif result.error:
            record["error"] = result.error
            skipped += 1
    write_inventory(records, Path(args.inventory), Path(args.json))
    print(f"Extracted text records: {extracted}")
    print(f"Skipped records: {skipped}")
    return 0


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


if __name__ == "__main__":
    raise SystemExit(main())
