"""
SQLite database layer for Jarvis memory.
"""

import sqlite3
from pathlib import Path


class Database:

    def __init__(self, database_path: str = "memory/jarvis.db"):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()

    def add_memory(self, content: str):
        cursor = self.connection.cursor()

        cursor.execute(
            "INSERT INTO memories (content) VALUES (?)",
            (content,),
        )

        self.connection.commit()

    def get_memories(self):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id, content, created_at
            FROM memories
            ORDER BY id ASC
            """
        )

        return cursor.fetchall()

    def close(self):
        self.connection.close()