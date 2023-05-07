from __future__ import annotations

from skilltracker import models
from skilltracker.exceptions import UserInputValidationError
from skilltracker.object_registry import ObjectRegistry
from skilltracker.repositories.user_repository import UserRepository, USER_REPO_REGISTRY


def validate_login_fields(username: str, clear_password: str):
    if len(username) < 3:
        raise UserInputValidationError("Username must be at least 3 characters long!")
    if len(clear_password) < 3:
        raise UserInputValidationError("Password must be at least 3 characters long!")


class SkilltrackerService:
    def __init__(self, practice_repository=None, user_repository: UserRepository | None = None):
        self._logged_in_user: models.User | None = None
        self._practice_repository = practice_repository
        self._user_repository = user_repository or USER_REPO_REGISTRY.get()

    def login(self, username: str, clear_password: str) -> models.User:
        """
        Raises:
            UserNotFoundError:
                If account with given username doesn't exist.
            InvalidPasswordError:
                If account exists but given password was wrong.
        """
        validate_login_fields(username, clear_password)
        user = self._user_repository.get_by_username_and_password(username, clear_password)
        self._logged_in_user = user
        return user

    @property
    def current_user(self):
        return self._logged_in_user

    def logout(self):
        self._logged_in_user = None

    def add_user(self, username: str, clear_password: str):
        """
        Raises:
            UserNotFoundError:
                If account with given username doesn't exist.
            InvalidPasswordError:
                If account exists but given password was wrong.
            UsernameTakenError:
        """
        validate_login_fields(username, clear_password)
        return self._user_repository.add_user(username, clear_password)


SKILLTRACKER_SERVICE_REGISTRY = ObjectRegistry(default_instance_factory=SkilltrackerService)
