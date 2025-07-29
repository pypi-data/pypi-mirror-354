from chimp_osc import Chimp
from chimp_osc.controllers.base import BaseController
from chimp_osc.controllers.base.inputs import GamepadButton, GamepadChimpFader, GamepadChimpButton, GamepadChimpEncoder

class LogicController(BaseController):
    def __init__(self, chimp : Chimp):
        super().__init__()
        self._chimp = chimp
        self._selected_fader : int = 1
        self.btn_previous_fader = GamepadButton(self.previous_fader)
        self.btn_next_fader = GamepadButton(self.next_fader)
        self.axis_dim_fader_1 = GamepadChimpFader(self._chimp.faders[self.selected_fader])
        self.axis_dim_fader_2 = GamepadChimpFader(self._chimp.faders[self.selected_fader])
        self.btn_flash_fader = GamepadChimpButton(self._chimp.faders[self.selected_fader].flash)
        self.btn_go_fader = GamepadChimpButton(self._chimp.faders[self.selected_fader].go)
        self.btn_pause_fader = GamepadChimpButton(self._chimp.faders[self.selected_fader].pause)
        self._selected_master : int = 1
        self.btn_previous_master = GamepadButton(self.previous_master)
        self.btn_next_master = GamepadButton(self.next_master)
        self.btn_next_master_round = GamepadButton(self.next_master_round)
        self.axis_dim_master_1 = GamepadChimpFader(self._chimp.masters[self.selected_master])
        self.axis_dim_master_2 = GamepadChimpFader(self._chimp.masters[self.selected_master])
        self.btn_flash_master = GamepadChimpButton(self._chimp.masters[self.selected_master].flash)
        self._selected_executor : int = 1
        self.btn_previous_executor = GamepadButton(self.previous_executor)
        self.btn_next_executor = GamepadButton(self.next_executor)
        self.btn_flash_executor = GamepadChimpButton(self._chimp.executors[self.selected_executor].flash)
        self._selected_virtual_executor : int = 1
        self.btn_previous_virtual_executor = GamepadButton(self.previous_virtual_executor)
        self.btn_next_virtual_executor = GamepadButton(self.next_virtual_executor)
        self.btn_flash_virtual_executor = GamepadChimpButton(self._chimp.virtual_executors[self.selected_virtual_executor].flash)
        self._selected_encoder : int = 1
        self.btn_previous_encoder = GamepadButton(self.next_encoder)
        self.btn_next_encoder = GamepadButton(self.next_encoder)
        self.btn_next_encoder_round = GamepadButton(self.next_encoder_round)
        self.btn_encoder = GamepadChimpButton(self._chimp.programmer.encoders[self.selected_encoder].btn)
        self.axis_encoder_1 = GamepadChimpEncoder(self._chimp.programmer.encoders[self.selected_encoder])
        self.axis_encoder_2 = GamepadChimpEncoder(self._chimp.programmer.encoders[self.selected_encoder])
        

    @property
    def selected_fader(self):
        return self._selected_fader
    
    @selected_fader.setter
    def selected_fader(self, value: int):
        assert value in range(1,31)
        self._selected_fader = value
        self.axis_dim_fader_1.fader = self._chimp.faders[self.selected_fader]
        self.axis_dim_fader_2.fader = self._chimp.faders[self.selected_fader]
        self.btn_flash_fader.act_btn = self._chimp.faders[self.selected_fader].flash
        self.btn_go_fader.act_btn = self._chimp.faders[self.selected_fader].go
        self.btn_pause_fader.act_btn = self._chimp.faders[self.selected_fader].pause

    def previous_fader(self):
        if self.selected_fader > 1:
            self.selected_fader -= 1
        
    def next_fader(self):
        if self.selected_fader<30:
                self.selected_fader +=1

    @property
    def selected_master(self):
        return self._selected_master
    
    @selected_master.setter
    def selected_master(self, value: int):
        assert value in range(1,5)
        self._selected_master = value
        self.axis_dim_master_1.fader = self._chimp.masters[self.selected_master]
        self.axis_dim_master_2.fader = self._chimp.masters[self.selected_master]
        self.btn_flash_master.act_btn = self._chimp.masters[self.selected_master].flash

    def previous_master(self):
        if self.selected_master > 1:
            self.selected_master -= 1
        
    def next_master(self):
        if self.selected_master<4:
            self.selected_master +=1

    def next_master_round(self):
        if self.selected_master<4:
            self.selected_master += 1
        else:
            self.selected_master = 1
        
    @property
    def selected_executor(self):
         return self._selected_executor

    @selected_executor.setter
    def selected_executor(self, value: int):
        assert value in range(1,11)
        self._selected_executor = value
        self.btn_flash_executor.act_btn = self._chimp.executors[self.selected_executor].flash

    def previous_executor(self):
        if self.selected_executor > 1:
            self.selected_executor -=1

    def next_executor(self):
        if self.selected_executor < 10:
            self.selected_executor +=1
    
    @property
    def selected_virtual_executor(self):
         return self._selected_virtual_executor

    @selected_virtual_executor.setter
    def selected_virtual_executor(self, value: int):
        assert value in range(1,11)
        self._selected_virtual_executor = value
        self.btn_flash_virtual_executor.act_btn = self._chimp.virtual_executors[self.selected_virtual_executor].flash

    def previous_virtual_executor(self):
        if self.selected_virtual_executor > 1:
            self.selected_virtual_executor -=1

    def next_virtual_executor(self):
        if self.selected_virtual_executor < 10:
            self.selected_virtual_executor +=1

    @property
    def selected_encoder(self):
        return self._selected_encoder
    
    @selected_encoder.setter
    def selected_encoder(self, value :int):
        assert value in range(1,5)
        self._selected_encoder = value
        self.btn_encoder.act_btn = self._chimp.programmer.encoders[self._selected_encoder].btn
        self.axis_encoder_1.encoder = self._chimp.programmer.encoders[self._selected_encoder]
        self.axis_encoder_2.encoder = self._chimp.programmer.encoders[self._selected_encoder]

    def previous_encoder(self):
        if self.selected_encoder > 1:
            self.selected_encoder -=1

    def next_encoder(self):
        if self.selected_encoder < 4:
            self.selected_encoder +=1

    def next_encoder_round(self):
        if self.selected_encoder <4:
            self.selected_encoder +=1
        else:
            self.selected_encoder = 1