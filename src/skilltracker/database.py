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
        schema_script: Path = SettingRegistry.get().database_schema_file,
    ):
        self._database_path: Path = database_file
        self._init_sqlite_script: Path = schema_script

    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """Context manager for automatically closing connection."""
        conn = sqlite3.connect(self._database_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    @contextmanager
    def get_cursor(self) -> Iterator[sqlite3.Cursor]:
        """Context manager for automatically closing cursor."""
        with self.get_connection() as conn:
            with closing(conn.cursor()) as cursor:
                yield cursor

    def initialize(self) -> Self:
        """Create database file."""
        with self.get_cursor() as cursor:
            cursor.execute(self._init_sqlite_script.read_text("utf8"))
        return self


def get_default_database() -> Database:
    """Create and/or return instance of a Database with default app configurations."""
    if not hasattr(get_default_database, "_database_instance"):
        database = Database().initialize()
        setattr(get_default_database, "_database_instance", database)

    return getattr(get_default_database, "_database_instance")
