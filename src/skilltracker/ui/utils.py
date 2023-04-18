from dearpygui import dearpygui as dpg


def show_modal(message: str, title: str) -> None:
    with dpg.window(label=title, modal=True, no_title_bar=True) as popup:
        dpg.add_text(message)
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item(popup))
