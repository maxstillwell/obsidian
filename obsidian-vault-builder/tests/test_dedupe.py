import unittest
from unittest.mock import patch

from vault_builder import dedupe
from vault_builder.dedupe import mark_duplicates


class DedupeTests(unittest.TestCase):
    def test_marks_duplicate_hash_without_deleting_records(self):
        records = [
            {"id": "a", "hash": "same", "source_url": "", "filename": "one.md", "size_bytes": 10, "modified_time": "1"},
            {"id": "b", "hash": "same", "source_url": "", "filename": "two.md", "size_bytes": 10, "modified_time": "1"},
        ]

        result = mark_duplicates(records)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].get("duplicate_of"), "")
        self.assertEqual(result[1].get("duplicate_of"), "a")

    def test_marks_duplicate_source_url(self):
        records = [
            {"id": "a", "hash": "", "source_url": "https://example.com", "filename": "urls.txt"},
            {"id": "b", "hash": "", "source_url": "https://example.com", "filename": "urls.txt"},
        ]

        result = mark_duplicates(records)

        self.assertEqual(result[1].get("duplicate_of"), "a")

    def test_marks_similar_filename_with_close_size_and_modified_time(self):
        records = [
            {
                "id": "a",
                "hash": "",
                "source_url": "",
                "filename": "DocMind Support Audit v1.pdf",
                "size_bytes": "100000",
                "modified_time": "2026-06-03T00:00:00+00:00",
            },
            {
                "id": "b",
                "hash": "",
                "source_url": "",
                "filename": "DocMind Support Audit v2.pdf",
                "size_bytes": "101000",
                "modified_time": "2026-06-03T00:01:00+00:00",
            },
        ]

        result = mark_duplicates(records)

        self.assertEqual(result[1].get("duplicate_of"), "a")

    def test_does_not_mark_url_list_records_by_filename_only(self):
        records = [
            {
                "id": "a",
                "hash": "hash-a",
                "source_url": "https://example.com/a",
                "filename": "urls.txt",
                "size_bytes": "0",
                "modified_time": "",
            },
            {
                "id": "b",
                "hash": "hash-b",
                "source_url": "https://example.com/b",
                "filename": "urls.txt",
                "size_bytes": "0",
                "modified_time": "",
            },
        ]

        result = mark_duplicates(records)

        self.assertEqual(result[1].get("duplicate_of"), "")

    def test_marks_same_title_with_similar_summary(self):
        records = [
            {
                "id": "a",
                "hash": "",
                "source_url": "",
                "page_title": "Source Grounded Support Automation",
                "content_summary": "This article explains how cited answers, confidence levels, and escalation rules reduce support risk.",
            },
            {
                "id": "b",
                "hash": "",
                "source_url": "",
                "page_title": "Source Grounded Support Automation",
                "content_summary": "This article explains how cited answers, confidence levels, and escalation rules lower support risk.",
            },
        ]

        result = mark_duplicates(records)

        self.assertEqual(result[1].get("duplicate_of"), "a")

    def test_metadata_only_dedupe_limits_pairwise_similarity_checks(self):
        records = [
            {
                "id": f"record-{index}",
                "hash": "",
                "source_url": "",
                "filename": f"unique-file-{index}.pdf",
                "size_bytes": "100000",
                "modified_time": "2026-06-03T00:00:00+00:00",
            }
            for index in range(400)
        ]
        calls = 0
        original = dedupe._is_probable_duplicate

        def counted(record, candidate):
            nonlocal calls
            calls += 1
            return original(record, candidate)

        with patch("vault_builder.dedupe._is_probable_duplicate", side_effect=counted):
            result = mark_duplicates(records)

        self.assertEqual(len(result), 400)
        self.assertLess(calls, 500)


if __name__ == "__main__":
    unittest.main()
