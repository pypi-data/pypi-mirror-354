from chimp_osc import ChimpOSCInterface
from chimp_osc.console.button import Button

class FaderPage:
    def __init__(self, itf: ChimpOSCInterface):
        self._itf = itf
        self._name = None
        self.next = Button(lambda value: self._itf.fader_page_next(value))
        self.previous = Button(lambda value: self._itf.fader_page_previous(value))
        self.template = Button(lambda value: self._itf.fader_page_template(value))
        self._itf.add_handler("/chimp/fader/page/name",self._handle_osc_name)

    def _handle_osc_name(self, address, *args):
        assert isinstance(args[0],str)
        self._name = args[0]

    @property
    def name(self):
        return self._name