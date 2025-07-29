from nicegui import ui

from chimp_osc.console import Executor
from chimp_osc.ui.elements.button_ui import ButtonUI


class ExecutorUI:
    def __init__(self, executor: Executor):
        self._executor = executor
        self._flash = ButtonUI(self._executor.flash)
        self._flash._btn_ui.bind_text_from(self._executor,"display")