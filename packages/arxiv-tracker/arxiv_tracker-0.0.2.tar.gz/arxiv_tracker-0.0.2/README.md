# ArXiv Tracker

A Python package for tracking new papers on arXiv based on keywords.

## Features

- Track papers based on keywords
- Automatic deduplication
- Save papers to CSV
- Configurable check interval

## Installation

```bash
pip install arxiv-tracker
```

## Usage

```text
from arxiv_tracker.query_tracker import QueryTracker

tracker = QueryTracker(["machine learning"])
papers = tracker.fetch(max_results=60)
```

```text
from arxiv_tracker.rss_tracker import RSSTracker

rss_url = f"http://export.arxiv.org/rss/cs.AI"
tracker = RSSTracker(rss_url=rss_url)
papers = tracker.fetch()
```

---

## Development

- install & test

```text
pip install -e .
python -m unittest discover tests
```

- build & upload to TestPyPI

```text
python -m build
twine upload --repository testpypi dist/*  -u__token__ -p <your_token>
```