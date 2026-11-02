from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
import json
from pathlib import Path
import time

from .config import BuilderConfig
from .sanitize import safe_join


MANAGED_MARKER_START = "<!-- founderos-visible-entry:start -->"
MANAGED_MARKER_END = "<!-- founderos-visible-entry:end -->"


@dataclass(frozen=True)
class VisibilityResult:
    written: list[Path]
    registered: bool
    registry_path: Path | None


def ensure_obsidian_visibility(
    config: BuilderConfig,
    register: bool = False,
    registry_path: Path | None = None,
) -> VisibilityResult:
    written: list[Path] = []
    entry = write_outer_entry(config)
    if entry:
        written.append(entry)
    written.extend(ensure_standalone_vault_config(config))
    registered = False
    if register:
        registered = register_vault(config, registry_path=registry_path)
    return VisibilityResult(written=written, registered=registered, registry_path=registry_path or default_obsidian_registry_path())


def write_outer_entry(config: BuilderConfig) -> Path | None:
    vault_path = config.vault_path.expanduser().resolve()
    parent = vault_path.parent
    entry_path = parent / f"{vault_path.name}.md"
    body = outer_entry_body(vault_path.name)
    existing = entry_path.read_text(encoding="utf-8") if entry_path.exists() else f"# {vault_path.name} Entry\n"
    updated = _upsert(existing, body)
    if updated != existing:
        entry_path.write_text(updated, encoding="utf-8")
        return entry_path
    return None


def ensure_standalone_vault_config(config: BuilderConfig) -> list[Path]:
    vault_path = config.vault_path.expanduser().resolve()
    obsidian_dir = safe_join(vault_path, ".obsidian")
    obsidian_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    app_json = obsidian_dir / "app.json"
    if not app_json.exists():
        app_json.write_text(json.dumps({"useMarkdownLinks": True, "newLinkFormat": "relative", "promptDelete": False}, indent=2) + "\n", encoding="utf-8")
        written.append(app_json)

    core_plugins = obsidian_dir / "core-plugins.json"
    if not core_plugins.exists():
        core_plugins.write_text(json.dumps(default_core_plugins(), indent=2) + "\n", encoding="utf-8")
        written.append(core_plugins)

    workspace = obsidian_dir / "workspace.json"
    updated_workspace = workspace_json(workspace)
    previous = workspace.read_text(encoding="utf-8") if workspace.exists() else ""
    serialized = json.dumps(updated_workspace, ensure_ascii=False, indent=2) + "\n"
    if serialized != previous:
        workspace.write_text(serialized, encoding="utf-8")
        written.append(workspace)
    return written


def register_vault(config: BuilderConfig, registry_path: Path | None = None) -> bool:
    registry = registry_path or default_obsidian_registry_path()
    registry.parent.mkdir(parents=True, exist_ok=True)
    vault_path = str(config.vault_path.expanduser().resolve())
    data = _read_json(registry, {"vaults": {}})
    vaults = data.setdefault("vaults", {})
    for vault in vaults.values():
        if str(vault.get("path")) == vault_path:
            vault["open"] = True
            registry.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            return False
    key = sha1(vault_path.encode("utf-8")).hexdigest()[:16]
    vaults[key] = {"path": vault_path, "ts": int(time.time() * 1000), "open": True}
    registry.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return True


def default_obsidian_registry_path() -> Path:
    return Path.home() / "Library/Application Support/obsidian/obsidian.json"


def outer_entry_body(vault_name: str) -> str:
    return f"""## Open {vault_name}

- [[{vault_name}/Home|{vault_name} Home]]
- [[{vault_name}/01 Daily Notes/Today|Today]]
- [[{vault_name}/01 Daily Notes/Founder Daily Dashboard|Founder Daily Dashboard]]
- [[{vault_name}/10 Projects/DocMind/DocMind GTM Dashboard|DocMind GTM Dashboard]]
- [[{vault_name}/30 Content/DocMind Publish Queue|DocMind Publish Queue]]
- [[{vault_name}/_System/COMPLETION_AUDIT|Completion Audit]]

## Where It Lives

- Folder: `{vault_name}/`
- Builder: `obsidian-vault-builder/`
- Safe full regeneration: `python scripts/generate_all.py --config config/sources.yaml`

## Safety State

- Private/local folders are disabled.
- Online AI, OCR, transcription, and embeddings are disabled.
- Current imported source notes are public URL source notes only.
"""


