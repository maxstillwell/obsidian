import json
import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.importer import create_import_plan, execute_import, importable_records, rollback_batch


class ImporterTests(unittest.TestCase):
    def test_create_import_plan_writes_gate_c_plan_without_importing(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            config = BuilderConfig(vault_path=vault, dry_run=True)
            records = [
                {
                    "id": "url-1",
                    "source_url": "https://example.com/a",
                    "original_path": str(Path(tmp) / "urls.txt"),
                    "filename": "urls.txt",
                    "suggested_destination": "60 Resources/Websites",
                    "suggested_area": "Resource",
                    "suggested_project": "",
                    "pii_risk": "low",
                    "secret_risk": False,
                    "import_action": "metadata_note",
                    "needs_manual_review": False,
                    "hash": "",
                }
            ]

            plan = create_import_plan(records, config)

            self.assertTrue(plan.exists())
            self.assertIn("Gate C", plan.read_text(encoding="utf-8"))
            self.assertEqual(list(vault.glob("60 Resources/Websites/*.md")), [])

    def test_create_import_plan_can_write_to_custom_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            output = Path(tmp) / "FULL_HOME_IMPORT_PLAN.md"
            config = BuilderConfig(vault_path=vault, dry_run=True)
            records = [
                {
                    "id": "file-1",
                    "original_path": str(Path(tmp) / "document.md"),
                    "filename": "document.md",
                    "suggested_destination": "00 Inbox",
                    "pii_risk": "medium",
                    "secret_risk": False,
                    "import_action": "metadata_note",
                    "needs_manual_review": False,
                    "hash": "",
                }
            ]

            plan = create_import_plan(records, config, output=output)

            self.assertEqual(plan, output)
            self.assertTrue(output.exists())
            self.assertFalse((vault / "_System/IMPORT_PLAN.md").exists())

    def test_create_import_plan_counts_string_false_as_not_manual_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault", dry_run=True)
            records = [
                {
                    "id": "url-1",
                    "source_url": "https://example.com/a",
                    "original_path": str(Path(tmp) / "urls.txt"),
                    "filename": "urls.txt",
                    "suggested_destination": "60 Resources/Websites",
                    "pii_risk": "low",
                    "secret_risk": "False",
                    "import_action": "metadata_note",
                    "needs_manual_review": "False",
                    "hash": "abc123",
                }
            ]

            plan = create_import_plan(records, config)

            text = plan.read_text(encoding="utf-8")
            self.assertIn("Planned importable records: 1", text)
            self.assertIn("Manual review records: 0", text)

    def test_execute_import_creates_metadata_note_and_state_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            state_path = Path(tmp) / "import_state.json"
            config = BuilderConfig(vault_path=vault, dry_run=False)
            records = [
                {
                    "id": "url-1",
                    "source_url": "https://example.com/a",
                    "original_path": str(Path(tmp) / "urls.txt"),
                    "filename": "Example URL",
                    "suggested_destination": "60 Resources/Websites",
                    "suggested_area": "Resource",
                    "suggested_project": "",
                    "pii_risk": "low",
                    "secret_risk": False,
                    "import_action": "metadata_note",
                    "needs_manual_review": False,
                    "hash": "abc123",
                }
            ]

            batch = execute_import(records, config, state_path=state_path)

            self.assertEqual(len(batch["created_files"]), 1)
            note = Path(batch["created_files"][0])
            self.assertTrue(note.exists())
            self.assertIn("source_url: https://example.com/a", note.read_text(encoding="utf-8"))
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["last_batch_id"], batch["batch_id"])

    def test_execute_import_skips_existing_source_url_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            note_dir = vault / "60 Resources/Websites"
            note_dir.mkdir(parents=True)
            (note_dir / "Existing.md").write_text(
                "---\nsource_url: https://example.com/a\nhash: abc123\n---\n\n# Existing\n",
                encoding="utf-8",
            )
            state_path = Path(tmp) / "import_state.json"
            config = BuilderConfig(vault_path=vault, dry_run=False)
            records = [
                {
                    "id": "url-1",
                    "source_url": "https://example.com/a",
                    "original_path": str(Path(tmp) / "urls.txt"),
                    "filename": "Example URL",
                    "suggested_destination": "60 Resources/Websites",
                    "suggested_area": "Resource",
                    "suggested_project": "",
                    "pii_risk": "low",
                    "secret_risk": False,
                    "import_action": "metadata_note",
                    "needs_manual_review": False,
                    "hash": "abc123",
                }
            ]

            batch = execute_import(records, config, state_path=state_path)

            self.assertEqual(batch["created_files"], [])
            self.assertEqual(len(batch["skipped"]), 1)
            self.assertEqual(len(list(note_dir.glob("*.md"))), 1)

    def test_rollback_removes_generated_note_not_original_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            original = Path(tmp) / "urls.txt"
            original.write_text("https://example.com/a", encoding="utf-8")
            state_path = Path(tmp) / "import_state.json"
            config = BuilderConfig(vault_path=vault, dry_run=False)
            records = [
                {
                    "id": "url-1",
                    "source_url": "https://example.com/a",
                    "original_path": str(original),
                    "filename": "Example URL",
                    "suggested_destination": "60 Resources/Websites",
                    "suggested_area": "Resource",
                    "suggested_project": "",
                    "pii_risk": "low",
                    "secret_risk": False,
                    "import_action": "metadata_note",
                    "needs_manual_review": False,
                    "hash": "abc123",
                }
            ]
            batch = execute_import(records, config, state_path=state_path)

            removed = rollback_batch(config, state_path=state_path, batch_id=batch["batch_id"])

            self.assertEqual(len(removed), 1)
            self.assertFalse(Path(batch["created_files"][0]).exists())
            self.assertTrue(original.exists())

    def test_importable_records_filters_manual_review_and_high_risk(self):
        records = [
            {"id": "ok", "import_action": "metadata_note", "needs_manual_review": "False", "pii_risk": "low", "secret_risk": "False"},
            {"id": "review", "import_action": "metadata_note", "needs_manual_review": "True", "pii_risk": "low", "secret_risk": "False"},
            {"id": "high", "import_action": "metadata_note", "needs_manual_review": "False", "pii_risk": "high", "secret_risk": "False"},
        ]

        result = importable_records(records)

        self.assertEqual([record["id"] for record in result], ["ok"])


if __name__ == "__main__":
    unittest.main()
