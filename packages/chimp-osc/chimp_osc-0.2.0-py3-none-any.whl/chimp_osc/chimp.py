from chimp_osc import ChimpOSCInterface
from chimp_osc.console import Fader,FaderPage,Master,Executor,ExecutorPage, Programmer

class Chimp:
    def __init__(self, target_ip:str | None = None, itf:ChimpOSCInterface | None = None):
        if target_ip is None and itf is None:
            raise ConnectionError("target_ip or itf needs to be provided")
        if itf:
            self._itf = itf
        else:
            self._itf = ChimpOSCInterface(target_ip)
        self.faders = {nr:Fader(self._itf,nr) for nr in range(1,31)}
        self.faderpage = FaderPage(self._itf)
        self.masters = {nr:Master(self._itf,nr) for nr in range(1,5)}
        self.executors = {nr:Executor(self._itf,nr) for nr in range(1,11)}
        self.executorpage = ExecutorPage(self._itf)
        self.virtual_executors ={nr:Executor(self._itf,nr,True) for nr in range(1,129)}
        self.programmer = Programmer(self._itf)
        self.sync()

    def sync(self):
        self._itf.sync(True)
        
    def use_accel(self):
        self._itf.use_accel(True)
        raise NotImplementedError
        