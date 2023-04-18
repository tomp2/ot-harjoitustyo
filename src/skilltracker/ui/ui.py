from __future__ import annotations

import dearpygui.dearpygui as dpg

from skilltracker import models
from skilltracker.ui.view import View
from skilltracker.ui.view_login import LoginView
from skilltracker.ui.view_main import MainView


class UI:
    """A class that starts/stops the UI, and manages different views."""

    VIEWPORT_WIDTH: int = 800
    VIEWPORT_HEIGHT: int = 600

    def __init__(self) -> None:
        self._current_view: View = None  # type: ignore[assign]
        self._logged_in_user: models.User | None = None

    def _show_view(self, view: View) -> None:
        """Set the given view as the primary window in the viewport."""
        view.set_primary_window(True)
        view.apply_viewport_title()

        if self._current_view is not None:
            self._current_view.destroy()
        self._current_view = view

    def _login_procedure(self, user: models.User):
        self._logged_in_user = user
        self._show_main_window(user)

    def _show_login_window(self):
        view = LoginView(login_callback=self._login_procedure).create()
        self._show_view(view)

    def _show_main_window(self, user):
        view = MainView(
            user=user,
            log_out_callback=self._show_login_window,
            quit_callback=dpg.stop_dearpygui,
        ).create()
        self._show_view(view)

    def start_main_loop(self):
        dpg.create_context()
        dpg.create_viewport(width=self.VIEWPORT_WIDTH, height=self.VIEWPORT_HEIGHT)

        self._show_login_window()

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
