import json
import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.obsidian_visibility import MANAGED_MARKER_START, ensure_obsidian_visibility


class ObsidianVisibilityTests(unittest.TestCase):
    def test_ensure_visibility_creates_outer_entry_and_standalone_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            vault = parent / "FounderOS"
            vault.mkdir()
            config = BuilderConfig(vault_path=vault)

            result = ensure_obsidian_visibility(config)

            entry = parent / "FounderOS.md"
            workspace = vault / ".obsidian/workspace.json"
            core_plugins = vault / ".obsidian/core-plugins.json"
            self.assertIn(entry.resolve(), {path.resolve() for path in result.written})
            self.assertTrue(workspace.exists())
            self.assertTrue(core_plugins.exists())
            self.assertIn("[[FounderOS/Home|FounderOS Home]]", entry.read_text(encoding="utf-8"))
            workspace_data = json.loads(workspace.read_text(encoding="utf-8"))
            self.assertIn("Home.md", workspace_data["lastOpenFiles"])

    def test_ensure_visibility_is_idempotent_and_preserves_outer_manual_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            vault = parent / "FounderOS"
            vault.mkdir()
            entry = parent / "FounderOS.md"
            entry.write_text("# FounderOS Entry\n\nManual note stays.\n", encoding="utf-8")
            config = BuilderConfig(vault_path=vault)

            ensure_obsidian_visibility(config)
            ensure_obsidian_visibility(config)

            text = entry.read_text(encoding="utf-8")
            self.assertIn("Manual note stays.", text)
            self.assertEqual(text.count(MANAGED_MARKER_START), 1)

    def test_ensure_visibility_registers_vault_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            vault = parent / "FounderOS"
            vault.mkdir()
            registry = parent / "obsidian.json"
            config = BuilderConfig(vault_path=vault)

            result = ensure_obsidian_visibility(config, register=True, registry_path=registry)

            data = json.loads(registry.read_text(encoding="utf-8"))
            self.assertTrue(result.registered)
            self.assertTrue(any(item["path"] == str(vault.resolve()) for item in data["vaults"].values()))


if __name__ == "__main__":
    unittest.main()
