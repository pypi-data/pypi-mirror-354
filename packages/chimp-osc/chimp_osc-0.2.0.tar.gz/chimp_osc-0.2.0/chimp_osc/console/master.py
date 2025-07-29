from chimp_osc import ChimpOSCInterface
from chimp_osc.console.button import Button

class Master:
    def __init__(self, itf: ChimpOSCInterface, nr : int):
        self._itf = itf
        self._nr = nr
        self._value = 0
        self.flash = Button(lambda value: self._itf.master_flash(self._nr, value))
        self._itf.add_handler(f"/chimp/master/{self._nr}/value",self._handle_osc_value)

    def _handle_osc_value(self, address, *args):
        assert isinstance(args[0],float)
        self._value = args[0]

    @property
    def value(self):
        return self._value/10
    
    @value.setter
    def value(self, value: float):
        self._value =max(min(value,100),0)*10
        self._itf.master_value(self._nr,self._value)