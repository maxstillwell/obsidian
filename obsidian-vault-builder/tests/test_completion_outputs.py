import tempfile
import unittest
from pathlib import Path

from vault_builder.completion_outputs import MANAGED_MARKER_START, write_completion_outputs
from vault_builder.config import BuilderConfig


class CompletionOutputTests(unittest.TestCase):
    def test_write_completion_outputs_creates_manual_and_completion_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")

            written = write_completion_outputs(config, inventory_count=31, source_count=26, manual_review_count=0)

            manual = config.vault_path / "_System/OPERATING_MANUAL.md"
            complete = config.vault_path / "_System/SETUP_COMPLETE.md"
            self.assertIn(manual.resolve(), {path.resolve() for path in written})
            self.assertIn(complete.resolve(), {path.resolve() for path in written})
            self.assertIn("Daily operating loop", manual.read_text(encoding="utf-8"))
            self.assertIn("Setup status: complete", complete.read_text(encoding="utf-8"))

    def test_write_completion_outputs_preserves_manual_home_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")
            home = config.vault_path / "Home.md"
            home.parent.mkdir(parents=True)
            home.write_text("# FounderOS\n\nManual note stays.\n", encoding="utf-8")

            write_completion_outputs(config, inventory_count=31, source_count=26, manual_review_count=0)
            write_completion_outputs(config, inventory_count=31, source_count=26, manual_review_count=0)

            text = home.read_text(encoding="utf-8")
            self.assertIn("Manual note stays.", text)
            self.assertEqual(text.count(MANAGED_MARKER_START), 1)


if __name__ == "__main__":
    unittest.main()
