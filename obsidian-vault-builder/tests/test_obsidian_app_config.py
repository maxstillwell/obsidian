import json
import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.obsidian_app_config import configure_obsidian_ui


class ObsidianAppConfigTests(unittest.TestCase):
    def test_configure_obsidian_ui_writes_bookmarks_daily_notes_and_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "FounderOS"
            vault.mkdir()
            config = BuilderConfig(vault_path=vault)

            result = configure_obsidian_ui(config)

            updated = {path.name for path in result.written}
            self.assertEqual(updated, {"bookmarks.json", "daily-notes.json", "templates.json"})

            bookmarks = json.loads((vault / ".obsidian/bookmarks.json").read_text(encoding="utf-8"))
            daily_notes = json.loads((vault / ".obsidian/daily-notes.json").read_text(encoding="utf-8"))
            templates = json.loads((vault / ".obsidian/templates.json").read_text(encoding="utf-8"))

            self.assertEqual(bookmarks["items"][0]["title"], "FounderOS")
            self.assertIn({"type": "file", "title": "Home", "path": "Home.md"}, bookmarks["items"][0]["items"])
            self.assertEqual(daily_notes["folder"], "01 Daily Notes")
            self.assertEqual(daily_notes["template"], "_Templates/Daily Operating Note Template.md")
            self.assertEqual(templates["folder"], "_Templates")

    def test_configure_obsidian_ui_is_idempotent_and_preserves_manual_bookmarks(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "FounderOS"
            obsidian_dir = vault / ".obsidian"
            obsidian_dir.mkdir(parents=True)
            (obsidian_dir / "bookmarks.json").write_text(
                json.dumps(
                    {
                        "items": [
                            {"type": "file", "title": "Manual", "path": "Manual.md"},
                            {"type": "group", "title": "FounderOS", "items": [{"type": "file", "title": "Old", "path": "Old.md"}]},
                        ]
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            config = BuilderConfig(vault_path=vault)

            configure_obsidian_ui(config)
            second = configure_obsidian_ui(config)

            self.assertEqual(second.written, [])
            bookmarks = json.loads((obsidian_dir / "bookmarks.json").read_text(encoding="utf-8"))
            self.assertEqual(sum(1 for item in bookmarks["items"] if item.get("title") == "FounderOS"), 1)
            self.assertIn({"type": "file", "title": "Manual", "path": "Manual.md"}, bookmarks["items"])
            founder_group = next(item for item in bookmarks["items"] if item.get("title") == "FounderOS")
            self.assertNotIn({"type": "file", "title": "Old", "path": "Old.md"}, founder_group["items"])

    def test_configure_obsidian_ui_preserves_extra_plugin_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "FounderOS"
            obsidian_dir = vault / ".obsidian"
            obsidian_dir.mkdir(parents=True)
            (obsidian_dir / "daily-notes.json").write_text('{"autorun": true}\n', encoding="utf-8")
            (obsidian_dir / "templates.json").write_text('{"dateFormat": "YYYY-MM-DD"}\n', encoding="utf-8")
            config = BuilderConfig(vault_path=vault)

            configure_obsidian_ui(config)

            daily_notes = json.loads((obsidian_dir / "daily-notes.json").read_text(encoding="utf-8"))
            templates = json.loads((obsidian_dir / "templates.json").read_text(encoding="utf-8"))
            self.assertTrue(daily_notes["autorun"])
            self.assertEqual(templates["dateFormat"], "YYYY-MM-DD")


if __name__ == "__main__":
    unittest.main()
