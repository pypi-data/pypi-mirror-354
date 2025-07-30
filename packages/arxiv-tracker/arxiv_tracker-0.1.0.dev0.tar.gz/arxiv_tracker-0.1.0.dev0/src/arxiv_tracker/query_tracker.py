import feedparser
import pandas as pd
import time
from datetime import datetime
import os
from typing import List, Dict, Set
from urllib.parse import quote


class QueryTracker:
    def __init__(self, keywords: List[str], save_path: str = 'arxiv_papers.csv') -> None:
        self.keywords = [k.lower() for k in keywords]
        self.save_path = save_path
        self.base_url = 'http://export.arxiv.org/api/query?'
        self.seen_papers: Set[str] = set()

        if os.path.exists(self.save_path):
            df = pd.read_csv(self.save_path)
            self.seen_papers = set(df['id'].tolist())

    def fetch_papers(self, max_results: int = 100) -> List[Dict]:
        # Properly encode keywords for URL
        encoded_keywords = '+OR+'.join(quote(k) for k in self.keywords)
        query = f"search_query=all:{encoded_keywords}&sortBy=lastUpdatedDate&sortOrder=descending&max_results={max_results}"
        feed = feedparser.parse(self.base_url + query)

        new_papers = []
        for entry in feed.entries:
            paper_id = entry.id.split('/abs/')[-1]

            if paper_id not in self.seen_papers:
                paper = {
                    'id': paper_id,
                    'title': entry.title,
                    'authors': ', '.join(author.name for author in entry.authors),
                    'summary': entry.summary,
                    "category": entry.category,
                    'published': entry.published,
                    'link': entry.link
                }
                new_papers.append(paper)
                self.seen_papers.add(paper_id)

        return new_papers

    def save_papers(self, papers: List[Dict]) -> None:
        if papers:
            df = pd.DataFrame(papers)
            if os.path.exists(self.save_path):
                existing_df = pd.read_csv(self.save_path)
                df = pd.concat([existing_df, df], ignore_index=True)
            df.to_csv(self.save_path, index=False)
            print(f"Saved {len(papers)} new papers")

    def track(self, interval_minutes: int = 60) -> None:
        while True:
            print(f"\nChecking for new papers at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            new_papers = self.fetch_papers()
            self.save_papers(new_papers)
            time.sleep(interval_minutes * 60)
