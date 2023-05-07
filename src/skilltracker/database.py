from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from skilltracker.custom_types import Self
from skilltracker.object_registry import ObjectRegistry
from skilltracker.settings import SETTINGS_REGISTRY


class Database:
    """Class that implements context managers for getting database cursor/connection."""

    def __init__(self, database_file: Path | None = None, sql_script: str | None = None):
        self._database_file = database_file or SETTINGS_REGISTRY.get().database_file
        self._sql_script = sql_script or SETTINGS_REGISTRY.get().database_schema_file.read_text(
            "utf8"
        )

    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """Context manager for automatically closing connection."""
        conn = sqlite3.connect(self._database_file)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    @contextmanager
    def get_cursor(self) -> Iterator[sqlite3.Cursor]:
        """Context manager for automatically closing cursor."""
        conn: sqlite3.Connection
        cursor: sqlite3.Cursor
        with self.get_connection() as conn:
            with closing(conn.cursor()) as cursor:
                yield cursor

    def initialize(self) -> Self:
        """Create database file."""
        conn: sqlite3.Connection
        with self.get_connection() as conn:
            conn.executescript(self._sql_script)
        return self


DATABASE_REGISTRY = ObjectRegistry(default_instance_factory=lambda: Database().initialize())
