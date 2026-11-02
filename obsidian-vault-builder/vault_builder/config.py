from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_EXCLUDE_DIRS = {
    "node_modules",
    ".git",
    ".svn",
    ".hg",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "target",
    ".next",
    ".nuxt",
    "coverage",
    "Library/Caches",
    "Application Support",
    ".Trash",
}


def _default_exclude_dirs() -> set[str]:
    return set(DEFAULT_EXCLUDE_DIRS)


@dataclass
class BuilderConfig:
    vault_path: Path
    dry_run: bool = True
    max_file_size_mb: int = 200
    copy_attachments: bool = False
    preserve_originals: bool = True
    read_file_contents: bool = False
    allow_ocr: bool = False
    allow_transcription: bool = False
    allow_online_ai: bool = False
    allow_network: bool = False
    sources: list[dict[str, Any]] = field(default_factory=list)
    exclude_dirs: set[str] = field(default_factory=_default_exclude_dirs)


def load_config(path: Path | str) -> BuilderConfig:
    config_path = Path(path).expanduser()
    try:
        import yaml
    except ImportError as exc:
        return _load_simple_yaml_config(config_path)

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return _from_raw_config(raw)


def _from_raw_config(raw: dict[str, Any]) -> BuilderConfig:
    settings = raw.get("settings", {})
    vault = raw.get("vault", {})
    exclude_dirs = _default_exclude_dirs()
    raw_exclude_dirs = settings.get("exclude_dirs")
    if isinstance(raw_exclude_dirs, list):
        exclude_dirs.update(str(item) for item in raw_exclude_dirs if str(item).strip())
    return BuilderConfig(
        vault_path=Path(vault.get("path", "~/Documents/Obsidian/FounderOS")).expanduser(),
        dry_run=bool(settings.get("dry_run", True)),
        max_file_size_mb=int(settings.get("max_file_size_mb", 200)),
        copy_attachments=bool(settings.get("copy_attachments", False)),
        preserve_originals=bool(settings.get("preserve_originals", True)),
        read_file_contents=bool(settings.get("read_file_contents", False)),
        allow_ocr=bool(settings.get("allow_ocr", False)),
        allow_transcription=bool(settings.get("allow_transcription", False)),
        allow_online_ai=bool(settings.get("allow_online_ai", False)),
        allow_network=bool(settings.get("allow_network", False)),
        sources=list(raw.get("sources", [])),
        exclude_dirs=exclude_dirs,
    )


def _load_simple_yaml_config(config_path: Path) -> BuilderConfig:
    raw: dict[str, Any] = {"vault": {}, "settings": {}, "sources": []}
    section = ""
    current_source: dict[str, Any] | None = None
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            section = stripped[:-1]
            continue
        if section == "vault" and stripped.startswith("path:"):
            raw["vault"]["path"] = _yaml_scalar(stripped.split(":", 1)[1])
        elif section == "settings" and stripped.startswith("- "):
            active = raw["settings"].get("_active_list")
            if active:
                raw["settings"].setdefault(active, []).append(_yaml_scalar(stripped[2:]))
        elif section == "settings" and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            parsed = _yaml_scalar(value)
            if value.strip() == "":
                raw["settings"][key] = []
                raw["settings"]["_active_list"] = key
            else:
                raw["settings"][key] = parsed
                raw["settings"].pop("_active_list", None)
        elif section == "sources":
            if stripped.startswith("- "):
                if current_source:
                    raw["sources"].append(current_source)
                current_source = {}
                item = stripped[2:]
                if ":" in item:
                    key, value = item.split(":", 1)
                    current_source[key.strip()] = _yaml_scalar(value)
            elif current_source is not None and ":" in stripped:
                key, value = stripped.split(":", 1)
                current_source[key.strip()] = _yaml_scalar(value)
    if current_source:
        raw["sources"].append(current_source)
    return _from_raw_config(raw)


def _yaml_scalar(value: str) -> Any:
    text = value.strip().strip('"').strip("'")
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    try:
        return int(text)
    except ValueError:
        return text
