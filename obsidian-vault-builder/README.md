# Obsidian Vault Builder

Privacy-first scaffolding for the FounderOS Obsidian vault.

This setup creates systems, templates, configuration, dry-run tools, import reports, Obsidian Bases scaffolds, and public URL source notes. It does not scan Desktop, Documents, Downloads, cloud folders, email, browser data, chats, APIs, or private exports until `config/sources.yaml` is reviewed and explicitly confirmed.

## Safety Defaults

- Private/local folder sources are disabled by default.
- `dry_run: true`
- `read_file_contents: false`
- `allow_network: true` in the active config, limited to public URL metadata/source notes from `data/urls.txt`
- `allow_online_ai: false`
- `allow_ocr: false`
- `allow_transcription: false`
- Originals are never deleted, moved, renamed, or overwritten.

## Commands

```bash
python scripts/preflight.py --config config/sources.yaml
python scripts/create_vault.py --config config/sources.yaml
python scripts/scan_sources.py --config config/sources.yaml --dry-run
python scripts/privacy_review.py --config config/sources.yaml --inventory data/inventory.csv
python scripts/dedupe_files.py --config config/sources.yaml
python scripts/run_import.py --config config/sources.yaml --plan-only
python scripts/run_import.py --config config/sources.yaml --execute --confirmed
python scripts/generate_indexes.py --config config/sources.yaml
python scripts/generate_source_indexes.py --config config/sources.yaml
python scripts/generate_context_packs.py --config config/sources.yaml
python scripts/generate_bases.py --config config/sources.yaml
python scripts/generate_strategy_outputs.py --config config/sources.yaml
python scripts/generate_public_workbench.py --config config/sources.yaml
python scripts/generate_docmind_execution_pack.py --config config/sources.yaml
python scripts/generate_gtm_operating_panel.py --config config/sources.yaml
python scripts/generate_daily_operating_layer.py --config config/sources.yaml
python scripts/ensure_obsidian_visibility.py --config config/sources.yaml --register
python scripts/configure_obsidian_ui.py --config config/sources.yaml
python scripts/generate_completion_outputs.py --config config/sources.yaml
python scripts/generate_completion_audit.py --config config/sources.yaml
python scripts/report.py --config config/sources.yaml
python scripts/rollback_import.py --last
```

`--execute` import is intentionally guarded by `--confirmed`. It should only be used after Gate A, Gate B, and Gate C are reviewed.

## Safe Full Regeneration

Use this to rebuild scaffolds, reports, indexes, context packs, strategy outputs, DocMind execution pages, GTM operating pages, and the completion audit from the current inventory without refreshing the network scan or executing imports:

```bash
python scripts/generate_all.py --config config/sources.yaml
```

Use `--refresh-scan` only when you intend to rerun the enabled-source dry-run scan. In the active config, that can fetch public URL metadata because `allow_network: true`. Use `--execute-import --confirmed` only after Gate C.

## Gate A: Confirm Sources

Edit `config/sources.yaml` manually. Start with one low-risk export folder, keep `read_file_contents: false`, and enable only that source.

Recommended first dry-run candidates:

- Browser bookmarks export HTML
- Readwise export folder
- Notion export folder
- Manual URL list with public URLs only

Avoid first:

- Whole `~/Documents`
- Whole `~/Downloads`
- iCloud Drive, Google Drive, Dropbox, OneDrive
- Email or chat exports
- Any folder likely to contain secrets, bank, tax, medical, passport, legal, customer, or credential files

## No Dependency Install Yet

`requirements.txt` is generated for later. Do not install dependencies until you approve the import plan. Core tests use only the Python standard library.

## Current Scope

- Active vault: `/Users/ditang/obsidian/FounderOS`
- Active source: manual public URL list at `data/urls.txt`
- Private/local sources: disabled
- Online AI/OCR/transcription/embeddings: disabled
- Current completion evidence: `_System/COMPLETION_AUDIT.md`, `_System/SETUP_COMPLETE.md`, `_System/FINAL_REPORT.md`, and the unit test suite.
