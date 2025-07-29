from chimp_osc import ChimpOSCInterface
from chimp_osc.console.button import Button

class Encoder:
    def __init__(self, itf: ChimpOSCInterface, nr : int):
        self._itf = itf
        self._nr = nr
        self._text1 = None
        self._text2 = None
        self._inc = 0
        self.btn = Button(lambda data:self._itf.programmer_encoder_btn(self._nr,data))
        self._itf.add_handler(f"/chimp/programmer/encoder/{nr}/text1",self._handle_osc_text1)
        self._itf.add_handler(f"/chimp/programmer/encoder/{nr}/text2",self._handle_osc_text2)

    def _handle_osc_text1(self, address, *args):
        assert isinstance(args[0],str)
        self._text1 = args[0]

    def _handle_osc_text2(self, address, *args):
        assert isinstance(args[0],str)
        self._text2 = args[0]

    @property
    def text1(self):
        return self._text1
    
    @property
    def text2(self):
        return self._text2
    
    @property
    def inc(self):
        return self._inc
    
    @inc.setter
    def inc(self, inc:float):
        # if abs(inc) > 5:
        #     raise ValueError(inc)
        self._inc = max(min(inc,5),-5)
        self._itf.programmer_encoder_inc(self._nr,self._inc)