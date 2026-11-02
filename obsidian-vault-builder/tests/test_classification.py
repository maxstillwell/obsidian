import unittest

from vault_builder.classification import classify_metadata


class ClassificationTests(unittest.TestCase):
    def test_docmind_file_classifies_to_docmind(self):
        result = classify_metadata('docmind shopify customer support roadmap.md')
        self.assertEqual(result.project, 'DocMind')

    def test_221b_file_classifies_to_221b(self):
        result = classify_metadata('221b ai search citation verification.md')
        self.assertEqual(result.project, '221B')

    def test_seo_blog_file_classifies_to_content(self):
        result = classify_metadata('seo blog brief for ai support.md')
        self.assertEqual(result.area, 'Content')

    def test_meeting_call_file_classifies_to_meetings(self):
        result = classify_metadata('customer call follow up notes.md')
        self.assertEqual(result.area, 'Meetings')

    def test_prompt_agent_codex_file_classifies_to_ai_workflows(self):
        result = classify_metadata('codex agent workflow prompt.md')
        self.assertEqual(result.area, 'AI Workflows')

    def test_claude_best_practices_classifies_to_ai_workflows(self):
        result = classify_metadata('https://code.claude.com/docs/en/best-practices', 'Best practices for Claude Code')
        self.assertEqual(result.area, 'AI Workflows')
        self.assertNotEqual(result.confidence, 'low')

    def test_claude_best_practices_url_only_classifies_to_ai_workflows(self):
        result = classify_metadata('https://code.claude.com/docs/en/best-practices')
        self.assertEqual(result.area, 'AI Workflows')
        self.assertNotEqual(result.confidence, 'low')

    def test_arxiv_citation_rag_paper_classifies_to_221b_research(self):
        result = classify_metadata('https://arxiv.org/abs/2412.18004', 'Correctness is not Faithfulness in RAG Attributions')
        self.assertEqual(result.project, '221B')
        self.assertEqual(result.area, 'Research')
        self.assertNotEqual(result.confidence, 'low')


if __name__ == '__main__':
    unittest.main()
