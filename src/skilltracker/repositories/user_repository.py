from __future__ import annotations

import hashlib
from hmac import compare_digest

from skilltracker import models
from skilltracker.database import Database, get_default_database
from skilltracker.exceptions import UserNotFoundError, InvalidPasswordError


def insecure_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class UserRepository:
    def __init__(self, database: Database):
        self._database = database

    def get_user(self, username: str) -> models.User | None:
        with self._database.get_cursor() as cursor:
            cursor.execute(
                "SELECT id,username,password FROM users WHERE username=?", (username,)
            )
            result = cursor.fetchone()
        return result and models.User(*result)

    def get_by_login(self, username: str, clear_password: str) -> models.User | None:
        hashed_password = insecure_hash(clear_password)
        with self._database.get_cursor() as cursor:
            cursor.execute(
                "SELECT id,username,password FROM users WHERE username=? AND password=?",
                (username, hashed_password)
            )
            result = cursor.fetchone()

        if not result:
            raise UserNotFoundError

        if not compare_digest(insecure_hash(clear_password), result[2]):
            raise InvalidPasswordError

        return models.User(id=result[0], username=result[1])

    def delete_user(self, username: str) -> models.User | None:
        with self._database.get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM users WHERE username=?", (username,)
            )
            result = cursor.fetchone()
        return result and models.User(*result)

    def add_user(self, username, clear_password) -> models.User:
        hashed_password = insecure_hash(clear_password)
        with self._database.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            user_id = cursor.lastrowid

        return models.User(user_id, username)


def get_default_user_repository() -> UserRepository:
    if not hasattr(get_default_user_repository, "_database_instance"):
        repository = UserRepository(get_default_database())
        setattr(get_default_user_repository, "_database_instance", repository)
        return repository
    return getattr(get_default_user_repository, "_database_instance")
