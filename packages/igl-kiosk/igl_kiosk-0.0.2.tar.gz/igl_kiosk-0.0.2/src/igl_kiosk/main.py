#!/usr/bin/env python3
"""
Main entry point for the Fullscreen Web Display application.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from .ui.main_window import FullscreenWebBrowser


def main():
    """Main function to run the application."""
    # Note: High DPI scaling settings are commented out as they may cause issues
    # on some systems. Uncomment if needed:
    # QApplication.setHighDpiScaleFactorRoundingPolicy(
    #     QApplication.HighDpiScaleFactorRoundingPolicy.PassThrough
    # )

    app = QApplication(sys.argv)
    app.setApplicationName("Fullscreen Web Display")

    # Create and show the browser
    browser = FullscreenWebBrowser()

    print("\n" + "=" * 60)
    print("Fullscreen Web Display Started")
    print("=" * 60)
    print(f"Command file: {Path('web_display_commands.json').absolute()}")
    print("\nTo display a website, update the JSON file with:")
    print('{"url": "https://example.com"}')
    print("\nKeyboard shortcuts:")
    print("  ESC - Exit application")
    print("  F11 - Toggle fullscreen")
    print("  Ctrl+R - Reload current page")
    print("=" * 60)

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
