from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path


SAFE_ACTIONS = {"metadata_note", "convert_to_note", "extract_text_to_note", "summary_note", "index_only"}
NOTE_LIKE_ACTIONS = {"metadata_note", "convert_to_note", "extract_text_to_note", "summary_note"}
BROAD_ROOT_DIRS = {"Desktop", "Documents", "Downloads"}
GENERATED_OR_TOOL_DIRS = {"FounderOS", "obsidian-vault-builder"}
GENERATED_OR_TOOL_FILES = {"FounderOS.md"}
SENSITIVE_PATH_TERMS = {
    "bank",
    "billing",
    "credential",
    "credentials",
    "customer",
    "client",
    "identity",
    "invoice",
    "key",
    "keychain",
    "medical",
    "passport",
    "password",
    "secret",
    "stripe",
    "tax",
    "title",
    "titles",
    "licence",
    "license",
    "legal",
    "visa",
    "客户",
    "客户项目",
    "医疗",
    "护照",
    "证件",
    "签证",
    "密码",
    "银行",
    "发票",
    "税",
    "财务",
    "身份",
    "权属",
    "牌照",
    "许可",
}


@dataclass(frozen=True)
class CandidateGroup:
    relative_dir: str
    absolute_dir: str
    record_count: int
    note_record_count: int
    actions: Counter[str]
    areas: Counter[str]
    extensions: Counter[str]
    sample_paths: list[str]


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def candidate_groups(records: list[dict], home_path: Path | None = None) -> list[CandidateGroup]:
    home = (home_path or Path.home()).expanduser().resolve()
    by_dir: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        if _is_safe_candidate(record, home):
            relative_dir = _relative_parent(record, home)
            by_dir[relative_dir].append(record)
    groups = [_group(relative_dir, group_records, home) for relative_dir, group_records in by_dir.items()]
    return sorted(groups, key=lambda group: (-group.note_record_count, -group.record_count, group.relative_dir.lower()))


def write_safe_import_candidates(
    records: list[dict],
    output: Path,
    home_path: Path | None = None,
    max_groups: int = 50,
) -> Path:
    groups = candidate_groups(records, home_path=home_path)
    safe_count = sum(group.record_count for group in groups)
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SAFE_IMPORT_CANDIDATES",
        "",
        "## Summary",
        "",
        f"- Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"- Full-home inventory records reviewed: {len(records)}",
        f"- Safe candidate records: {safe_count}",
        f"- Candidate directories: {len(groups)}",
        f"- Excluded records: {len(records) - safe_count}",
        "",
        "## Rules Used",
        "",
        "- Metadata-only inventory was used; file bodies were not read.",
        "- Critical, high-risk, secret-like, duplicate, skipped, and manual-review records were excluded.",
        "- Hidden paths and paths containing customer, credential, identity, medical, passport, tax, bank, invoice, or password terms were excluded.",
        "- Do not run full-home import directly. Pick one directory below, create a narrow config for it, then dry-run again.",
        "",
        "## Top Candidate Directories",
        "",
    ]
    if not groups:
        lines.append("- None.")
    for index, group in enumerate(groups[:max_groups], start=1):
        lines.extend(
            [
                f"### {index}. `{group.relative_dir}`",
                "",
                f"- Records: {group.record_count}",
                f"- Note-like records: {group.note_record_count}",
                f"- Actions: {_format_counter(group.actions)}",
                f"- Areas: {_format_counter(group.areas)}",
                f"- Extensions: {_format_counter(group.extensions)}",
                "- Samples:",
            ]
        )
        for sample in group.sample_paths:
            lines.append(f"  - `{sample}`")
        lines.append("")
    if len(groups) > max_groups:
        lines.append(f"- Truncated: {len(groups) - max_groups} additional candidate directories not shown.")
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output


def _group(relative_dir: str, records: list[dict], home: Path) -> CandidateGroup:
    actions = Counter(str(record.get("import_action") or "unknown") for record in records)
    areas = Counter(str(record.get("suggested_area") or "Resource") for record in records)
    extensions = Counter(str(record.get("extension") or Path(str(record.get("original_path") or "")).suffix or "none") for record in records)
    sample_paths = [_relative_path(record, home) for record in records[:5]]
    return CandidateGroup(
        relative_dir=relative_dir,
        absolute_dir=str((home / relative_dir).resolve()) if relative_dir != "." else str(home),
        record_count=len(records),
        note_record_count=sum(1 for record in records if str(record.get("import_action") or "") in NOTE_LIKE_ACTIONS),
        actions=actions,
        areas=areas,
        extensions=extensions,
        sample_paths=sample_paths,
    )


def _is_safe_candidate(record: dict, home: Path) -> bool:
    action = str(record.get("import_action") or "")
    if action not in SAFE_ACTIONS:
        return False
    if _as_bool(record.get("needs_manual_review")):
        return False
    if _as_bool(record.get("secret_risk")):
        return False
    if str(record.get("pii_risk") or "").lower() in {"critical", "high"}:
        return False
    if str(record.get("duplicate_of") or ""):
        return False
    relative = _relative_path(record, home)
    if not relative or relative.startswith("../"):
        return False
    parts = Path(relative).parts
    if any(part.startswith(".") for part in parts):
        return False
    if parts and parts[-1] in GENERATED_OR_TOOL_FILES:
        return False
    if any(part in GENERATED_OR_TOOL_DIRS for part in parts):
        return False
    if len(parts) <= 2 and parts and parts[0] in BROAD_ROOT_DIRS:
        return False
    lowered = relative.lower()
    return not any(term.lower() in lowered for term in SENSITIVE_PATH_TERMS)


def _relative_parent(record: dict, home: Path) -> str:
    relative = Path(_relative_path(record, home))
    parent = relative.parent
    return "." if str(parent) == "." else str(parent)


def _relative_path(record: dict, home: Path) -> str:
    path_text = str(record.get("original_path") or "")
    if not path_text:
        return ""
    try:
        path = Path(path_text).expanduser().resolve()
        return str(path.relative_to(home))
    except (OSError, ValueError):
        return f"../{path_text}"


def _format_counter(counter: Counter[str], limit: int = 4) -> str:
    if not counter:
        return "none"
    parts = [f"{key}:{value}" for key, value in counter.most_common(limit)]
    if len(counter) > limit:
        parts.append(f"+{len(counter) - limit} more")
    return ", ".join(parts)


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y"}
