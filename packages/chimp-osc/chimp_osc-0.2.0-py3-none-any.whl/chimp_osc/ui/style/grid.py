from nicegui import ui

class Grid(ui.grid):
    def __init__(self, *, rows = None, columns = None):
        super().__init__(rows=rows, columns=columns)
        self.classes('gap-1')