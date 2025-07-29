from nicegui import ui

from chimp_osc.console import Programmer, FaderPage,ExecutorPage
from chimp_osc.ui.elements.button_ui import ButtonUI
from chimp_osc.ui.elements.led_button_ui import LedButtonUI
from chimp_osc.ui.style import Grid


class ProgrammerUI:
    def __init__(self, programmer: Programmer, fpg: FaderPage, epg:ExecutorPage):
        self._programmer = programmer
        self._faderpage = fpg
        self._executorpage = epg
        with ui.row():
            ui.label("Fader Page:")
            ui.label().bind_text_from(self._faderpage,"name")
            ui.label("Executor Page:")
            ui.label().bind_text_from(self._executorpage,"name")
        with Grid(rows=7,columns=10):
            # ROW 1
            self._fixture = ButtonUI(self._programmer.fixture,"Fixture")
            self._group = ButtonUI(self._programmer.group,"Group")
            self._preset = ButtonUI(self._programmer.preset,"Preset")
            self._cuelist = ButtonUI(self._programmer.cuelist,"Cuelist")
            self._cue = ButtonUI(self._programmer.cue,"Cue")
            ui.space()
            self._fan = LedButtonUI(self._programmer.fan,"Fan")
            self._effect = ButtonUI(self._programmer.effect,"Effect")
            self._clear = LedButtonUI(self._programmer.clear,"Clear",span2=True)
            # ROW 2
            [ui.space() for _ in range(10)]
            # ROW 3
            self._rec = ButtonUI(self._programmer.record,"Rec")
            self._edit = ButtonUI(self._programmer.edit,"Edit")
            self._del = ButtonUI(self._programmer.delete,"Del")
            self._copy = ButtonUI(self._programmer.copy,"Copy")
            self._move = ButtonUI(self._programmer.move,"Move")
            ui.space()
            self._backspace= ButtonUI(self._programmer.backspace, "<-")
            self._fw_slash= ButtonUI(self._programmer.fw_slash, "/")
            self._minus=ButtonUI(self._programmer.minus,"-")
            self._plus=ButtonUI(self._programmer.plus,"+")
            #ROW 4
            self._name = ButtonUI(self._programmer.name,"Name")
            self._select = ButtonUI(self._programmer.select,"Select")
            self._link = ButtonUI(self._programmer.link,"Link")
            self._load = ButtonUI(self._programmer.load,"Load")
            self._off = ButtonUI(self._programmer.off,"Off")
            ui.space()
            self._7 = ButtonUI(self._programmer.num7,"7")
            self._8 = ButtonUI(self._programmer.num8,"8")
            self._9 = ButtonUI(self._programmer.num9,"9")
            self._thru = ButtonUI(self._programmer.thru,"Thru")
            # ROW 5
            [ui.space() for _ in range(6)]
            self._4 = ButtonUI(self._programmer.num4,"4")
            self._5 = ButtonUI(self._programmer.num5,"5")
            self._6 = ButtonUI(self._programmer.num6,"6")
            self._full = ButtonUI(self._programmer.full,"Full")
            # ROW 6
            self._fpg_up = ButtonUI(self._faderpage.next,"↑ FPg")
            self._epg_up = ButtonUI(self._executorpage.next,"↑ EPg")
            self._template = ButtonUI(self._faderpage.template,"Templ")
            self._time = ButtonUI(self._programmer.time,"Time")
            self._infinity = ButtonUI(self._programmer.shift,"Infinity")
            ui.space()
            self._1 = ButtonUI(self._programmer.num1,"1")
            self._2 = ButtonUI(self._programmer.num2,"2")
            self._3 = ButtonUI(self._programmer.num3,"3")
            self._at = ButtonUI(self._programmer.at,"@")
            # ROW 7
            self._fpg_down = ButtonUI(self._faderpage.previous,"↓ FPg")
            self._epg_down = ButtonUI(self._executorpage.previous,"↓ EPg")
            self._skip = ButtonUI(self._programmer.skip,"Skip")
            self._goto = ButtonUI(self._programmer.goto,"Goto")
            self._open = ButtonUI(self._programmer.open,"Open")
            ui.space()
            self._0 = ButtonUI(self._programmer.num0,"0")
            self._dot = ButtonUI(self._programmer.dot,".")
            self._enter = ButtonUI(self._programmer.enter,"Enter",span2=True)
        with ui.row():
            ui.label().bind_text_from(self._programmer,"content")
            ui.icon("error").bind_visibility_from(self._programmer,"error_led")