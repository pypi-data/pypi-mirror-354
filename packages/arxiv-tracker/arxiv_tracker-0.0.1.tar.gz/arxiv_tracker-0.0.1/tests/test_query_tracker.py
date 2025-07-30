import unittest
from arxiv_tracker.query_tracker import QueryTracker


class TestQueryTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = QueryTracker(["machine learning"])

    def test_init(self):
        self.assertEqual(self.tracker.keywords, ["machine learning"])
        self.assertEqual(self.tracker.base_url, 'http://export.arxiv.org/api/query?')

    def test_fetch(self):
        papers = self.tracker.fetch(max_results=5)
        self.assertIsInstance(papers, list)
        if papers:
            self.assertIsInstance(papers[0], dict)
            self.assertTrue('id' in papers[0])
