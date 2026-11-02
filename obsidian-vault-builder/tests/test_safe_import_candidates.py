import tempfile
import unittest
from pathlib import Path

from vault_builder.safe_import_candidates import candidate_groups, write_safe_import_candidates


class SafeImportCandidatesTests(unittest.TestCase):
    def test_candidate_groups_keep_low_risk_non_hidden_directories(self):
        home = Path("/tmp/home")
        records = [
            _record(home / "Projects/Research/brief.md", action="convert_to_note", area="Research"),
            _record(home / "Projects/Research/map.pdf", action="extract_text_to_note", area="Research"),
            _record(home / ".ssh/config", action="metadata_note"),
            _record(home / "Downloads/random.md", action="convert_to_note"),
            _record(home / "obsidian/FounderOS/Home.md", action="convert_to_note"),
            _record(home / "obsidian/FounderOS.md", action="convert_to_note"),
            _record(home / "Desktop/客户项目/passport.pdf", action="extract_text_to_note"),
            _record(home / "Projects/Legal/title.pdf", action="extract_text_to_note"),
            _record(home / "Projects/Finance/tax-return.pdf", action="extract_text_to_note"),
            _record(home / "Projects/Research/duplicate.md", action="convert_to_note", duplicate_of="first"),
            _record(home / "Projects/Secret/high.md", risk="high", action="convert_to_note"),
            _record(home / "Projects/Manual/unknown.bin", manual=True, action="needs_review"),
        ]

        groups = candidate_groups(records, home_path=home)

        self.assertEqual(len(groups), 1)
        group = groups[0]
        self.assertEqual(group.relative_dir, "Projects/Research")
        self.assertEqual(group.record_count, 2)
        self.assertEqual(group.actions["convert_to_note"], 1)
        self.assertEqual(group.actions["extract_text_to_note"], 1)

    def test_write_safe_import_candidates_creates_local_review_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            output = Path(tmp) / "SAFE_IMPORT_CANDIDATES.md"
            records = [
                _record(home / "Projects/Research/brief.md", action="convert_to_note", area="Research"),
                _record(home / "Projects/Research/map.pdf", action="extract_text_to_note", area="Research"),
                _record(home / "Desktop/客户项目/passport.pdf", action="extract_text_to_note"),
            ]

            report = write_safe_import_candidates(records, output, home_path=home)

            text = report.read_text(encoding="utf-8")
            self.assertIn("SAFE_IMPORT_CANDIDATES", text)
            self.assertIn("Candidate directories: 1", text)
            self.assertIn("Projects/Research", text)
            self.assertIn("Do not run full-home import directly", text)
            self.assertNotIn("Desktop/客户项目", text)

    def test_candidate_groups_prioritize_note_like_directories_over_attachment_only_directories(self):
        home = Path("/tmp/home")
        records = [_record(home / f"Images/Extracted/image-{index}.jpg", action="index_only") for index in range(20)]
        records.extend(
            [
                _record(home / "Projects/Docs/README.md", action="convert_to_note"),
                _record(home / "Projects/Docs/Brief.pdf", action="extract_text_to_note"),
            ]
        )

        groups = candidate_groups(records, home_path=home)

        self.assertEqual(groups[0].relative_dir, "Projects/Docs")
        self.assertEqual(groups[0].note_record_count, 2)


def _record(
    path: Path,
    action: str,
    risk: str = "medium",
    area: str = "Resource",
    manual: bool = False,
    duplicate_of: str = "",
) -> dict:
    return {
        "id": str(path),
        "original_path": str(path),
        "filename": path.name,
        "extension": path.suffix,
        "suggested_area": area,
        "suggested_project": "",
        "import_action": action,
        "needs_manual_review": manual,
        "pii_risk": risk,
        "secret_risk": False,
        "duplicate_of": duplicate_of,
    }


if __name__ == "__main__":
    unittest.main()
