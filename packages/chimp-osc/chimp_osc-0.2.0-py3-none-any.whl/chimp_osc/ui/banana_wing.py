from nicegui import ui
from chimp_osc import Chimp
from chimp_osc.ui.elements import FaderUI
from chimp_osc.ui.style import Grid

class BananaWing:
    def __init__(self, chimp: Chimp):
        self.chimp = chimp

    def show(self):
        self.fader_ui()

    def fader_ui(self):
        with Grid(rows=1,columns=20):
            for i in range(11,31):
                FaderUI(self.chimp.faders[i])