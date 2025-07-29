from nicegui import ui

from chimp_osc.console import Programmer
from chimp_osc.ui.elements.button_ui import ButtonUI
from chimp_osc.ui.elements.led_button_ui import LedButtonUI
from chimp_osc.ui.style import Grid


class HomeUI:
    def __init__(self, programmer: Programmer):
        self._programmer = programmer
        
        with Grid(rows=2,columns=4):
            # ROW 1
            self._prev = ButtonUI(self._programmer.previous,"Prev")
            self._next = ButtonUI(self._programmer.next,"Next")
            ui.space()
            self._set = ButtonUI(self._programmer.set,"Set")
            # ROW 2
            self._home = ButtonUI(self._programmer.home,"Home")
            self._highlight = LedButtonUI(self._programmer.highlight,"High\nlight")
            ui.space()
            self._blind = LedButtonUI(self._programmer.blind,"Blind")