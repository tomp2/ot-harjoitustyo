from contextlib import contextmanager

from dearpygui import dearpygui as dpg


@contextmanager
def centered_window(**kwargs):
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_width()
    window_width = viewport_width // 3 * 2
    with dpg.window(show=False, width=window_width, **kwargs) as popup:
        yield popup

    dpg.split_frame()
    dpg.set_item_pos(
        item=popup,
        pos=[(viewport_width - window_width) // 2, viewport_height // 5]
    )
    dpg.configure_item(popup, show=True)


def show_exception(title: str, message: str, traceback: str) -> None:
    with centered_window(label=title, modal=True, horizontal_scrollbar=True) as popup:
        dpg.add_text(message)
        dpg.add_separator()
        dpg.add_input_text(multiline=True, readonly=True, default_value=traceback, width=-1)
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item(popup))


class Colors:
    RED = [255, 0, 0]
    BRIGHT_RED = [255, 100, 100]
    GREEN = [0, 255, 0]
    BRIGHT_GREEN = [100, 255, 100]
    BLUE = [0, 0, 255]
    BRIGHT_BLUE = [100, 100, 255]