def workspace_json(path: Path) -> dict:
    data = _read_json(path, default_workspace())
    _ensure_home_leaf(data)
    _ensure_file_explorer_auto_reveal(data)
    last_open = data.setdefault("lastOpenFiles", [])
    for item in [
        "Home.md",
        "01 Daily Notes/Today.md",
        "01 Daily Notes/Founder Daily Dashboard.md",
        "10 Projects/DocMind/DocMind GTM Dashboard.md",
        "_System/COMPLETION_AUDIT.md",
    ]:
        if item not in last_open:
            last_open.append(item)
    return data


def default_workspace() -> dict:
    return {
        "main": {
            "id": "founderos-main",
            "type": "split",
            "children": [
                {
                    "id": "founderos-tabs",
                    "type": "tabs",
                    "children": [
                        {
                            "id": "founderos-home",
                            "type": "leaf",
                            "state": {
                                "type": "markdown",
                                "state": {"file": "Home.md", "mode": "source", "source": False},
                                "icon": "lucide-file",
                                "title": "Home",
                            },
                        }
                    ],
                }
            ],
            "direction": "vertical",
        },
        "left": {
            "id": "founderos-left",
            "type": "split",
            "children": [
                {
                    "id": "founderos-left-tabs",
                    "type": "tabs",
                    "children": [
                        {
                            "id": "founderos-file-explorer",
                            "type": "leaf",
                            "state": {
                                "type": "file-explorer",
                                "state": {"sortOrder": "alphabetical", "autoReveal": True},
                                "icon": "lucide-folder-closed",
                                "title": "Files",
                            },
                        }
                    ],
                }
            ],
            "direction": "horizontal",
            "width": 300,
        },
        "right": {"id": "founderos-right", "type": "split", "children": [], "direction": "horizontal", "width": 300, "collapsed": True},
        "active": "founderos-home",
        "lastOpenFiles": ["Home.md"],
    }


def default_core_plugins() -> list[str]:
    return [
        "file-explorer",
        "global-search",
        "switcher",
        "graph",
        "backlink",
        "canvas",
        "outgoing-link",
        "tag-pane",
        "page-preview",
        "daily-notes",
        "templates",
        "note-composer",
        "command-palette",
        "slash-command",
        "editor-status",
        "bookmarks",
        "properties",
        "bases",
    ]


def _upsert(existing: str, body: str) -> str:
    block = f"{MANAGED_MARKER_START}\n{body.rstrip()}\n{MANAGED_MARKER_END}\n"
    if MANAGED_MARKER_START in existing and MANAGED_MARKER_END in existing:
        start = existing.index(MANAGED_MARKER_START)
        end = existing.index(MANAGED_MARKER_END, start) + len(MANAGED_MARKER_END)
        return f"{existing[:start]}{block.rstrip()}{existing[end:]}".rstrip() + "\n"
    return f"{existing.rstrip()}\n\n{block}"


def _read_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _ensure_home_leaf(data: dict) -> None:
    main = data.setdefault("main", default_workspace()["main"])
    if not _contains_file(main, "Home.md"):
        data["main"] = default_workspace()["main"]
        data["active"] = "founderos-home"


def _ensure_file_explorer_auto_reveal(node: object) -> None:
    if isinstance(node, dict):
        state = node.get("state")
        if isinstance(state, dict) and state.get("type") == "file-explorer":
            inner = state.setdefault("state", {})
            if isinstance(inner, dict):
                inner["autoReveal"] = True
        for value in node.values():
            _ensure_file_explorer_auto_reveal(value)
    elif isinstance(node, list):
        for value in node:
            _ensure_file_explorer_auto_reveal(value)


def _contains_file(node: object, filename: str) -> bool:
    if isinstance(node, dict):
        state = node.get("state")
        if isinstance(state, dict):
            inner = state.get("state")
            if isinstance(inner, dict) and inner.get("file") == filename:
                return True
        return any(_contains_file(value, filename) for value in node.values())
    if isinstance(node, list):
        return any(_contains_file(value, filename) for value in node)
    return False
