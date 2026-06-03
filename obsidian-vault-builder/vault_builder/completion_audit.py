from __future__ import annotations

import json
from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join
from .vault_writer import VAULT_DIRS


REQUIRED_VAULT_FILES = [
    "Home.md",
    "00 Inbox/Inbox.md",
    "10 Projects/DocMind/DocMind Home.md",
    "10 Projects/221B/221B Home.md",
    "20 Research/Research Map.md",
    "30 Content/Content Engine Home.md",
    "40 Meetings & People/Meetings Home.md",
    "50 AI Prompts & Workflows/AI Workflow Library.md",
    "60 Resources/Resources Home.md",
    "80 Databases/Databases Home.md",
    "_System/README.md",
    "_System/IMPORT_PLAN.md",
    "_System/SCAN_REPORT.md",
    "_System/PRIVACY_REVIEW.md",
    "_System/CHANGELOG.md",
    "_System/IMPORT_LOG.md",
    "_System/ERROR_LOG.md",
    "_System/MANUAL_REVIEW.md",
    "_System/DEDUPE_REPORT.md",
    "_System/SOURCES.md",
    "_System/RULES.md",
    "_System/FINAL_REPORT.md",
    "_System/SETUP_COMPLETE.md",
    "_System/GATE_STATUS.md",
]


REQUIRED_INDEXES = [
    "_Indexes/Master Index.md",
    "_Indexes/Project Index.md",
    "_Indexes/DocMind Index.md",
    "_Indexes/221B Index.md",
    "_Indexes/Content Index.md",
    "_Indexes/Research Index.md",
    "_Indexes/Meeting Index.md",
    "_Indexes/People Index.md",
    "_Indexes/Decision Index.md",
    "_Indexes/Source Index.md",
    "_Indexes/AI Workflow Index.md",
    "_Indexes/Tag Index.md",
]


REQUIRED_TEMPLATES = [
    "_Templates/Daily Note Template.md",
    "_Templates/Project Template.md",
    "_Templates/Meeting Template.md",
    "_Templates/Customer Call Template.md",
    "_Templates/Research Note Template.md",
    "_Templates/Content Brief Template.md",
    "_Templates/Decision Template.md",
    "_Templates/Source Note Template.md",
    "_Templates/Person Template.md",
    "_Templates/Company Template.md",
    "_Templates/Prompt Template.md",
    "_Templates/AI Workflow Template.md",
    "_Templates/Book Note Template.md",
    "_Templates/Article Note Template.md",
    "_Templates/Weekly Review Template.md",
    "_Templates/Monthly Review Template.md",
]


REQUIRED_CONTEXT_PACKS = [
    "_Context Packs/founder-profile-context.md",
    "_Context Packs/docmind-context.md",
    "_Context Packs/221b-context.md",
    "_Context Packs/content-strategy-context.md",
    "_Context Packs/ai-workflow-context.md",
    "_Context Packs/research-context.md",
    "_Context Packs/current-projects-context.md",
    "_Context Packs/weekly-review-context.md",
    "_Context Packs/docmind-execution-context.md",
    "_Context Packs/docmind-gtm-context.md",
    "_Context Packs/daily-operating-context.md",
]


REQUIRED_BASES = [
    "80 Databases/Projects.base",
    "80 Databases/Content.base",
    "80 Databases/Meetings.base",
    "80 Databases/Research.base",
    "80 Databases/People.base",
    "80 Databases/Decisions.base",
    "80 Databases/Sources.base",
    "80 Databases/Operating.base",
    "80 Databases/DocMind GTM.base",
]


REQUIRED_BUILDER_FILES = [
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    ".gitignore",
    "config/sources.example.yaml",
    "config/sources.yaml",
    "config/sources.full-home.example.yaml",
    "config/rules.yaml",
    "config/privacy_rules.yaml",
    "config/classification_rules.yaml",
    "data/inventory.csv",
    "data/inventory.json",
    "data/import_state.json",
    "data/hashes.json",
    "data/review_queue.csv",
    "logs/scan.log",
    "logs/import.log",
    "logs/errors.log",
    "scripts/preflight.py",
    "scripts/create_vault.py",
    "scripts/scan_sources.py",
    "scripts/classify_files.py",
    "scripts/privacy_review.py",
    "scripts/dedupe_files.py",
    "scripts/extract_text.py",
    "scripts/create_obsidian_notes.py",
    "scripts/generate_indexes.py",
    "scripts/generate_context_packs.py",
    "scripts/generate_bases.py",
    "scripts/run_import.py",
    "scripts/rollback_import.py",
    "scripts/report.py",
    "scripts/generate_all.py",
    "scripts/generate_completion_audit.py",
    "scripts/generate_daily_operating_layer.py",
    "scripts/ensure_obsidian_visibility.py",
    "scripts/configure_obsidian_ui.py",
    "vault_builder/obsidian_app_config.py",
    "vault_builder/preflight.py",
]


