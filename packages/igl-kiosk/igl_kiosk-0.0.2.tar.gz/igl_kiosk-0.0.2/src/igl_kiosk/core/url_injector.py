"""
URL Injector module for handling external URL injection via file monitoring.
"""

import json
import threading
import time
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal


class URLInjector(QObject):
    """Handles external URL injection via file monitoring."""

    url_received = pyqtSignal(str)

    def __init__(self, command_file_path="web_display_commands.json"):
        super().__init__()
        self.command_file = Path(command_file_path)
        self.last_modified = 0
        self.monitoring = True
        self.monitoring_thread = None

        # Create command file if it doesn't exist
        if not self.command_file.exists():
            self.create_command_file()

    def create_command_file(self):
        """Create initial command file with instructions."""
        initial_data = {
            "instructions": "To display a website, update this file with: {'url': 'https://example.com'}",
            "url": "",
        }
        with open(self.command_file, "w") as f:
            json.dump(initial_data, f, indent=2)

    def start_monitoring(self):
        """Start monitoring the command file in a separate thread."""
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
            self.monitoring = True
            self.monitoring_thread = threading.Thread(
                target=self._monitor_file, daemon=True
            )
            self.monitoring_thread.start()

    def _monitor_file(self):
        """Monitor the command file for changes."""
        while self.monitoring:
            try:
                if self.command_file.exists():
                    current_modified = self.command_file.stat().st_mtime

                    if current_modified > self.last_modified:
                        self.last_modified = current_modified
                        self._process_command_file()

            except Exception as e:
                print(f"Error monitoring file: {e}")

            time.sleep(0.5)  # Check every 500ms

    def _process_command_file(self):
        """Process the command file and extract URL."""
        try:
            with open(self.command_file, "r") as f:
                data = json.load(f)

            url = data.get("url", "").strip()
            if url and url != "":
                print(f"Received URL command: {url}")
                self.url_received.emit(url)

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error processing command file: {e}")

    def stop_monitoring(self):
        """Stop monitoring the command file."""
        self.monitoring = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=1.0)

    @property
    def command_file_path(self):
        """Get the absolute path to the command file."""
        return self.command_file.absolute()
