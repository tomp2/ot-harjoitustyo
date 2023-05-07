"""Provides a repository for app users."""
from __future__ import annotations

import hashlib
from hmac import compare_digest

from skilltracker import models
from skilltracker.database import DATABASE_REGISTRY, Database
from skilltracker.exceptions import UserNotFoundError, InvalidPasswordError, UsernameTakenError
from skilltracker.object_registry import ObjectRegistry


def insecure_hash(text: str) -> str:
    """Calculate SHA256 hash of given string."""
    # noinspection InsecureHash
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class UserRepository:
    """A class that implements user account related read/write operations."""

    def __init__(self, database: Database | None):
        """Return a new UserRepository instance.

        Args:
            database: Optional Database instance to use for connections.
                Default Database will be used if not given.
        """
        self._database = database or DATABASE_REGISTRY.get()

    def get_by_username(self, username: str) -> models.User | None:
        """Return user with given username, or None if not found."""
        with self._database.get_cursor() as cursor:
            cursor.execute("SELECT id,username,password FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
        if result is None:
            return None
        return models.User(*result)

    def get_by_username_and_password(self, username: str, clear_password: str) -> models.User:
        """Return user with given username and password.

        Args:
            username: username
            clear_password: un-hashed clear password

        Raises:
            UserNotFoundError: If username does not exist in the database.
            InvalidPasswordError: If hashed password does not match found
                user's stored password hash.
        """
        user = self.get_by_username(username)

        if user is None:
            raise UserNotFoundError

        if not compare_digest(insecure_hash(clear_password), user.password_hash):
            raise InvalidPasswordError

        return user

    def delete_user(self, username: str) -> None:
        """Deletes user with given username from the database."""
        with self._database.get_cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username=?", (username,))

    def add_user(self, username: str, clear_password: str) -> models.User:
        """Add a new user entry to the database.

        Args:
            username: username
            clear_password: un-hashed clear password

        Returns:
            User instance corresponding to the created user.
        """
        hashed_password = insecure_hash(clear_password)
        with self._database.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            user_id = cursor.lastrowid

        return models.User(user_id, username, hashed_password)


USER_REPO_REGISTRY = ObjectRegistry(default_instance_factory=UserRepository)
