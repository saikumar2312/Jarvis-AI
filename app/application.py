"""
Main application lifecycle.
"""

from app.bootstrap import Bootstrap
from core.assistant import Assistant


class Application:
    def __init__(self):
        self.bootstrap = Bootstrap()
        self.assistant = Assistant()

    def run(self):
        self.bootstrap.initialize()
        self.assistant.start()