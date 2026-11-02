import tempfile
import unittest
from pathlib import Path
import hashlib
from unittest.mock import patch

from vault_builder.config import BuilderConfig
from vault_builder.scanner import dry_run_scan
from vault_builder.web_metadata import URLMetadata
from vault_builder.sanitize import safe_join


class PathSafetyTests(unittest.TestCase):
    def test_safe_join_does_not_write_outside_vault(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            with self.assertRaises(ValueError):
                safe_join(vault, '../../escape.md')

    def test_dry_run_does_not_create_import_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source'
            vault = root / 'vault'
            source.mkdir()
            (source / 'docmind-roadmap.md').write_text('do not read in dry run', encoding='utf-8')
            config = BuilderConfig(
                vault_path=vault,
                dry_run=True,
                read_file_contents=False,
                sources=[
                    {
                        'name': 'Test Source',
                        'type': 'folder',
                        'path_or_url': str(source),
                        'enabled': True,
                        'destination': '00 Inbox',
                        'privacy_level': 'low',
                    }
                ],
            )

            records = dry_run_scan(config)

            self.assertEqual(len(records), 1)
            self.assertFalse(vault.exists())
            self.assertEqual(records[0]['original_path'], str(source / 'docmind-roadmap.md'))

    def test_dry_run_preserves_original_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            original = source / 'meeting-notes.txt'
            original.write_text('private body should not be read', encoding='utf-8')
            config = BuilderConfig(
                vault_path=Path(tmp) / 'vault',
                dry_run=True,
                read_file_contents=False,
                sources=[
                    {
                        'name': 'Test Source',
                        'type': 'folder',
                        'path_or_url': str(source),
                        'enabled': True,
                        'destination': '00 Inbox',
                        'privacy_level': 'low',
                    }
                ],
            )

            records = dry_run_scan(config)

            self.assertEqual(records[0]['original_path'], str(original))
            self.assertTrue(original.exists())

    def test_url_list_dry_run_does_not_use_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            urls = Path(tmp) / 'urls.txt'
            urls.write_text('# comment\nhttps://example.com/page\n\n', encoding='utf-8')
            config = BuilderConfig(
                vault_path=Path(tmp) / 'vault',
                dry_run=True,
                allow_network=False,
                sources=[
                    {
                        'name': 'URL List',
                        'type': 'url_list',
                        'path_or_url': str(urls),
                        'enabled': True,
                        'destination': '60 Resources/Websites',
                        'privacy_level': 'low',
                    }
                ],
            )

            records = dry_run_scan(config)

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['source_url'], 'https://example.com/page')
            self.assertFalse(records[0]['can_read_content'])
            self.assertEqual(records[0]['hash'], hashlib.sha256(b'https://example.com/page').hexdigest())

    def test_file_hash_only_when_content_reading_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            file_path = source / 'safe-note.txt'
            file_path.write_text('hello', encoding='utf-8')
            config = BuilderConfig(
                vault_path=Path(tmp) / 'vault',
                dry_run=True,
                read_file_contents=True,
                sources=[
                    {
                        'name': 'Safe Source',
                        'type': 'folder',
                        'path_or_url': str(source),
                        'enabled': True,
                        'destination': '00 Inbox',
                        'privacy_level': 'low',
                    }
                ],
            )

            records = dry_run_scan(config)

            self.assertEqual(records[0]['hash'], hashlib.sha256(b'hello').hexdigest())

    def test_sensitive_file_is_not_hashed_even_when_content_reading_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            (source / '.env').write_text('SECRET=value', encoding='utf-8')
            config = BuilderConfig(
                vault_path=Path(tmp) / 'vault',
                dry_run=True,
                read_file_contents=True,
                sources=[
                    {
                        'name': 'Sensitive Source',
                        'type': 'folder',
                        'path_or_url': str(source),
                        'enabled': True,
                        'destination': '00 Inbox',
                        'privacy_level': 'low',
                    }
                ],
            )

            records = dry_run_scan(config)

            self.assertEqual(records[0]['pii_risk'], 'critical')
            self.assertEqual(records[0]['hash'], '')

    def test_non_2xx_url_metadata_requires_manual_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            urls = Path(tmp) / 'urls.txt'
            urls.write_text('https://example.com/protected\n', encoding='utf-8')
            config = BuilderConfig(
                vault_path=Path(tmp) / 'vault',
                dry_run=True,
                allow_network=True,
                sources=[
                    {
                        'name': 'URL List',
                        'type': 'url_list',
                        'path_or_url': str(urls),
                        'enabled': True,
                        'destination': '60 Resources/Websites',
                        'privacy_level': 'low',
                    }
                ],
            )
            with patch('vault_builder.scanner.fetch_url_metadata') as fetch:
                fetch.return_value = URLMetadata(True, '403', 'text/html', 'Verifying your connection', 'HTTP Error 403')

                records = dry_run_scan(config)

            self.assertTrue(records[0]['needs_manual_review'])
            self.assertEqual(records[0]['import_action'], 'needs_review')


if __name__ == '__main__':
    unittest.main()
