"""
Main window implementation for the fullscreen web browser.
"""

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

from ..core.url_injector import URLInjector
from ..core.browser import BackgroundLoader, URLHandler
from ..utils.shortcuts import ShortcutManager
from .templates import get_welcome_html, get_loading_status_script


class FullscreenWebBrowser(QMainWindow):
    """Main fullscreen web browser window."""

    def __init__(self):
        super().__init__()
        self.background_loader = BackgroundLoader()
        self.shortcut_manager = ShortcutManager(self)
        self.url_injector = None

        self.init_ui()
        self.setup_url_injector()

    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("Fullscreen Web Display")

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for true fullscreen

        # Create stacked widget to manage multiple web views
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create main web view (visible)
        self.main_web_view = QWebEngineView()
        self.stacked_widget.addWidget(self.main_web_view)

        # Set up keyboard shortcuts
        self.shortcut_manager.setup_shortcuts(
            self.main_web_view, self.close, self.toggle_fullscreen
        )

        # Load initial page
        self.load_initial_page()

        # Go fullscreen
        self.showFullScreen()

    def setup_url_injector(self):
        """Set up the URL injector for external commands."""
        self.url_injector = URLInjector()
        self.url_injector.url_received.connect(self.load_url)
        self.url_injector.start_monitoring()

        # Connect background loader signals
        self.background_loader.load_completed.connect(self.on_background_load_finished)

        print(f"Monitoring command file: {self.url_injector.command_file_path}")
        print(
            "Update the JSON file with {'url': 'https://example.com'} to display websites"
        )

    def load_initial_page(self):
        """Load the initial welcome page."""
        self.main_web_view.setHtml(get_welcome_html())

    def load_url(self, url):
        """Load a URL in the background and display when fully loaded."""
        normalized_url = URLHandler.normalize_url(url)

        if not URLHandler.is_valid_url(normalized_url):
            print(f"Invalid URL: {url}")
            self.show_loading_status(f"Invalid URL: {url}")
            return

        # Show loading status on current page
        self.show_loading_status(f"Loading {normalized_url}...")

        # Start background loading
        self.background_loader.load_url(normalized_url)

    def show_loading_status(self, message):
        """Show loading status on the current page."""
        script = get_loading_status_script(message)
        self.main_web_view.page().runJavaScript(script)

    def on_background_load_finished(self, success, url, web_view):
        """Handle when background loading is finished."""
        if success:
            print(f"Successfully loaded: {url}")
            print("Switching to loaded page...")

            # Remove the old main web view from stacked widget
            self.stacked_widget.removeWidget(self.main_web_view)
            old_web_view = self.main_web_view

            # Move the loaded web view to become the main view
            self.main_web_view = web_view
            self.stacked_widget.addWidget(self.main_web_view)
            self.stacked_widget.setCurrentWidget(self.main_web_view)

            # Clean up old web view
            old_web_view.deleteLater()

            # Update shortcuts to work with new web view
            self.shortcut_manager.cleanup()
            self.shortcut_manager.setup_shortcuts(
                self.main_web_view, self.close, self.toggle_fullscreen
            )

        else:
            print(f"Failed to load: {url}")
            # Show error on current page
            self.show_loading_status(f"Failed to load {url}")

            # Clean up failed loading web view
            web_view.deleteLater()

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def closeEvent(self, event):
        """Handle close event."""
        if self.url_injector:
            self.url_injector.stop_monitoring()

        self.background_loader.cleanup()
        self.shortcut_manager.cleanup()

        event.accept()
