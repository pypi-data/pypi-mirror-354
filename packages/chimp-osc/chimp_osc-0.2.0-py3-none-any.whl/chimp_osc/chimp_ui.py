from nicegui import ui


from chimp_osc import Chimp
from chimp_osc.ui import BananaWing, MainConsole, Virtual

def create_ui(chimp:Chimp, host : str = "0.0.0.0", port: int = 3000):

    bw = BananaWing(chimp)
    mc = MainConsole(chimp)
    v = Virtual(chimp)

    @ui.page("/")
    def main_page():
        ui.dark_mode(True)
        ui.colors(primary="#444444",accent="#dddd44")
        with ui.tabs() as tabs:
            ui.tab("Main Console")
            ui.tab("Banana Wing")
            ui.tab("Virtual Executors")

        with ui.tab_panels(tabs).classes("w-full"):
            with ui.tab_panel("Main Console"):
                mc.show()
            with ui.tab_panel("Banana Wing"):
                bw.show()
            with ui.tab_panel("Virtual Executors"):
                v.show()

    ui.run(host=host,port=port,reload=False,title="Chimp")