REQUIRED_TESTS = [
    "tests/test_paths.py",
    "tests/test_sanitize.py",
    "tests/test_classification.py",
    "tests/test_privacy_rules.py",
    "tests/test_dedupe.py",
    "tests/test_importer.py",
    "tests/test_report.py",
    "tests/test_completion_audit.py",
    "tests/test_daily_operating_layer.py",
    "tests/test_obsidian_visibility.py",
    "tests/test_obsidian_app_config.py",
    "tests/test_preflight_scope.py",
]


def write_completion_audit(config: BuilderConfig, records: list[dict], builder_root: Path | str = Path(".")) -> Path:
    root = Path(builder_root).expanduser().resolve()
    checks = completion_checks(config, records, root)
    passed = sum(1 for check in checks if check["status"] == "PASS")
    failed = [check for check in checks if check["status"] != "PASS"]
    output = safe_join(config.vault_path, "_System/COMPLETION_AUDIT.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# COMPLETION_AUDIT",
        "",
        "## Summary",
        "",
        f"- Checks passed: {passed}/{len(checks)}",
        f"- Checks failed: {len(failed)}",
        f"- Inventory records: {len(records)}",
        f"- Private/local sources enabled: {len(_enabled_private_sources(config))}",
        "",
        "## Requirement Matrix",
        "",
        "| Requirement | Status | Evidence |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| {check['requirement']} | {check['status']} | {check['evidence']} |")
    if failed:
        lines.extend(["", "## Failing Checks", ""])
        for check in failed:
            lines.append(f"- {check['requirement']}: {check['evidence']}")
    else:
        lines.extend(["", "## Result", "", "All completion checks passed for the current configured scope."])
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def completion_checks(config: BuilderConfig, records: list[dict], builder_root: Path) -> list[dict[str, str]]:
    return [
        _check("Vault directory exists", config.vault_path.exists(), str(config.vault_path)),
        _missing_check("Required vault folders", [safe_join(config.vault_path, path) for path in VAULT_DIRS]),
        _missing_check("Required vault system files", [safe_join(config.vault_path, path) for path in REQUIRED_VAULT_FILES]),
        _missing_check("Required templates", [safe_join(config.vault_path, path) for path in REQUIRED_TEMPLATES]),
        _missing_check("Required indexes", [safe_join(config.vault_path, path) for path in REQUIRED_INDEXES]),
        _missing_check("Required context packs", [safe_join(config.vault_path, path) for path in REQUIRED_CONTEXT_PACKS]),
        _missing_check("Required Obsidian Bases", [safe_join(config.vault_path, path) for path in REQUIRED_BASES]),
        _missing_check("Required builder scaffold", [builder_root / path for path in REQUIRED_BUILDER_FILES]),
        _missing_check("Required tests", [builder_root / path for path in REQUIRED_TESTS]),
        _check("Outer Obsidian entry note exists", _outer_entry_exists(config), str(config.vault_path.expanduser().resolve().parent / f"{config.vault_path.expanduser().resolve().name}.md")),
        _check("Standalone Obsidian config exists", _standalone_obsidian_config_exists(config), str(config.vault_path.expanduser().resolve() / ".obsidian")),
        _check("Standalone Obsidian UI config exists", _standalone_obsidian_ui_config_exists(config), str(config.vault_path.expanduser().resolve() / ".obsidian")),
        _check("Obsidian registry includes FounderOS vault", _obsidian_registry_has_vault(config), str(_default_obsidian_registry_path())),
        _check("Private/local sources disabled", not _enabled_private_sources(config), str(_enabled_private_sources(config))),
        _check("Dry-run default remains enabled", config.dry_run is True, f"dry_run={config.dry_run}"),
        _check("File content reads disabled", config.read_file_contents is False, f"read_file_contents={config.read_file_contents}"),
        _check("Online AI disabled", config.allow_online_ai is False, f"allow_online_ai={config.allow_online_ai}"),
        _check("OCR disabled", config.allow_ocr is False, f"allow_ocr={config.allow_ocr}"),
        _check("Transcription disabled", config.allow_transcription is False, f"allow_transcription={config.allow_transcription}"),
        _check("Inventory records exist", len(records) > 0, f"records={len(records)}"),
        _check(
            "Current inventory is public URL-list only",
            all(str(record.get("source_type")) == "url_list" for record in records),
            _source_type_summary(records),
        ),
        _check("Manual-review queue is empty for current scope", _manual_review_count(records) == 0, f"manual={_manual_review_count(records)}"),
        _check("Source notes have traceable frontmatter", _source_notes_traceable(config, records), _source_note_evidence(config)),
        _check("Import state supports resume", _import_state_has_batches(builder_root), str(builder_root / "data/import_state.json")),
        _check("Rollback script exists", (builder_root / "scripts/rollback_import.py").exists(), "scripts/rollback_import.py"),
        _check("Dedupe report exists", safe_join(config.vault_path, "_System/DEDUPE_REPORT.md").exists(), "_System/DEDUPE_REPORT.md"),
        _check("Privacy review matches inventory count", _report_contains(config, "_System/PRIVACY_REVIEW.md", f"Inventory rows: {len(records)}"), "_System/PRIVACY_REVIEW.md"),
        _check("Gate status exists", safe_join(config.vault_path, "_System/GATE_STATUS.md").exists(), "_System/GATE_STATUS.md"),
        _check("Final report exists", safe_join(config.vault_path, "_System/FINAL_REPORT.md").exists(), "_System/FINAL_REPORT.md"),
    ]


