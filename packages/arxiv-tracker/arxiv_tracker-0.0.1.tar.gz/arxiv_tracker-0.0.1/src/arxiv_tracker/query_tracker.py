from typing import List, Dict, Set
from urllib.parse import quote

import feedparser


class QueryTracker:
    def __init__(self, keywords: List[str]) -> None:
        self.keywords = [k.lower() for k in keywords]
        self.base_url = 'http://export.arxiv.org/api/query?'
        self.papers_cache: Set[str] = set()

    def fetch(self, max_results: int = 100) -> List[Dict]:
        # Properly encode keywords for URL
        encoded_keywords = '+OR+'.join(quote(k) for k in self.keywords)
        query = f"search_query=all:{encoded_keywords}&sortBy=lastUpdatedDate&sortOrder=descending&max_results={max_results}"
        feed = feedparser.parse(self.base_url + query)

        papers = []
        for entry in feed.entries:
            paper_id = entry.id.split('/abs/')[-1]

            if paper_id not in self.papers_cache:
                paper = {
                    'id': paper_id,
                    'title': entry.title,
                    'authors': ', '.join(author.name for author in entry.authors),
                    'summary': entry.summary,
                    "category": entry.category,
                    'published': entry.published,
                    'link': entry.link
                }
                papers.append(paper)
                self.papers_cache.add(paper_id)

        return papers
