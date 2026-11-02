import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.final_report import current_imported_note_count, write_final_report
from vault_builder.reports import write_privacy_review


class FinalReportTests(unittest.TestCase):
    def test_write_final_report_summarizes_safe_current_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            config = BuilderConfig(vault_path=vault, sources=[{"name": "URL List", "enabled": True}])
            report = write_final_report(config, inventory_count=0, imported_count=0)

            text = report.read_text(encoding="utf-8")
            self.assertIn("Final Report", text)
            self.assertIn("URL List", text)
            self.assertIn("Imported notes: 0", text)

    def test_write_final_report_describes_public_url_phase_after_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            config = BuilderConfig(vault_path=vault, allow_network=True, sources=[{"name": "URL List", "enabled": True}])

            report = write_final_report(config, inventory_count=15, imported_count=11)

            text = report.read_text(encoding="utf-8")
            self.assertIn("Public URL source phase is active", text)
            self.assertIn("Private/local folders remain disabled", text)
            self.assertIn("Manual review queue remains available", text)
            self.assertNotIn("Manual review records remain", text)

    def test_current_imported_note_count_excludes_rolled_back_batches(self):
        state = {
            "batches": [
                {"created_files": ["one.md", "two.md"], "rolled_back_at": "2026-06-02T22:00:00"},
                {"created_files": ["three.md"]},
            ]
        }

        self.assertEqual(current_imported_note_count(state), 1)

    def test_write_privacy_review_updates_vault_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            config = BuilderConfig(vault_path=vault)
            records = [
                {"original_path": "safe.md", "pii_risk": "low", "needs_manual_review": False, "import_action": "metadata_note"},
                {
                    "original_path": ".env",
                    "pii_risk": "critical",
                    "secret_risk": True,
                    "needs_manual_review": True,
                    "import_action": "skip",
                    "import_reason": "secret-like file",
                },
            ]

            report = write_privacy_review(records, config)

            text = report.read_text(encoding="utf-8")
            self.assertIn("Inventory rows: 2", text)
            self.assertIn("Critical rows: 1", text)
            self.assertIn("Secret-Like Files", text)
            self.assertIn("`.env`", text)


if __name__ == "__main__":
    unittest.main()
