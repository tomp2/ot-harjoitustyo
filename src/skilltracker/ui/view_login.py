from __future__ import annotations

import sqlite3
import time
from hmac import compare_digest
from typing import Callable, Any

from dearpygui import dearpygui as dpg

from skilltracker import models
from skilltracker.custom_types import *
from skilltracker.database import get_db, insecure_hash
from skilltracker.ui.utils import show_modal, Colors
from skilltracker.ui.view import View


class ValidationError(Exception):
    pass


class LoginView(View):
    """Initial login window shown on app startup. Allows login and account creation."""

    def __init__(self, login_callback: Callable[[models.User], Any]):
        """
        Args:
            login_callback: callable to check login credentials
        """
        super().__init__(viewport_title="Login")
        self._login_callback = login_callback

        self._messages_group_tag = dpg.generate_uuid()
        self._username_input_tag = dpg.generate_uuid()
        self._password_input_tag = dpg.generate_uuid()

    def create(self) -> Self:
        with dpg.window() as window:
            self.window_tag = window

            dpg.add_text("Log in to your account", color=[70, 230, 255])
            dpg.add_separator()
            dpg.add_input_text(
                tag=self._username_input_tag,
                label="Username",
                width=200,
                hint="Type your username here",
                callback=self._attempt_login,
                on_enter=True,
            )
            dpg.add_input_text(
                tag=self._password_input_tag,
                label="Password",
                width=200,
                hint="Type your password here",
                password=True,
                callback=self._attempt_login,
                on_enter=True,
            )
            dpg.add_group(tag=self._messages_group_tag)

            with dpg.group(horizontal=True):
                dpg.add_button(label="Sign Up", width=100, callback=self._attempt_signup)
                dpg.add_button(label="Login", width=100, callback=self._attempt_login)
                dpg.add_loading_indicator(tag="loading", show=False)

        return self

    def _add_message(self, message: str, color=Colors.RED) -> None:
        dpg.add_text(
            default_value=message,
            color=color,
            bullet=True,
            parent=self._messages_group_tag,
        )

    def _clear_messages(self):
        dpg.delete_item(self._messages_group_tag, children_only=True)

    def _get_login_fields(self) -> tuple[str, str]:
        username = dpg.get_value(self._username_input_tag)
        password = dpg.get_value(self._password_input_tag)
        print(f"{username=}")
        self._clear_messages()
        time.sleep(0.08)
        if len(username) < 3:
            self._add_message("Username must be at least 3 characters long!")
            raise ValidationError
        if len(password) < 3:
            self._add_message("Password must be at least 3 characters long!")
            raise ValidationError

        return username, password

    def _attempt_login(self):
        try:
            username, password = self._get_login_fields()
        except ValidationError:
            return

        try:
            user_in_db = get_db().get_user(username)
        except Exception as err:
            show_modal(
                title="Unexpected error!",
                message=f"Could not login.\n" f"Error message is shown below:\n\n{err}",
            )
            return

        if user_in_db is None:
            self._add_message("Unknown username!")
            return

        if not compare_digest(user_in_db.password, insecure_hash(password)):
            self._add_message(f"Invalid password!")
            return

        dpg.configure_item("loading", show=True)
        self._add_message(
            "Username and Password correct! Logging in...", Colors.BRIGHT_GREEN
        )
        time.sleep(0.75)
        self._login_callback(user_in_db)

    def _attempt_signup(self) -> None:
        try:
            username, password = self._get_login_fields()
        except ValidationError:
            return

        try:
            user_in_db = get_db().add_user(username, password)
        except sqlite3.IntegrityError:
            self._add_message("This username is already taken!")
            return
        except Exception as err:
            show_modal(
                title="Unexpected error!",
                message=f"Could not login.\n" f"Error message is shown below:\n\n{err}",
            )
            return

        dpg.configure_item("loading", show=True)
        self._add_message("Username & password OK, creating account...", Colors.GREEN)
        time.sleep(1)
        self._add_message("Account created! Logging in...", Colors.GREEN)
        time.sleep(1)
        self._login_callback(user_in_db)
