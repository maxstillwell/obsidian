import tempfile
import unittest
from pathlib import Path

from vault_builder.completion_audit import completion_checks, write_completion_audit
from vault_builder.config import BuilderConfig


class CompletionAuditTests(unittest.TestCase):
    def test_completion_audit_reports_missing_requirements(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vault = root / "vault"
            vault.mkdir()
            config = BuilderConfig(vault_path=vault)

            checks = completion_checks(config, [], root)

            self.assertTrue(any(check["status"] == "FAIL" for check in checks))
            self.assertTrue(any(check["requirement"] == "Inventory records exist" for check in checks))

    def test_write_completion_audit_creates_system_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vault = root / "vault"
            config = BuilderConfig(vault_path=vault)

            report = write_completion_audit(config, [], builder_root=root)

            text = report.read_text(encoding="utf-8")
            self.assertIn("COMPLETION_AUDIT", text)
            self.assertIn("Requirement Matrix", text)
            self.assertIn("Checks failed:", text)


if __name__ == "__main__":
    unittest.main()
