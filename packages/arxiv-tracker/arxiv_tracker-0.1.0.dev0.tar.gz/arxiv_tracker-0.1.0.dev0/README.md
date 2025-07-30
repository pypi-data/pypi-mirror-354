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
安装和使用：
1. 在包目录下运行: `pip install -e .`
2. 使用示例:
```python
from arxiv_tracker import ArxivTracker

tracker = ArxivTracker(["machine learning"])
tracker.track(interval_minutes=60)
```
