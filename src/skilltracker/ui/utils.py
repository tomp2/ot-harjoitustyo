from __future__ import annotations

import pprint
import traceback
from contextlib import contextmanager
from types import TracebackType
from typing import Type, Callable

from dearpygui import dearpygui as dpg


@contextmanager
def centered_window(**kwargs):
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    kwargs.setdefault("autosize", True)
    kwargs.setdefault("min_size", (450, 100))
    kwargs.setdefault("max_size", (int(viewport_width * 0.8), int(viewport_height * 0.7)))

    with dpg.mutex():
        with dpg.window(**kwargs) as popup:
            yield popup

    dpg.split_frame()
    window_height = dpg.get_item_height(popup)
    window_width = dpg.get_item_width(popup)
    dpg.set_item_pos(
        item=popup,
        pos=[
            (viewport_width - window_width) // 2,
            (viewport_height - window_height) // 5,
        ],
    )


def create_exception_modal(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    traceback_: TracebackType,
):
    traceback_text = traceback.format_exception(exc_type, exc_value, traceback_)

    with centered_window(
        label="Unexpected Error!",
        modal=True,
    ) as popup:
        dpg.add_text(
            "There was an error that shouldn't have happened, this app has an bug."
            "You can continue to use the app, but it's not recommended since we "
            "don't know whats wrong and if the problem will cause data-loss."
            "It would be better to close the app and report the problem.",
            wrap=0,
        )
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Dismiss",
                width=75,
                callback=lambda: dpg.delete_item(popup),
            )
            dpg.add_button(
                label="Quit app",
                width=95,
                callback=dpg.stop_dearpygui,
            )
        dpg.add_separator()
        with dpg.collapsing_header(label="See error details"):
            dpg.add_input_text(
                label="Error source file",
                readonly=True,
                default_value=traceback_.tb_frame.f_code.co_filename,
            )
            dpg.add_input_text(
                label="Error line nro",
                readonly=True,
                default_value=str(traceback_.tb_lineno),
            )
            dpg.add_input_text(
                label="Exception type", readonly=True, default_value=exc_type.__name__
            )
            dpg.add_input_text(label="Message", readonly=True, default_value=str(exc_value))
            dpg.add_input_text(
                label="Function/module",
                readonly=True,
                default_value=traceback_.tb_frame.f_code.co_name,
            )
            dpg.add_text("Traceback")
            dpg.add_input_text(
                multiline=True,
                readonly=True,
                default_value="".join(traceback_text) * 10,
                width=-1,
            )
            dpg.add_text("Locals")
            dpg.add_input_text(
                readonly=True,
                default_value=pprint.pformat(traceback_.tb_frame.f_locals, depth=10, indent=2),
                multiline=True,
                width=-1,
            )


class Colors:
    RED = (255, 0, 0)
    BRIGHT_RED = (255, 100, 100)
    GREEN = (0, 255, 0)
    BRIGHT_GREEN = (100, 255, 100)
    BLUE = (0, 0, 255)
    BRIGHT_BLUE = (100, 100, 255)
