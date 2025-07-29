from nicegui import ui
from chimp_osc import Chimp
from chimp_osc.ui.elements import ExecutorUI
from chimp_osc.ui.style import Grid

class Virtual:
    def __init__(self, chimp: Chimp):
        self.chimp = chimp

    def show(self):
        self.virtual_executor_ui()

    def virtual_executor_ui(self):
        with ui.grid(rows=2, columns=2):
            for j in range(4):
                with Grid(rows=4,columns=8):
                    for i in range(1,33):
                        ExecutorUI(self.chimp.virtual_executors[j*32+i])