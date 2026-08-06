"""
Application settings for Jarvis.
"""

from dataclasses import dataclass


@dataclass
class Settings:
    """Global configuration for the application."""

    APP_NAME: str = "Jarvis AI"
    VERSION: str = "0.1.0"
    DEBUG: bool = True


settings = Settings()