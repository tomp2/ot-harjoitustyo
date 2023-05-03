"""Provides a repository for app users."""
from __future__ import annotations

import hashlib
from hmac import compare_digest
from typing import Final

from skilltracker import models
from skilltracker.database import Database, get_default_database
from skilltracker.exceptions import UserNotFoundError, InvalidPasswordError


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
        if database is None:
            database = get_default_database()
        self._database = database

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


class UserRepositoryRegistry:
    """Handles registering and providing UserRepository instances."""

    DEFAULT_NAME: Final[str] = "default"
    _registry: dict[str, UserRepository] = {}

    @classmethod
    def register(cls, name: str, user_repository: UserRepository) -> UserRepository:
        """Register a UserRepository instance with the given name.

        Args:
            name: name for the instance. Used to access it later with `get`.
            user_repository: UserRepository instance to register.

        Returns:
            UserRepository: the registered UserRepository instance.

        Raises:
            ValueError: If the name is already taken.

        Notes:
            The name "default" is reserved and cannot be used.
        """
        if name in cls._registry:
            raise ValueError(f'UserRepository with name "{name}" is already registered.')
        if name == cls.DEFAULT_NAME and cls.DEFAULT_NAME in cls._registry:
            raise ValueError(
                'Name "default" is reserved for registry\'s default UserRepository instance.'
            )

        cls._registry[name] = user_repository
        return user_repository

    @classmethod
    def get(cls, name: str | None = None) -> UserRepository:
        """Return UserRepository instance with the given name form the registry.

        Args:
            name: name for the instance. Defaults to "default".

        Returns:
            UserRepository: from the registry.

        Notes:
            If config_name isn't given, a new default UserRepository instance
            will be created and registered with the name "default" and default
            database. After, the default instance will be returned when
            calling this again without config_name.
        """
        if name is not None:
            return cls._registry[name]

        default_instance = cls._registry.get(cls.DEFAULT_NAME)
        if default_instance is None:
            default_instance = UserRepository(get_default_database())
            cls.register(cls.DEFAULT_NAME, default_instance)
        return default_instance
