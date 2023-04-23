from __future__ import annotations

import hashlib
import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from skilltracker import config
from skilltracker import models


def insecure_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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

    def initialize(self) -> None:
        with self.get_cursor() as cursor:
            cursor.execute(self._init_sqlite_script.read_text("utf8"))

    def get_user(self, username: str) -> models.User | None:
        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT id,username,password FROM users WHERE username=?", (username,)
            )
            result = cursor.fetchone()
        return result and models.User(*result)

    def add_user(self, username, password) -> models.User:
        hashed_password = insecure_hash(password)
        with self.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            user_id = cursor.lastrowid

        return models.User(user_id, username, password)


def get_db() -> Database:
    db = Database()
    db.initialize()
    return db
