"""
Keyboard shortcuts utilities.
"""

from PyQt6.QtGui import QKeySequence, QShortcut


class ShortcutManager:
    """Manages keyboard shortcuts for the application."""

    def __init__(self, parent):
        self.parent = parent
        self.shortcuts = []

    def setup_shortcuts(self, main_web_view, close_callback, fullscreen_callback):
        """Set up all keyboard shortcuts."""
        # ESC to exit fullscreen/quit
        quit_shortcut = QShortcut(QKeySequence("Escape"), self.parent)
        quit_shortcut.activated.connect(close_callback)
        self.shortcuts.append(quit_shortcut)

        # F11 to toggle fullscreen
        fullscreen_shortcut = QShortcut(QKeySequence("F11"), self.parent)
        fullscreen_shortcut.activated.connect(fullscreen_callback)
        self.shortcuts.append(fullscreen_shortcut)

        # Ctrl+R to reload
        reload_shortcut = QShortcut(QKeySequence("Ctrl+R"), self.parent)
        reload_shortcut.activated.connect(main_web_view.reload)
        self.shortcuts.append(reload_shortcut)

    def cleanup(self):
        """Clean up shortcuts."""
        for shortcut in self.shortcuts:
            shortcut.deleteLater()
        self.shortcuts.clear()
