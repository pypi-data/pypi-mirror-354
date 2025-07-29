from chimp_osc.console.button import Button
from chimp_osc import ChimpOSCInterface

class LedButton(Button):
    def __init__(self, btn: callable, itf:ChimpOSCInterface , led_path: str):
        super().__init__(btn)
        self._itf = itf
        self._led =  False
        self._itf.add_handler(led_path, self.handle_led)
        self._led_handler = None

    def handle_led(self, adress, *args):
        assert args[0] in (0.0,1.0)
        self._led = bool(args[0])
        if self._led_handler:
            self._led_handler(self.led)

    @property
    def led(self):
        return self._led
    
    def add_handler(self, handler: callable):
        self._led_handler = handler
