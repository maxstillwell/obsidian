import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig, load_config
from vault_builder.preflight import validate_scan_scope


class PreflightScopeTests(unittest.TestCase):
    def test_load_config_reads_exclude_dirs_for_full_home_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "sources.full-home.yaml"
            config_path.write_text(
                """
vault:
  path: "/tmp/vault"

settings:
  dry_run: true
  read_file_contents: false
  exclude_dirs:
    - Library
    - .ssh

sources:
  - name: "Full Home Metadata Index"
    type: "folder"
    path_or_url: "~"
    enabled: true
    destination: "00 Inbox"
    privacy_level: "medium"
""",
                encoding="utf-8",
            )

            config = load_config(config_path)

            self.assertIn("Library", config.exclude_dirs)
            self.assertIn(".ssh", config.exclude_dirs)

    def test_validate_scan_scope_blocks_home_scan_without_required_exclusions(self):
        config = BuilderConfig(
            vault_path=Path("/tmp/vault"),
            dry_run=True,
            read_file_contents=False,
            sources=[
                {
                    "name": "Unsafe Home",
                    "type": "folder",
                    "path_or_url": "~",
                    "enabled": True,
                    "destination": "00 Inbox",
                    "privacy_level": "medium",
                }
            ],
        )

        result = validate_scan_scope(config)

        self.assertFalse(result.ok)
        self.assertTrue(any("Library" in error for error in result.errors))

    def test_validate_scan_scope_allows_metadata_only_home_scan_with_required_exclusions(self):
        required = {
            "Library",
            ".ssh",
            ".gnupg",
            ".1password",
            ".Trash",
            "Mail",
            "Messages",
            "Keychains",
            "Application Support",
            ".codex",
            ".claude",
            ".claudian",
            ".gemini",
            ".antigravity",
            ".antigravity_cockpit",
            "codex_home",
            "User Data",
        }
        config = BuilderConfig(
            vault_path=Path("/tmp/vault"),
            dry_run=True,
            read_file_contents=False,
            allow_online_ai=False,
            allow_ocr=False,
            allow_transcription=False,
            copy_attachments=False,
            exclude_dirs=required,
            sources=[
                {
                    "name": "Full Home Metadata Index",
                    "type": "folder",
                    "path_or_url": "~",
                    "enabled": True,
                    "destination": "00 Inbox",
                    "privacy_level": "medium",
                }
            ],
        )

        result = validate_scan_scope(config)

        self.assertTrue(result.ok, result.errors)

    def test_validate_scan_scope_requires_ai_state_directory_exclusions(self):
        required_without_gemini = {
            "Library",
            ".ssh",
            ".gnupg",
            ".1password",
            ".Trash",
            "Mail",
            "Messages",
            "Keychains",
            "Application Support",
            ".codex",
            ".claude",
            ".claudian",
            ".antigravity",
            ".antigravity_cockpit",
            "codex_home",
            "User Data",
        }
        config = BuilderConfig(
            vault_path=Path("/tmp/vault"),
            dry_run=True,
            read_file_contents=False,
            exclude_dirs=required_without_gemini,
            sources=[
                {
                    "name": "Full Home Metadata Index",
                    "type": "folder",
                    "path_or_url": "~",
                    "enabled": True,
                    "destination": "00 Inbox",
                    "privacy_level": "medium",
                }
            ],
        )

        result = validate_scan_scope(config)

        self.assertFalse(result.ok)
        self.assertTrue(any(".gemini" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
