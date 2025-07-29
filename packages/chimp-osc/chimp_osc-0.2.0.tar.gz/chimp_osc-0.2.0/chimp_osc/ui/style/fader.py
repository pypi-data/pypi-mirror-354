from nicegui import ui

class Slider(ui.slider):
    def __init__(self, *, min, max, step = 1, value = None, on_change = None):
        super().__init__(min=min, max=max, step=step, value=value, on_change=on_change)
        self.props('vertical reverse')
        self.style("margin-top: 15px; margin-left: auto; margin-right: auto; display: block; height: 550px")