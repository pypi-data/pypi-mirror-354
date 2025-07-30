"""
Core browser functionality for background loading and URL handling.
"""

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal, QObject


class BackgroundLoader(QObject):
    """Handles background loading of web pages."""

    load_completed = pyqtSignal(bool, str, QWebEngineView)  # success, url, web_view

    def __init__(self):
        super().__init__()
        self.loading_views = []

    def load_url(self, url):
        """Load a URL in the background."""
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        print(f"Loading URL in background: {url}")

        # Create new hidden web view for background loading
        web_view = QWebEngineView()
        self.loading_views.append(web_view)

        # Connect load finished signal
        web_view.loadFinished.connect(
            lambda success: self._on_load_finished(success, url, web_view)
        )

        # Start loading in background
        web_view.setUrl(QUrl(url))

        return web_view

    def _on_load_finished(self, success, url, web_view):
        """Handle when background loading is finished."""
        if web_view in self.loading_views:
            self.loading_views.remove(web_view)

        self.load_completed.emit(success, url, web_view)

    def cleanup(self):
        """Clean up all loading views."""
        for view in self.loading_views:
            view.deleteLater()
        self.loading_views.clear()


class URLHandler:
    """Utility class for URL processing."""

    @staticmethod
    def normalize_url(url):
        """Normalize a URL by adding protocol if missing."""
        if not url.strip():
            return ""

        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url

    @staticmethod
    def is_valid_url(url):
        """Basic URL validation."""
        normalized = URLHandler.normalize_url(url)
        return bool(normalized and "." in normalized)
