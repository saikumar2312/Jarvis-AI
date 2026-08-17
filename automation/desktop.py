"""
Desktop automation tools for macOS.
"""

import subprocess
from pathlib import Path


class DesktopManager:

    APP_ALIASES = {
        "apple music": "Music",
        "music": "Music",
        "apple notes": "Notes",
        "notes": "Notes",
        "calc": "Calculator",
        "calculator": "Calculator",
        "safari": "Safari",
        "chrome": "Google Chrome",
        "google chrome": "Google Chrome",
        "vs code": "Visual Studio Code",
        "vscode": "Visual Studio Code",
        "visual studio code": "Visual Studio Code",
        "terminal": "Terminal",
        "finder": "Finder",
        "mail": "Mail",
        "calendar": "Calendar",
        "photos": "Photos",
        "messages": "Messages",
        "reminders": "Reminders",
        "settings": "System Settings",
        "system settings": "System Settings",
    }

    APPLICATION_DIRECTORIES = [
        Path("/Applications"),
        Path.home() / "Applications",
        Path("/System/Applications"),
    ]

    def _find_application(self, name: str) -> str | None:
        """Find an installed macOS application."""

        requested = name.strip().lower()

        # Check aliases first.
        requested = self.APP_ALIASES.get(requested, requested)

        for directory in self.APPLICATION_DIRECTORIES:

            if not directory.exists():
                continue

            for app in directory.glob("*.app"):

                app_name = app.stem.lower()

                if app_name == requested.lower():
                    return app.stem

                if requested.lower() in app_name:
                    return app.stem

        return None

    def open_application(self, application: str) -> str:
        """Open an installed macOS application."""

        application = application.strip()

        if not application:
            return "Please specify an application."

        app_name = self._find_application(application)

        if app_name is None:
            return f"I couldn't find an installed application called {application}."

        try:
            subprocess.run(
                ["open", "-a", app_name],
                check=True,
            )

            return f"Opened {application}."

        except subprocess.CalledProcessError:
            return f"I couldn't open {application}."