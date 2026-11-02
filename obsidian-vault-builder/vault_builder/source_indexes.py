from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


MANAGED_MARKER_START = "<!-- founderos-source-index:start -->"
MANAGED_MARKER_END = "<!-- founderos-source-index:end -->"


@dataclass(frozen=True)
class SourceNote:
    title: str
    path: Path
    source_url: str
    project: str
    area: str
    status: str

    @property
    def wikilink(self) -> str:
        if "[" in self.path.stem or "]" in self.path.stem:
            return f"[{self.title}]({_resource_relative_path(self.path)})"
        return f"[[{self.path.stem}]]"


def write_source_indexes(config: BuilderConfig) -> list[Path]:
    notes = read_source_notes(config.vault_path)
    index_bodies = {
        "_Indexes/Source Index.md": source_index_body(notes),
        "_Indexes/Research Index.md": filtered_index_body("Research Sources", notes, area="Research"),
        "_Indexes/DocMind Index.md": filtered_index_body("DocMind Sources", notes, project="DocMind"),
        "_Indexes/221B Index.md": filtered_index_body("221B Sources", notes, project="221B"),
        "_Indexes/AI Workflow Index.md": filtered_index_body("AI Workflow Sources", notes, area="AI Workflows"),
        "60 Resources/Resources Home.md": resources_home_body(notes),
    }
    written: list[Path] = []
    for relative_path, body in index_bodies.items():
        path = safe_join(config.vault_path, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else f"# {Path(relative_path).stem}\n"
        updated = _upsert(existing, body)
        if updated != existing:
            path.write_text(updated, encoding="utf-8")
            written.append(path)
    return written


def read_source_notes(vault_path: Path) -> list[SourceNote]:
    root = vault_path / "60 Resources"
    notes: list[SourceNote] = []
    if not root.exists():
        return notes
    for path in sorted(root.rglob("*.md")):
        meta = _frontmatter(path)
        if meta.get("type") != "source":
            continue
        notes.append(
            SourceNote(
                title=meta.get("title") or path.stem,
                path=path,
                source_url=meta.get("source_url", ""),
                project=meta.get("project", ""),
                area=meta.get("area", "") or "Resource",
                status=meta.get("status", ""),
            )
        )
    return notes


def source_index_body(notes: list[SourceNote]) -> str:
    by_area = defaultdict(list)
    by_project = defaultdict(list)
    for note in notes:
        by_area[note.area].append(note)
        if note.project:
            by_project[note.project].append(note)
    lines = [
        "## Generated Source Overview",
        "",
        f"- Imported source notes: {len(notes)}",
        f"- Areas: {', '.join(sorted(by_area)) if by_area else 'None'}",
        f"- Projects: {', '.join(sorted(by_project)) if by_project else 'None'}",
        "",
        "## By Area",
        "",
    ]
    lines.extend(_group_lines(by_area))
    lines.extend(["", "## By Project", ""])
    lines.extend(_group_lines(by_project))
    lines.extend(["", "## All Sources", ""])
    lines.extend(_note_lines(notes) or ["- None."])
    return "\n".join(lines)


def filtered_index_body(title: str, notes: list[SourceNote], area: str = "", project: str = "") -> str:
    filtered = [
        note for note in notes
        if (not area or note.area == area) and (not project or note.project == project)
    ]
    lines = [
        f"## Generated {title}",
        "",
        f"- Source notes: {len(filtered)}",
        "",
        "## Sources",
        "",
    ]
    lines.extend(_note_lines(filtered) or ["- None."])
    return "\n".join(lines)


def resources_home_body(notes: list[SourceNote]) -> str:
    recent = notes[-12:]
    lines = [
        "## Generated Public Resource Overview",
        "",
        f"- Public source notes: {len(notes)}",
        "- Private/local folders: disabled",
        "- Source note folder: [[Source Index]]",
        "",
        "## Recent Source Notes",
        "",
    ]
    lines.extend(_note_lines(recent) or ["- None."])
    return "\n".join(lines)


def _note_lines(notes: list[SourceNote]) -> list[str]:
    return [
        f"- {note.wikilink} - {note.area}{f' / {note.project}' if note.project else ''}{f' - {note.source_url}' if note.source_url else ''}"
        for note in notes
    ]


def _resource_relative_path(path: Path) -> str:
    parts = path.parts
    if "60 Resources" in parts:
        index = parts.index("60 Resources")
        return "../" + "/".join(parts[index:])
    return str(path)


def _group_lines(groups: dict[str, list[SourceNote]]) -> list[str]:
    lines: list[str] = []
    if not groups:
        return ["- None."]
    for group in sorted(groups):
        lines.append(f"### {group}")
        lines.append("")
        lines.extend(_note_lines(groups[group]) or ["- None."])
        lines.append("")
    return lines


def _frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta


def _upsert(existing: str, body: str) -> str:
    block = f"{MANAGED_MARKER_START}\n{body.rstrip()}\n{MANAGED_MARKER_END}\n"
    if MANAGED_MARKER_START in existing and MANAGED_MARKER_END in existing:
        start = existing.index(MANAGED_MARKER_START)
        end = existing.index(MANAGED_MARKER_END, start) + len(MANAGED_MARKER_END)
        return f"{existing[:start]}{block.rstrip()}{existing[end:]}".rstrip() + "\n"
    return f"{existing.rstrip()}\n\n{block}"
