from nicegui import ui

from chimp_osc.console import Fader
from chimp_osc.ui.elements.button_ui import ButtonUI
from chimp_osc.ui.style import Slider


class FaderUI:
    def __init__(self, fader: Fader):
        self._fader = fader
        with ui.column().classes("w-full"):
            self._go = ButtonUI(self._fader.go,icon='play_arrow')
            self._pause = ButtonUI(self._fader.pause,icon='pause')
            self._slider = Slider(min=0,max=100).bind_value(self._fader,"value")
            self._flash = ButtonUI(self._fader.flash,name=str(self._fader._nr))
            self._flash._btn_ui.bind_text_from(self._fader,"display")