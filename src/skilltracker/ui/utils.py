from dearpygui import dearpygui as dpg


def show_modal(message: str, title: str) -> None:
    with dpg.window(label=title, modal=True, no_title_bar=True) as popup:
        dpg.add_text(message)
        # dpg.add_separator()
        # dpg.add_checkbox(label="Don't ask me next time")
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item(popup))
            # dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.delete_item(popup))


class Colors:
    RED = [255, 0, 0]
    BRIGHT_RED = [255, 100, 100]
    GREEN = [0, 255, 0]
    BRIGHT_GREEN = [100, 255, 100]
    BLUE = [0, 0, 255]
    BRIGHT_BLUE = [100, 100, 255]
