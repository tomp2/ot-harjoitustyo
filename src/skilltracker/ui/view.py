from __future__ import annotations

from dearpygui import dearpygui as dpg

from skilltracker.custom_types import Self, DpgTag


class View:
    def __init__(self, viewport_title: str | None = None):
        self.viewport_title = "skilltracker"
        if self.viewport_title is not None:
            self.viewport_title += f"- {viewport_title}"

        self._window_tag: DpgTag | None = None

    @property
    def window_tag(self) -> DpgTag:
        if self._window_tag is None:
            raise RuntimeError("window_id doesn't exists before view has been created.")
        return self._window_tag

    @window_tag.setter
    def window_tag(self, window_tag: DpgTag) -> None:
        if self._window_tag is not None:
            raise RuntimeError("window_id is already set.")
        self._window_tag = window_tag

    def initialize(self):
        self.window_tag = dpg.generate_uuid()
        return self.build(self.window_tag)

    def build(self, window_tag: DpgTag) -> Self:
        dpg.add_window(tag=window_tag)
        return self

    def set_as_primary_window(self, value: bool) -> None:
        dpg.set_primary_window(self.window_tag, value)

    def apply_viewport_title(self) -> None:
        dpg.set_viewport_title(self.viewport_title)

    def destroy(self) -> None:
        dpg.delete_item(self.window_tag)
        self._window_tag = None
