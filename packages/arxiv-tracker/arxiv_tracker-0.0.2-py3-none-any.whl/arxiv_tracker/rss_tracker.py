# rss_fetcher.py
import feedparser


class RSSTracker:
    def __init__(self, rss_url: str):
        self.rss_url = rss_url

    def fetch(self):
        """
        拉取 RSS 并解析成论文条目列表

        :return: List[dict]，每个 dict 包含论文基本信息
        """
        feed = feedparser.parse(self.rss_url)
        papers = []
        for entry in feed.entries:
            paper = {
                "id": self._extract_arxiv_id(entry.link),
                "title": entry.title,
                "link": entry.link,
                'authors': ', '.join(author.name for author in entry.authors),
                "published": entry.published,
                "summary": entry.summary,
                "category": entry.category,
            }
            papers.append(paper)
        return papers

    def _extract_arxiv_id(self, url: str) -> str:
        # 假设 url 格式如 https://arxiv.org/abs/2405.12345
        # 简单切割，返回最后一部分作为 arxiv_id
        return url.rstrip('/').split('/')[-1]
