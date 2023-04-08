from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

import config


class Database:
    def __init__(
            self,
            db_path: Path = config.DATABASE_FILEPATH,
            schema_script: Path = config.DATABASE_CREATE_SCRIPT,
    ):
        self._database: Path = db_path
        self._init_sqlite_script: Path = schema_script

    def get_connection(self) -> sqlite3.Connection:
        """Connection that closes automatically"""
        with closing(sqlite3.connect(self._database)) as conn:
            return conn

    def get_cursor(self) -> sqlite3.Cursor:
        """Cursor that closes automatically"""
        with self.get_connection().cursor() as cursor:
            return cursor

    def initialize(self) -> None:
        self.get_cursor().execute(self._init_sqlite_script.read_text("utf8"))
