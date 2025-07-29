from chimp_osc import ChimpOSCInterface
from chimp_osc.console.button import Button

class Executor:
    def __init__(self, itf: ChimpOSCInterface, nr : int, virtual:bool = False):
        self._itf = itf
        self._nr = nr
        self._name = None
        self.flash = Button(lambda value: self._itf.virtual_executor_flash(self._nr,value) if virtual else self._itf.executor_flash(self._nr,value))
        self._itf.add_handler(f"/chimp/{'virtual_executor' if virtual else 'executor'}/{self._nr}/name",self._handle_osc_name)

    def _handle_osc_name(self, address, *args):
        assert isinstance(args[0],str)
        self._name = args[0]

    @property
    def name(self):
        return self._name
    
    @property
    def display(self):
        return self.name if self.name else self._nr