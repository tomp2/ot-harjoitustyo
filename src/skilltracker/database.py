import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from skilltracker.settings import SettingRegistry
from skilltracker.custom_types import Self


class Database:
    """Class that implements context managers for getting database cursor/connection."""

    def __init__(
        self,
        database_file: Path = SettingRegistry.get().database_file,
        sql_script: Path = SettingRegistry.get().database_schema_file,
    ):
        self._database_file: Path = database_file
        self._sql_script: Path = sql_script

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
            conn.executescript(self._sql_script.read_text("utf8"))
        return self


def get_default_database() -> Database:
    """Create and/or return instance of a Database with default app configurations."""
    if not hasattr(get_default_database, "_database_instance"):
        database = Database().initialize()
        setattr(get_default_database, "_database_instance", database)

    return getattr(get_default_database, "_database_instance")
