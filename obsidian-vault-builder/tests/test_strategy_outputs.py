import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.strategy_outputs import MANAGED_MARKER_START, write_strategy_outputs


class StrategyOutputTests(unittest.TestCase):
    def test_write_strategy_outputs_creates_decisions_and_briefs(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")

            written = write_strategy_outputs(config)

            docmind_decision = config.vault_path / "10 Projects/DocMind/Decision - Support Automation Wedge.md"
            shopify_brief = config.vault_path / "30 Content/SEO Briefs/Shopify Support Automation Brief.md"
            self.assertIn(docmind_decision.resolve(), {path.resolve() for path in written})
            self.assertIn(shopify_brief.resolve(), {path.resolve() for path in written})
            self.assertIn("source-grounded support automation", docmind_decision.read_text(encoding="utf-8"))
            self.assertIn("Search Intent", shopify_brief.read_text(encoding="utf-8"))

    def test_write_strategy_outputs_is_idempotent_and_preserves_manual_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")
            target = config.vault_path / "10 Projects/DocMind/Decision - Support Automation Wedge.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Decision\n\nManual note stays.\n", encoding="utf-8")

            write_strategy_outputs(config)
            write_strategy_outputs(config)

            text = target.read_text(encoding="utf-8")
            self.assertIn("Manual note stays.", text)
            self.assertEqual(text.count(MANAGED_MARKER_START), 1)


if __name__ == "__main__":
    unittest.main()
