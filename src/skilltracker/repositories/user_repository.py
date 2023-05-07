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


def check_password(clear_password, hashed_password) -> bool:
    """Check password against a hash string."""
    return compare_digest(insecure_hash(clear_password), hashed_password)


class UserRepository:
    """A class that implements user account related read/write operations."""

    def __init__(self, database: Database | None = None):
        """Return a new UserRepository instance.

        Args:
            database: Optional Database instance to use for connections.
                Default Database will be used if not given.
        """
        self._database = database or DATABASE_REGISTRY.get()

    def check_user_exists(self, username: str) -> bool:
        """Return boolean indicating whether account with given username exists.

        Args:
            username: username for user.
        """
        with self._database.get_cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE username=?", (username,))
            user = cursor.fetchone()

        return user is not None

    def get_by_username(self, username: str) -> models.User:
        """Return user with given username.

        Args:
            username: username for user,

        Raises:
            UserNotFoundError: If account with given username doesn't exist.
        """
        with self._database.get_cursor() as cursor:
            cursor.execute("SELECT id,username,password FROM users WHERE username=?", (username,))
            user = cursor.fetchone()

        if user is None:
            raise UserNotFoundError(f"User {username!r} doesn't exists.")

        return models.User(*user)

    def get_by_username_and_password(self, username: str, clear_password: str) -> models.User:
        """Return user with given username and password.

        Args:
            username: username
            clear_password: un-hashed clear password

        Raises:
            UserNotFoundError: If account with given username doesn't exist.
            InvalidPasswordError: If account exists but given password was wrong.
        """
        user = self.get_by_username(username)
        if not check_password(clear_password, user.password_hash):
            raise InvalidPasswordError(f"Wrong password for user {username!r}")
        return user

    def delete_user(self, username: str) -> None:
        """Deletes user with given username from the database_file.

        Args:
            username: username

        Raises:
            UserNotFoundError: If account with given username doesn't exist.
        """
        self.get_by_username(username)
        with self._database.get_cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username=?", (username,))

    def add_user(self, username: str, clear_password: str) -> models.User:
        """Add a new user entry to the database.

        Args:
            username: username
            clear_password: un-hashed clear password

        Raises:
            UsernameTakenError: if username is already in use.

        Returns:
            User instance of the created user.
        """
        if self.check_user_exists(username):
            raise UsernameTakenError(f"The username {username!r} is taken.")

        hashed_password = insecure_hash(clear_password)
        with self._database.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            user_id = cursor.lastrowid

        return models.User(user_id, username, hashed_password)


USER_REPO_REGISTRY = ObjectRegistry(default_instance_factory=UserRepository)
