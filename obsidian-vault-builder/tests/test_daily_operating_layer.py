import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.daily_operating_layer import MANAGED_MARKER_START, write_daily_operating_layer


class DailyOperatingLayerTests(unittest.TestCase):
    def test_write_daily_operating_layer_creates_daily_dashboard_templates_and_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")

            written = write_daily_operating_layer(config)

            today = config.vault_path / "01 Daily Notes/Today.md"
            dashboard = config.vault_path / "01 Daily Notes/Founder Daily Dashboard.md"
            weekly = config.vault_path / "01 Daily Notes/Weekly Operating Review.md"
            source_queue = config.vault_path / "00 Inbox/Source Intake Queue.md"
            source_template = config.vault_path / "_Templates/Source Approval Plan Template.md"
            context = config.vault_path / "_Context Packs/daily-operating-context.md"
            base = config.vault_path / "80 Databases/Operating.base"

            written_paths = {path.resolve() for path in written}
            self.assertIn(today.resolve(), written_paths)
            self.assertIn(dashboard.resolve(), written_paths)
            self.assertIn(weekly.resolve(), written_paths)
            self.assertIn(source_queue.resolve(), written_paths)
            self.assertIn(source_template.resolve(), written_paths)
            self.assertIn(context.resolve(), written_paths)
            self.assertIn(base.resolve(), written_paths)
            self.assertIn("Today's Commitments", today.read_text(encoding="utf-8"))
            self.assertIn("Operating Stack", dashboard.read_text(encoding="utf-8"))
            self.assertIn("Approval Checklist", source_queue.read_text(encoding="utf-8"))
            self.assertIn("Copy-Ready Daily Operating Context", context.read_text(encoding="utf-8"))

    def test_write_daily_operating_layer_is_idempotent_and_preserves_manual_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")
            target = config.vault_path / "01 Daily Notes/Today.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Today\n\nManual note stays.\n", encoding="utf-8")

            write_daily_operating_layer(config)
            write_daily_operating_layer(config)

            text = target.read_text(encoding="utf-8")
            self.assertIn("Manual note stays.", text)
            self.assertEqual(text.count(MANAGED_MARKER_START), 1)


if __name__ == "__main__":
    unittest.main()
