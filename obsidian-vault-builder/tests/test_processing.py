import tempfile
import unittest
from pathlib import Path

from vault_builder.processing import classify_inventory_records, extract_text_file


class ProcessingTests(unittest.TestCase):
    def test_classify_inventory_records_updates_area_project_confidence(self):
        records = [
            {
                "filename": "docmind shopify seo roadmap.md",
                "original_path": "/tmp/docmind shopify seo roadmap.md",
                "source_name": "Sample",
            }
        ]

        result = classify_inventory_records(records)

        self.assertEqual(result[0]["suggested_project"], "DocMind")
        self.assertEqual(result[0]["suggested_area"], "Content")
        self.assertIn(result[0]["classification_confidence"], {"medium", "high"})

    def test_extract_text_file_truncates_plain_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "note.txt"
            source.write_text("abcdef", encoding="utf-8")

            result = extract_text_file(source, max_chars=3)

            self.assertEqual(result.text, "abc")
            self.assertTrue(result.truncated)
            self.assertEqual(result.error, "")

    def test_extract_text_file_returns_friendly_unsupported_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "binary.bin"
            source.write_bytes(b"\x00\x01")

            result = extract_text_file(source)

            self.assertEqual(result.text, "")
            self.assertIn("Unsupported", result.error)


if __name__ == "__main__":
    unittest.main()
