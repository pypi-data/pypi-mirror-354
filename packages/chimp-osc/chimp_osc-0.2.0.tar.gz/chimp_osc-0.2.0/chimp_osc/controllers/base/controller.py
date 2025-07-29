from typing import List, Dict
from abc import ABC, abstractmethod
from chimp_osc.controllers.base.inputs import GamepadInput, GamepadAxis, GamepadButton, GamepadHat
from pygame.event import Event

class BaseController(ABC):
    def __init__(self):
        self._buttons : Dict[int,GamepadButton] = {}
        self._hats : Dict[int,GamepadHat] = {}
        self._axes : Dict[int,GamepadAxis] = {}
        self._manager = None

    def set_button(self, nr:int, btn: GamepadButton):
        self._buttons[nr] = btn

    def set_hat(self, nr:int, hat: GamepadHat):
        self._hats[nr] = hat

    def set_axis(self, nr: int, axis: GamepadAxis):
        self._axes[nr] = axis

    @property
    def buttons_list(self):
        return list(self._buttons.values())
    
    @property
    def hats_list(self):
        return list(self._hats.values())
    
    @property
    def axes_list(self):
        return list(self._axes.values())

    @property
    def inputs(self) -> List[GamepadInput]:
        return self.buttons_list + self.hats_list + self.axes_list
    
    def start(self,joystick_nr:int = 0):
        from chimp_osc.controllers.base import ControllerManager
        self._manager = ControllerManager(self,joystick_nr)