# ArXiv Tracker

A Python package for tracking new papers on arXiv based on keywords.

## Installation

```bash
pip install arxiv-tracker
```

## Usage

```text
from arxiv_tracker import ArxivTracker

# Initialize tracker with keywords
tracker = ArxivTracker(["machine learning", "deep learning"])

# Start tracking with custom interval (in minutes)
tracker.track(interval_minutes=60)
```

## Features

- Track papers based on keywords
- Automatic deduplication
- Save papers to CSV
- Configurable check interval

```text
from arxiv_tracker import ArxivTracker
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