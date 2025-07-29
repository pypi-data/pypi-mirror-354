from nicegui import ui

from chimp_osc.console import Programmer
from chimp_osc.ui.elements.button_ui import ButtonUI
from chimp_osc.ui.style import Grid


class SelectFeatureUI:
    def __init__(self, programmer: Programmer):
        self._programmer = programmer
        
        with Grid(rows=8,columns=2):
            self._intensity = ButtonUI(self._programmer.intensity,"Intensity")
            self._all_none = ButtonUI(self._programmer.all_none,"All/None")
            self._position = ButtonUI(self._programmer.position,"Position")
            self._next = ButtonUI(self._programmer.next,"Next")
            self._color = ButtonUI(self._programmer.color,"Color")
            self._previous = ButtonUI(self._programmer.previous,"Previous")
            self._gobo = ButtonUI(self._programmer.gobo,"Gobo")
            self._even_odd = ButtonUI(self._programmer.even_odd,"Even/Odd")
            self._beam = ButtonUI(self._programmer.beam,"Beam")
            self._first_second_half = ButtonUI(self._programmer.first_second_half,"Half")
            self._shaper = ButtonUI(self._programmer.shaper,"Shaper")
            self._random = ButtonUI(self._programmer.random,"Random")
            self._control = ButtonUI(self._programmer.control,"Control")
            self._shuffle_selection = ButtonUI(self._programmer.shuffle_selection,"Shuffle")
            self._special = ButtonUI(self._programmer.special,"Special")
            self._invert = ButtonUI(self._programmer.invert,"Invert")