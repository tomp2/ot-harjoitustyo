from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from dearpygui import dearpygui as dpg
from abc import abstractmethod

from skilltracker.custom_types import *


class View:
    def __init__(self, viewport_title: str | None = None):
        self.viewport_title = f"skilltracker"
        if self.viewport_title is not None:
            self.viewport_title += f"- {viewport_title}"

        self._window_tag: DPG_ID | None = None

    @property
    def window_tag(self) -> DPG_ID:
        if self._window_tag is None:
            raise RuntimeError("window_id doesn't exists before view's window exists.")
        return self._window_tag

    @window_tag.setter
    def window_tag(self, window_tag: DPG_ID) -> None:
        if self._window_tag is not None:
            raise RuntimeError("window_id is already set.")
        self._window_tag = window_tag

    @abstractmethod
    def create(self) -> Self:
        """Implementation should create a dpg window and set the private
        _window_tag instance variable to the created dpg window's tag."""
        pass

    def set_primary_window(self, value: bool) -> None:
        dpg.set_primary_window(self.window_tag, value)

    def apply_viewport_title(self) -> None:
        dpg.set_viewport_title(self.viewport_title)

    def destroy(self) -> None:
        dpg.delete_item(self.window_tag)
        self._window_tag = None
