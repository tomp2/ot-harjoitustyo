import math
from typing import Callable

from dearpygui import dearpygui as dpg

from skilltracker import models
from skilltracker.custom_types import Self
from skilltracker.ui.utils import centered_window
from skilltracker.ui.view import View
from skilltracker.repositories.user_repository import get_default_user_repository


class MainView(View):
    """The main window of the app, shown after user has logged in."""

    def __init__(
            self, user: models.User, quit_callback: Callable, log_out_callback: Callable
    ):
        """
        Args:
            user: the user that has logged in
        """
        super().__init__(viewport_title="Main view")
        self._user = user
        self._quit_callback = quit_callback
        self._log_out_callback = log_out_callback

    def _delete_account_callback(self):
        def _yes_callback():
            get_default_user_repository().delete_user(self._user.username)
            dpg.delete_item(popup)
            self._log_out_callback()

        with centered_window(label="Delete account?", modal=True, horizontal_scrollbar=True) as popup:
            dpg.add_text("You won't be able to get your data back after this.")
            dpg.add_separator()
            dpg.add_text("Are you sure you want to delete everything?")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Yes", width=75, callback=_yes_callback)
                dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.delete_item(popup))

    def create(self) -> Self:
        with dpg.window(label="Main Window", width=400, height=300) as window:
            self.window_tag = window
            dpg.add_text(f"Welcome, {self._user.username}!")

            with dpg.menu_bar():
                with dpg.menu(label="Settings"):
                    dpg.add_menu_item(label="Quit", callback=self._quit_callback)
                with dpg.menu(label="User"):
                    dpg.add_menu_item(label="Log out", callback=self._log_out_callback)
                    dpg.add_menu_item(label="Delete account", callback=self._delete_account_callback)

            with dpg.child_window(height=75, horizontal_scrollbar=True):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Videogame 1", height=55, enabled=False)
                    dpg.add_button(label="Videogame 2", height=55, enabled=False)
                    dpg.add_button(label="Videogame 3", height=55, enabled=False)

            with dpg.child_window(height=450):
                with dpg.group(horizontal=True, width=0):
                    with dpg.child_window(width=102, height=150):
                        dpg.add_button(label="Day", enabled=False)
                        dpg.add_button(label="Weed", enabled=False)
                        dpg.add_button(label="Month", enabled=False)

                    with dpg.child_window(height=350, width=500):
                        dpg.add_simple_plot(
                            label="Performance",
                            min_scale=-1.0,
                            max_scale=1.0,
                            tag="performanceGraph",
                            height=300,
                            width=400,
                        )
                        data = [math.sin(i / 50) for i in range(400)]
                        dpg.set_value("performanceGraph", data)

        return self
