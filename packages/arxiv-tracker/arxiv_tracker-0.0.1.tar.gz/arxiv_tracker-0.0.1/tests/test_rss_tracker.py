import unittest
from arxiv_tracker.rss_tracker import RSSTracker


class TestRSSTracker(unittest.TestCase):
    def setUp(self):
        cat = "cs.AI"
        self.rss_url = f"http://export.arxiv.org/rss/{cat}"
        self.tracker = RSSTracker(rss_url=self.rss_url)

    def test_init(self):
        self.assertEqual(self.tracker.rss_url, self.rss_url)

    def test_fetch(self):
        papers = self.tracker.fetch()
        self.assertIsInstance(papers, list)
        if papers:
            self.assertIsInstance(papers[0], dict)
            self.assertTrue('id' in papers[0])
