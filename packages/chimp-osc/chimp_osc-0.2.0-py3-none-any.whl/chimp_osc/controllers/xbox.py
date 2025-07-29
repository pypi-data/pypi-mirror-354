from chimp_osc.controllers.base import LogicController

from chimp_osc.controllers.base.inputs import GamepadChimpButton, GamepadHat
from chimp_osc import Chimp

class XBoxController(LogicController):
    def __init__(self, chimp : Chimp):
        super().__init__(chimp)
        # Joystick Top Left -> Encoder
        self.axis_encoder_1.scale = 1
        self.axis_encoder_2.scale = -5
        self.set_axis(0,self.axis_encoder_1)
        self.set_axis(1,self.axis_encoder_2)
        self.set_button(9,self.btn_next_master_round)

        # Hat Buttom Left -> Executors
        self.set_hat(0,GamepadHat(self.btn_previous_executor,self.btn_next_executor,self.btn_flash_executor, self.btn_flash_executor))

        # Joystick Bottom Right -> Master
        self.set_button(8,self.btn_next_encoder_round)
        self.axis_dim_master_2.scale = -5
        self.set_axis(2,self.axis_dim_master_1)
        self.set_axis(3,self.axis_dim_master_2)

        # 4 Buttons -> 4 virtual Executors
        for i in range(4):
            self.set_button(i,GamepadChimpButton(self._chimp.virtual_executors[i+1].flash))

        # Backside -> Faders
        self.axis_dim_fader_1.mode = "DECREASE"
        self.axis_dim_fader_2.mode = "INCREASE"
        self.set_axis(4,self.axis_dim_fader_1)
        self.set_axis(5,self.axis_dim_fader_2)
        self.set_button(4,self.btn_previous_fader)
        self.set_button(5,self.btn_next_fader)

        # Mode-Buttons -> Fader go, pause flash
        self.set_button(6,self.btn_pause_fader)
        self.set_button(7,self.btn_go_fader)
        self.set_button(10,self.btn_flash_fader)