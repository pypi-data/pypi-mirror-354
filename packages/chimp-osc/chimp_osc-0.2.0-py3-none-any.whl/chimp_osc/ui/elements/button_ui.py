from nicegui import ui

from chimp_osc.console.button import Button
from chimp_osc.ui.style import UiButton

class ButtonUI:
    def __init__(self, btn : Button, name: str| None = None, icon : str | None = None, span2: bool = False):
        self._btn = btn
        self._btn_ui = UiButton(icon=icon,text=name).classes("w-full m-0 p-0").style("font-size: 66%;white-space: pre-wrap;")
        self._btn_ui.on('mousedown',self._mousedown)
        self._btn_ui.on('mouseup',self._mouseup)
        if span2:
           self._btn_ui.style('grid-column: span 2;')
        else:
           self._btn_ui.classes("aspect-square")
        

    def _mousedown(self,e):
        match e.args["button"]:
            case 0: # left click
                self._btn.press()
            case 1: # middle click
                self._btn.toggle()
            case 2: # right click
                pass

    def _mouseup(self,e):
        match e.args["button"]:
            case 0:
                self._btn.release()