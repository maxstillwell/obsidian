import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.docmind_execution_pack import MANAGED_MARKER_START, write_docmind_execution_pack


class DocMindExecutionPackTests(unittest.TestCase):
    def test_write_docmind_execution_pack_creates_plan_briefs_workflow_and_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")

            written = write_docmind_execution_pack(config)

            plan = config.vault_path / "10 Projects/DocMind/DocMind 7-Day Execution Plan.md"
            demo = config.vault_path / "50 AI Prompts & Workflows/DocMind Demo Workflow.md"
            demo_script = config.vault_path / "50 AI Prompts & Workflows/DocMind Demo Script.md"
            context = config.vault_path / "_Context Packs/docmind-execution-context.md"
            landing = config.vault_path / "30 Content/Drafts/DocMind Landing Page Draft.md"
            discovery = config.vault_path / "10 Projects/DocMind/Customer Discovery Questionnaire.md"
            order_status = config.vault_path / "30 Content/SEO Briefs/Order Status Support Automation Brief.md"
            self.assertIn(plan.resolve(), {path.resolve() for path in written})
            self.assertIn(demo.resolve(), {path.resolve() for path in written})
            self.assertIn(demo_script.resolve(), {path.resolve() for path in written})
            self.assertIn(context.resolve(), {path.resolve() for path in written})
            self.assertIn(landing.resolve(), {path.resolve() for path in written})
            self.assertIn(discovery.resolve(), {path.resolve() for path in written})
            self.assertIn(order_status.resolve(), {path.resolve() for path in written})
            self.assertIn("Day 1", plan.read_text(encoding="utf-8"))
            self.assertIn("source-grounded answer", demo.read_text(encoding="utf-8"))
            self.assertIn("Hero", landing.read_text(encoding="utf-8"))
            self.assertIn("Discovery questions", discovery.read_text(encoding="utf-8"))

    def test_write_docmind_execution_pack_is_idempotent_and_preserves_manual_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")
            target = config.vault_path / "10 Projects/DocMind/DocMind 7-Day Execution Plan.md"
            target.parent.mkdir(parents=True)
            target.write_text("# DocMind 7-Day Execution Plan\n\nManual note stays.\n", encoding="utf-8")

            write_docmind_execution_pack(config)
            write_docmind_execution_pack(config)

            text = target.read_text(encoding="utf-8")
            self.assertIn("Manual note stays.", text)
            self.assertEqual(text.count(MANAGED_MARKER_START), 1)


if __name__ == "__main__":
    unittest.main()
