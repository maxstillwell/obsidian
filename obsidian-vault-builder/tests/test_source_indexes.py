import tempfile
import unittest
from pathlib import Path

from vault_builder.config import BuilderConfig
from vault_builder.source_indexes import MANAGED_MARKER_START, write_source_indexes


class SourceIndexTests(unittest.TestCase):
    def test_write_source_indexes_groups_source_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            note_dir = vault / "60 Resources/Websites"
            note_dir.mkdir(parents=True)
            (note_dir / "RAG Paper.md").write_text(
                "---\n"
                "type: source\n"
                "title: RAG Paper\n"
                "source_url: https://example.com/rag\n"
                "project: 221B\n"
                "area: Research\n"
                "status: imported\n"
                "---\n\n# RAG Paper\n",
                encoding="utf-8",
            )
            config = BuilderConfig(vault_path=vault)

            written = write_source_indexes(config)

            source_index = vault / "_Indexes/Source Index.md"
            research_index = vault / "_Indexes/Research Index.md"
            self.assertIn(source_index.resolve(), {path.resolve() for path in written})
            source_text = source_index.read_text(encoding="utf-8")
            self.assertIn("[[RAG Paper]]", source_text)
            self.assertIn("https://example.com/rag", source_text)
            self.assertIn("Research", research_index.read_text(encoding="utf-8"))

    def test_write_source_indexes_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            note_dir = vault / "60 Resources/Websites"
            note_dir.mkdir(parents=True)
            (note_dir / "Source.md").write_text("---\ntype: source\ntitle: Source\narea: AI Workflows\n---\n", encoding="utf-8")
            target = vault / "_Indexes/Source Index.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Source Index\n\nManual note stays.\n", encoding="utf-8")
            config = BuilderConfig(vault_path=vault)

            write_source_indexes(config)
            write_source_indexes(config)

            text = target.read_text(encoding="utf-8")
            self.assertIn("Manual note stays.", text)
            self.assertEqual(text.count(MANAGED_MARKER_START), 1)

    def test_source_index_uses_markdown_link_for_bracketed_filenames(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            note_dir = vault / "60 Resources/Websites"
            note_dir.mkdir(parents=True)
            (note_dir / "[2412.18004] Paper.md").write_text(
                "---\ntype: source\ntitle: RAG Attribution Paper\narea: Research\nproject: 221B\n---\n",
                encoding="utf-8",
            )

            write_source_indexes(BuilderConfig(vault_path=vault))

            text = (vault / "_Indexes/Source Index.md").read_text(encoding="utf-8")
            self.assertIn("[RAG Attribution Paper](../60 Resources/Websites/[2412.18004] Paper.md)", text)
            self.assertNotIn("[[[2412.18004] Paper]]", text)


if __name__ == "__main__":
    unittest.main()
