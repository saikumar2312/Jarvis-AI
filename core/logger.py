"""
Logging configuration for Jarvis.
"""

from loguru import logger
import sys


def setup_logger():
    """Configure the application logger."""

    logger.remove()

    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
    )

    logger.add(
        "logs/jarvis.log",
        rotation="5 MB",
        retention="7 days",
        level="DEBUG",
    )

    return logger