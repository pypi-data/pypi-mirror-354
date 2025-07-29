from nicegui import ui

class UiButton(ui.button):
    def __init__(self, text = '', *, on_click = None, color = 'primary', icon = None):
        super().__init__(text, on_click=on_click, color=color, icon=icon)
        self.classes("w-full m-0 p-0 h-16")
        self.style("font-size: 66%;white-space: pre-wrap;")