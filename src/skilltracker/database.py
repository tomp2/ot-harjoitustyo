import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from skilltracker import config
from skilltracker.custom_types import Self


class Database:
    def __init__(
            self,
            db_path: Path = config.DATABASE_FILEPATH,
            schema_script: Path = config.DATABASE_CREATE_SCRIPT,
    ):
        self._database: Path = db_path
        self._init_sqlite_script: Path = schema_script

    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """Connection that closes automatically"""
        conn = sqlite3.connect(self._database)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    @contextmanager
    def get_cursor(self) -> Iterator[sqlite3.Cursor]:
        """Cursor that closes automatically"""
        with self.get_connection() as conn:
            with closing(conn.cursor()) as cursor:
                yield cursor

    def initialize(self) -> Self:
        """Create database file"""
        with self.get_cursor() as cursor:
            cursor.execute(self._init_sqlite_script.read_text("utf8"))
        return self


def get_default_database() -> Database:
    if not hasattr(get_default_database, "_database_instance"):
        database = Database().initialize()
        setattr(get_default_database, "_database_instance", database)

    return getattr(get_default_database, "_database_instance")
