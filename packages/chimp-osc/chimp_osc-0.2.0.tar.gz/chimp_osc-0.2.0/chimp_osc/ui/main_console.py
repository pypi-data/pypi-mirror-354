from nicegui import ui
from chimp_osc import Chimp
from chimp_osc.ui.elements import FaderUI, MasterUI, ExecutorUI, ProgrammerUI, HomeUI, EncoderUI
from chimp_osc.ui.style import Grid
from chimp_osc.ui.elements.select_feature_ui import SelectFeatureUI

class MainConsole:
    def __init__(self, chimp: Chimp):
        self.chimp = chimp

    def show(self):
        with ui.row().style("align-items: flex-end;"):
            self.fader_ui()
            self.executor_ui()
            self.master_ui()
            self.select_feature_ui()

    def fader_ui(self):
        with Grid(rows=1,columns=10):
            for i in range(1,11):
                FaderUI(self.chimp.faders[i])

    def executor_ui(self):
        with ui.column():
            with Grid(rows=1, columns=4):
                for i in range(1,5):
                    EncoderUI(self.chimp.programmer.encoders[i])
            ProgrammerUI(self.chimp.programmer,self.chimp.faderpage,self.chimp.executorpage)
            with Grid(rows=1,columns=10):
                for i in range(1,11):
                    ExecutorUI(self.chimp.executors[i])

    def master_ui(self):
        with ui.column():
            HomeUI(self.chimp.programmer)
            with Grid(rows=1,columns=4):
                for i in range(1,5):
                    MasterUI(self.chimp.masters[i])

    def select_feature_ui(self):
        SelectFeatureUI(self.chimp.programmer)