import json
import os
from pathlib import Path

from arxiv_tracker.rss_tracker import RSSTracker

if __name__ == "__main__":
    meta_dir = Path("./papers/meta")
    os.makedirs(meta_dir, exist_ok=True)

    # 可选的 arXiv 分类后缀（可以继续添加）
    ARXIV_CATEGORIES = [
        'cs.AI', 'stat.ML', 'cs.CL', 'cs.CV',
        'cs.RO', 'quant-ph', 'math', 'q-bio.NC'
    ]

    for cat in ARXIV_CATEGORIES:
        rss_url = f"http://export.arxiv.org/rss/{cat}"
        print(f"📡 Fetching {rss_url}")
        try:
            fetcher = RSSTracker(rss_url)
            papers = fetcher.fetch()
        except Exception as e:
            print(f"❌ Failed to fetch {cat}: {e}")
            continue

        print(f"✅ Fetched {len(papers)} papers from {cat}")

        for paper in papers:
            arxiv_id = paper["id"].split("/")[-1]  # 通常类似 '2405.12345'

            filename = f"{arxiv_id}.json"
            save_path = meta_dir / filename
            if save_path.exists():
                print(f"⏭️ Already exists: {filename}")
                continue

            # 加入元数据：rss_url
            paper["rss_url"] = rss_url

            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(paper, f, ensure_ascii=False, indent=2)
                print(f"✅ Saved: {filename}")
            except Exception as e:
                print(f"❌ Failed to save {filename}: {e}")
