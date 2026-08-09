import unittest
from pathlib import Path

from vault_builder.sanitize import safe_join, sanitize_filename, unique_filename


class SanitizeTests(unittest.TestCase):
    def test_sanitize_removes_illegal_filename_characters(self):
        self.assertEqual(sanitize_filename('Bad:Name/With\\Chars?.md'), 'Bad-Name-With-Chars.md')

    def test_unique_filename_adds_hash_for_existing_name(self):
        existing = {'Report.md'}
        result = unique_filename('Report.md', existing, content_hash='abcdef123456')
        self.assertEqual(result, 'Report-abcdef12.md')

    def test_unique_filename_treats_existing_names_case_insensitively(self):
        existing = {'templates - Obsidian Help.md'}
        result = unique_filename('Templates - Obsidian Help.md', existing, content_hash='abcdef123456')
        self.assertEqual(result, 'Templates - Obsidian Help-abcdef12.md')

    def test_safe_join_blocks_path_traversal(self):
        base = Path('/tmp/vault')
        with self.assertRaises(ValueError):
            safe_join(base, '../outside.md')


if __name__ == '__main__':
    unittest.main()
