from nicegui import ui

from chimp_osc.console import Master
from chimp_osc.ui.elements.button_ui import ButtonUI
from chimp_osc.ui.style import Slider

class MasterUI:
    def __init__(self, master: Master):
        self._master = master
        with ui.column().classes("w-full"):
            self._slider = Slider(min=0,max=100).bind_value(self._master,"value")
            self._flash = ButtonUI(self._master.flash,name=str(self._master._nr))
            