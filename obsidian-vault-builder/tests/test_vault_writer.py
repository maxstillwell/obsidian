import tempfile
import unittest
from pathlib import Path

from vault_builder.vault_writer import create_vault


class VaultWriterTests(unittest.TestCase):
    def test_create_vault_writes_required_base_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "FounderOS"

            create_vault(vault)

            expected = [
                "Projects.base",
                "Content.base",
                "Meetings.base",
                "Research.base",
                "People.base",
                "Decisions.base",
                "Sources.base",
            ]
            for filename in expected:
                base = vault / "80 Databases" / filename
                self.assertTrue(base.exists(), filename)
                text = base.read_text(encoding="utf-8")
                self.assertIn("views:", text)
                self.assertIn("type: table", text)


if __name__ == "__main__":
    unittest.main()
