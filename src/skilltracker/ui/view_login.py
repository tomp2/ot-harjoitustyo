from __future__ import annotations

import time
from typing import Callable

from dearpygui import dearpygui as dpg

from skilltracker.custom_types import Self, DpgTag
from skilltracker.exceptions import (
    LoginUserInputError,
)
from skilltracker.services.skilltracker_service import (
    SkilltrackerService,
    SKILLTRACKER_SERVICE_REGISTRY,
)
from skilltracker.ui.utils import Colors
from skilltracker.ui.view import View


class LoginView(View):
    """Initial login window shown on app startup. Allows login and account creation."""

    def __init__(
        self,
        login_callback: Callable[[], None],
        skilltracker_service: SkilltrackerService | None = None,
    ):
        super().__init__(viewport_title="Login")
        self._login_callback = login_callback
        self._skilltracker_service = skilltracker_service or SKILLTRACKER_SERVICE_REGISTRY.get()

        self._messages_group_tag: DpgTag | None = None
        self._username_input_tag: DpgTag | None = None
        self._password_input_tag: DpgTag | None = None

    def create(self) -> Self:
        with dpg.window() as window:
            self.window_tag = window

            dpg.add_text("Log in to your account", color=[70, 230, 255])
            dpg.add_separator()
            self._username_input_tag = dpg.add_input_text(
                label="Username",
                width=200,
                hint="<username>",
                callback=self._attempt_login,
                on_enter=True,
            )
            self._password_input_tag = dpg.add_input_text(
                label="Password",
                width=200,
                hint="<password>",
                password=True,
                callback=self._attempt_login,
                on_enter=True,
            )
            self._messages_group_tag = dpg.add_group()

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
        return username, password

    def _attempt_login(self) -> None:
        username, password = self._get_login_fields()
        try:
            self._skilltracker_service.login(username, password)
        except LoginUserInputError as err:
            self._clear_messages()
            self._add_message(str(err))
            return

        dpg.configure_item("loading", show=True)
        self._add_message("Username & Password correct! Logging in...", Colors.BRIGHT_GREEN)
        time.sleep(0.4)
        self._login_callback()

    def _attempt_signup(self) -> None:
        username, password = self._get_login_fields()
        try:
            self._skilltracker_service.add_user(username, password)
        except LoginUserInputError as err:
            self._clear_messages()
            self._add_message(str(err))
            return

        dpg.configure_item("loading", show=True)
        self._add_message("Username & password OK, creating account...", Colors.GREEN)
        time.sleep(0.3)
        self._add_message("Account created! Logging in...", Colors.GREEN)
        time.sleep(0.3)
        self._login_callback()
