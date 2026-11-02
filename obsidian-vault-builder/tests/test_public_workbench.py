import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.public_workbench import MANAGED_MARKER_START, write_public_workbench


class PublicWorkbenchTests(unittest.TestCase):
    def test_write_public_workbench_creates_key_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")

            written = write_public_workbench(config)

            docmind = config.vault_path / "10 Projects/DocMind/DocMind Home.md"
            ai_workflows = config.vault_path / "50 AI Prompts & Workflows/AI Workflow Library.md"
            written_resolved = {path.resolve() for path in written}
            self.assertIn(docmind.resolve(), written_resolved)
            self.assertIn(ai_workflows.resolve(), written_resolved)
            self.assertIn("Shopify support automation", docmind.read_text(encoding="utf-8"))
            self.assertIn("Codex implementation loop", ai_workflows.read_text(encoding="utf-8"))

    def test_write_public_workbench_preserves_unmanaged_content_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")
            target = config.vault_path / "10 Projects/DocMind/DocMind Home.md"
            target.parent.mkdir(parents=True)
            target.write_text("# DocMind Home\n\nManual note stays.\n", encoding="utf-8")

            write_public_workbench(config)
            write_public_workbench(config)

            text = target.read_text(encoding="utf-8")
            self.assertIn("Manual note stays.", text)
            self.assertEqual(text.count(MANAGED_MARKER_START), 1)


if __name__ == "__main__":
    unittest.main()
