from __future__ import annotations

import ctypes
import platform
import sys

import dearpygui.dearpygui as dpg

from skilltracker import models
from skilltracker.settings import SETTINGS_REGISTRY, Settings
from skilltracker.ui.utils import create_exception_modal
from skilltracker.ui.view import View
from skilltracker.ui.view_login import LoginView
from skilltracker.ui.view_main import MainView


class GuiManager:
    """A class that starts/stops the UI, and manages different views."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.current_view: View | None = None
        self.logged_in_user: models.User | None = None
        self.settings = settings or SETTINGS_REGISTRY.get()

    def _set_gui_font(self):
        with dpg.font_registry():
            default_font = dpg.add_font(str(self.settings.font_file), 20)
            dpg.bind_font(default_font)
            if platform.system() == "Windows":
                ctypes.windll.shcore.SetProcessDpiAwareness(2)

    @staticmethod
    def register_modal_exception_hook():
        def hook(*args, **kwargs):
            try:
                create_exception_modal(*args, **kwargs)
            finally:
                sys.__excepthook__(*args, **kwargs)

        sys.excepthook = hook

    def show_view(self, view: View) -> None:
        """Set view as the primary window in the viewport."""
        view.set_primary_window(True)
        view.apply_viewport_title()

        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = view

    def show_login_view(self):
        view = LoginView(login_callback=self.login_user).create()
        self.logged_in_user = None
        self.show_view(view)

    def show_main_view(self, user):
        view = MainView(
            user=user,
            log_out_callback=self.show_login_view,
            quit_callback=dpg.stop_dearpygui,
        ).create()
        self.show_view(view)

    def start_main_loop(
        self,
        custom_render_loop: tuple[int, int] = SETTINGS_REGISTRY.get().custom_render_loop,
    ):
        dpg.create_context()
        dpg.create_viewport(
            width=self.settings.viewport_shape[0], height=self.settings.viewport_shape[1]
        )

        self._set_gui_font()
        self.show_login_view()

        dpg.setup_dearpygui()
        dpg.show_viewport()

        self.register_modal_exception_hook()

        if custom_render_loop:
            while dpg.is_dearpygui_running():
                jobs = dpg.get_callback_queue()
                if jobs:
                    dpg.run_callbacks(jobs)
                dpg.render_dearpygui_frame()
        else:
            dpg.start_dearpygui()

        dpg.destroy_context()
