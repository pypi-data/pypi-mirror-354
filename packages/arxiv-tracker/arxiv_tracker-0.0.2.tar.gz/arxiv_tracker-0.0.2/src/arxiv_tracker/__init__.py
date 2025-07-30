from arxiv_tracker.query_tracker import QueryTracker
from arxiv_tracker.rss_tracker import RSSTracker

try:
    from importlib.metadata import version
except ImportError:  # For Python<3.8
    from importlib_metadata import version

__version__ = version("arxiv-tracker")
__all__ = ["QueryTracker", "RSSTracker"]
