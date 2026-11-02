import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.gtm_operating_panel import MANAGED_MARKER_START, write_gtm_operating_panel


class GTMOperatingPanelTests(unittest.TestCase):
    def test_write_gtm_operating_panel_creates_dashboard_queue_templates_and_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")

            written = write_gtm_operating_panel(config)

            dashboard = config.vault_path / "10 Projects/DocMind/DocMind GTM Dashboard.md"
            rhythm = config.vault_path / "10 Projects/DocMind/DocMind Daily Operating Rhythm.md"
            queue = config.vault_path / "30 Content/DocMind Publish Queue.md"
            interview_log = config.vault_path / "40 Meetings & People/Customer Calls/DocMind Customer Interview Log.md"
            lead_tracker = config.vault_path / "40 Meetings & People/People/DocMind Lead Follow-Up Tracker.md"
            interview_template = config.vault_path / "_Templates/DocMind Customer Interview Template.md"
            lead_template = config.vault_path / "_Templates/DocMind Lead Follow-Up Template.md"
            context = config.vault_path / "_Context Packs/docmind-gtm-context.md"
            base = config.vault_path / "80 Databases/DocMind GTM.base"

            written_paths = {path.resolve() for path in written}
            self.assertIn(dashboard.resolve(), written_paths)
            self.assertIn(rhythm.resolve(), written_paths)
            self.assertIn(queue.resolve(), written_paths)
            self.assertIn(interview_log.resolve(), written_paths)
            self.assertIn(lead_tracker.resolve(), written_paths)
            self.assertIn(interview_template.resolve(), written_paths)
            self.assertIn(lead_template.resolve(), written_paths)
            self.assertIn(context.resolve(), written_paths)
            self.assertIn(base.resolve(), written_paths)
            self.assertIn("Scoreboard", dashboard.read_text(encoding="utf-8"))
            self.assertIn("Publish Definition", queue.read_text(encoding="utf-8"))
            self.assertIn("Do not import inboxes", lead_tracker.read_text(encoding="utf-8"))
            self.assertIn("Copy-Ready DocMind GTM Context", context.read_text(encoding="utf-8"))

    def test_write_gtm_operating_panel_is_idempotent_and_preserves_manual_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(vault_path=Path(tmp) / "vault")
            target = config.vault_path / "10 Projects/DocMind/DocMind GTM Dashboard.md"
            target.parent.mkdir(parents=True)
            target.write_text("# DocMind GTM Dashboard\n\nManual note stays.\n", encoding="utf-8")

            write_gtm_operating_panel(config)
            write_gtm_operating_panel(config)

            text = target.read_text(encoding="utf-8")
            self.assertIn("Manual note stays.", text)
            self.assertEqual(text.count(MANAGED_MARKER_START), 1)


if __name__ == "__main__":
    unittest.main()