def _check(requirement: str, ok: bool, evidence: str) -> dict[str, str]:
    return {"requirement": requirement, "status": "PASS" if ok else "FAIL", "evidence": _table_escape(evidence)}


def _missing_check(requirement: str, paths: list[Path]) -> dict[str, str]:
    missing = [str(path) for path in paths if not path.exists()]
    return _check(requirement, not missing, "missing none" if not missing else f"missing {len(missing)}: {', '.join(missing[:5])}")


def _enabled_private_sources(config: BuilderConfig) -> list[str]:
    private_types = {"folder", "file"}
    return [str(source.get("name") or source.get("path_or_url") or "") for source in config.sources if source.get("enabled") and source.get("type") in private_types]


def _outer_entry_exists(config: BuilderConfig) -> bool:
    vault_path = config.vault_path.expanduser().resolve()
    entry = vault_path.parent / f"{vault_path.name}.md"
    if not entry.exists():
        return False
    text = entry.read_text(encoding="utf-8", errors="ignore")
    return f"[[{vault_path.name}/Home" in text


def _standalone_obsidian_config_exists(config: BuilderConfig) -> bool:
    obsidian_dir = config.vault_path.expanduser().resolve() / ".obsidian"
    return (obsidian_dir / "app.json").exists() and (obsidian_dir / "core-plugins.json").exists() and (obsidian_dir / "workspace.json").exists()


def _standalone_obsidian_ui_config_exists(config: BuilderConfig) -> bool:
    obsidian_dir = config.vault_path.expanduser().resolve() / ".obsidian"
    bookmarks = _read_json_file(obsidian_dir / "bookmarks.json")
    daily_notes = _read_json_file(obsidian_dir / "daily-notes.json")
    templates = _read_json_file(obsidian_dir / "templates.json")
    return (
        _bookmarks_have_founderos_group(bookmarks)
        and daily_notes.get("folder") == "01 Daily Notes"
        and daily_notes.get("template") == "_Templates/Daily Operating Note Template.md"
        and templates.get("folder") == "_Templates"
    )


def _bookmarks_have_founderos_group(data: dict) -> bool:
    items = data.get("items")
    if not isinstance(items, list):
        return False
    for item in items:
        if not isinstance(item, dict) or item.get("type") != "group" or item.get("title") != "FounderOS":
            continue
        children = item.get("items")
        if not isinstance(children, list):
            return False
        paths = {child.get("path") for child in children if isinstance(child, dict)}
        return {"Home.md", "01 Daily Notes/Today.md", "_System/COMPLETION_AUDIT.md"}.issubset(paths)
    return False


def _read_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _obsidian_registry_has_vault(config: BuilderConfig) -> bool:
    registry = _default_obsidian_registry_path()
    if not registry.exists():
        return False
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    target = str(config.vault_path.expanduser().resolve())
    return any(str(vault.get("path")) == target for vault in data.get("vaults", {}).values())


def _default_obsidian_registry_path() -> Path:
    return Path.home() / "Library/Application Support/obsidian/obsidian.json"


def _manual_review_count(records: list[dict]) -> int:
    return sum(1 for record in records if _as_bool(record.get("needs_manual_review")))


def _source_type_summary(records: list[dict]) -> str:
    types = sorted({str(record.get("source_type") or "") for record in records})
    return ", ".join(types)


def _source_notes(config: BuilderConfig) -> list[Path]:
    resources = safe_join(config.vault_path, "60 Resources")
    if not resources.exists():
        return []
    notes: list[Path] = []
    for path in resources.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "type: source" in text[:500]:
            notes.append(path)
    return notes


def _source_notes_traceable(config: BuilderConfig, records: list[dict]) -> bool:
    notes = _source_notes(config)
    if len(notes) < len(records):
        return False
    for path in notes:
        text = path.read_text(encoding="utf-8", errors="ignore")[:1200]
        if "source_url:" not in text or "hash:" not in text or "import_action:" not in text:
            return False
    return True


def _source_note_evidence(config: BuilderConfig) -> str:
    notes = _source_notes(config)
    return f"source_notes={len(notes)}"


def _import_state_has_batches(builder_root: Path) -> bool:
    state_path = builder_root / "data/import_state.json"
    if not state_path.exists():
        return False
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return bool(state.get("batches")) and bool(state.get("last_batch_id"))


def _report_contains(config: BuilderConfig, relative_path: str, text: str) -> bool:
    path = safe_join(config.vault_path, relative_path)
    if not path.exists():
        return False
    return text in path.read_text(encoding="utf-8", errors="ignore")


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _table_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
