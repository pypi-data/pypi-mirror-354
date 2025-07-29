from chimp_osc.console.led_button import LedButton
from chimp_osc.ui.elements.button_ui import ButtonUI


class LedButtonUI(ButtonUI):
    def __init__(self, btn:LedButton, name = None, icon = None, span2 = False):
        super().__init__(btn, name, icon, span2)
        self._btn.add_handler(self.handler)

    def handler(self, value: bool):
        self._btn_ui.props(f'color={"accent" if value else "primary"}')
