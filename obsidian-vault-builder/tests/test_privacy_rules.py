import unittest

from vault_builder.privacy import assess_privacy


class PrivacyRuleTests(unittest.TestCase):
    def test_env_file_is_critical_and_skipped(self):
        result = assess_privacy('/tmp/project/.env')
        self.assertEqual(result.level, 'critical')
        self.assertEqual(result.import_action, 'skip')

    def test_ssh_private_key_is_critical_and_skipped(self):
        result = assess_privacy('/Users/me/.ssh/id_rsa')
        self.assertEqual(result.level, 'critical')
        self.assertTrue(result.needs_manual_review)

    def test_credentials_json_is_critical_and_skipped(self):
        result = assess_privacy('/tmp/credentials.json')
        self.assertEqual(result.level, 'critical')
        self.assertEqual(result.import_action, 'skip')

    def test_bank_tax_passport_keywords_are_sensitive(self):
        for path in ('bank-statement.pdf', 'tax-return.pdf', 'passport-scan.pdf'):
            result = assess_privacy(path)
            self.assertIn(result.level, ('high', 'critical'))
            self.assertTrue(result.needs_manual_review)


if __name__ == '__main__':
    unittest.main()
