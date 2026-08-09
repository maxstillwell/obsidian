import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.gates import write_gate_status


class GateStatusTests(unittest.TestCase):
    def test_write_gate_status_records_disabled_network_and_gate_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(
                vault_path=Path(tmp) / "vault",
                allow_network=False,
                read_file_contents=False,
                sources=[{"name": "URL List", "enabled": True}],
            )

            report = write_gate_status(config, inventory_count=0, imported_count=0)

            text = report.read_text(encoding="utf-8")
            self.assertIn("Gate A", text)
            self.assertIn("URL List", text)
            self.assertIn("Network allowed: False", text)

    def test_write_gate_status_reports_completed_public_import_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = BuilderConfig(
                vault_path=Path(tmp) / "vault",
                allow_network=True,
                read_file_contents=False,
                sources=[{"name": "URL List", "enabled": True}],
            )

            report = write_gate_status(config, inventory_count=15, imported_count=11)

            text = report.read_text(encoding="utf-8")
            self.assertIn("Current importable public-source records have been imported.", text)
            self.assertNotIn("Confirm before generating a detailed import plan", text)


if __name__ == "__main__":
    unittest.main()
