from __future__ import annotations

from dataclasses import dataclass
import copy
import json
from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


@dataclass(frozen=True)
class ObsidianUIConfigResult:
    written: list[Path]


BOOKMARK_FILES = [
    ("Home", "Home.md"),
    ("Today", "01 Daily Notes/Today.md"),
    ("Founder Daily Dashboard", "01 Daily Notes/Founder Daily Dashboard.md"),
    ("DocMind GTM Dashboard", "10 Projects/DocMind/DocMind GTM Dashboard.md"),
    ("DocMind Publish Queue", "30 Content/DocMind Publish Queue.md"),
    ("Source Index", "_Indexes/Source Index.md"),
    ("Completion Audit", "_System/COMPLETION_AUDIT.md"),
]


def configure_obsidian_ui(config: BuilderConfig) -> ObsidianUIConfigResult:
    vault_path = config.vault_path.expanduser().resolve()
    obsidian_dir = safe_join(vault_path, ".obsidian")
    obsidian_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for path, data in [
        (obsidian_dir / "bookmarks.json", bookmarks_json(obsidian_dir / "bookmarks.json")),
        (obsidian_dir / "daily-notes.json", daily_notes_json(obsidian_dir / "daily-notes.json")),
        (obsidian_dir / "templates.json", templates_json(obsidian_dir / "templates.json")),
    ]:
        if _write_json_if_changed(path, data):
            written.append(path)
    return ObsidianUIConfigResult(written=written)


def bookmarks_json(path: Path) -> dict:
    data = _read_json(path, {"items": []})
    items = data.setdefault("items", [])
    if not isinstance(items, list):
        items = []
        data["items"] = items

    group = founder_bookmarks_group()
    replaced = False
    for index, item in enumerate(items):
        if isinstance(item, dict) and item.get("type") == "group" and item.get("title") == group["title"]:
            items[index] = group
            replaced = True
            break
    if not replaced:
        items.insert(0, group)
    return data


def founder_bookmarks_group() -> dict:
    return {
        "type": "group",
        "title": "FounderOS",
        "items": [{"type": "file", "title": title, "path": path} for title, path in BOOKMARK_FILES],
    }


def daily_notes_json(path: Path) -> dict:
    data = _read_json(path, {})
    data["folder"] = "01 Daily Notes"
    data["format"] = "YYYY-MM-DD"
    data["template"] = "_Templates/Daily Operating Note Template.md"
    return data


def templates_json(path: Path) -> dict:
    data = _read_json(path, {})
    data["folder"] = "_Templates"
    return data


def _read_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return copy.deepcopy(default)
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return copy.deepcopy(default)
    return loaded if isinstance(loaded, dict) else copy.deepcopy(default)


def _write_json_if_changed(path: Path, data: dict) -> bool:
    serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if serialized == previous:
        return False
    path.write_text(serialized, encoding="utf-8")
    return True
