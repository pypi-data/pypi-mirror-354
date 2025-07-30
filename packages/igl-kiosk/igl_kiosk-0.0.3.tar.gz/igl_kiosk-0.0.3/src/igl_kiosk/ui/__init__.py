"""User interface components."""

from .main_window import FullscreenWebBrowser
from .templates import get_welcome_html, get_loading_status_script

__all__ = ["FullscreenWebBrowser", "get_welcome_html", "get_loading_status_script"]
