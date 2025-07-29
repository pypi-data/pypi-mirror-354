import pygame
from pygame.event import Event
from abc import ABC, abstractmethod
from typing import Literal

from chimp_osc.console.button import Button
from chimp_osc.console.fader import Fader
from chimp_osc.console.encoder import Encoder


class GamepadInput(ABC):
    @abstractmethod
    def handle(self, event : Event):
        pass

class GamepadButton(GamepadInput):
    def __init__(self, press: callable = None, release:callable=None):
        self._press : callable = press
        self._release : callable = release

    @property
    def press(self):
        return self._press

    @press.setter
    def press(self, press:callable):
        self._press = press

    @property
    def release(self):
        return self._release
    
    @release.setter
    def release(self,release:callable):
        self._release = release

    def handle(self, event: Event):
        if event.type != pygame.JOYBUTTONUP and event.type != pygame.JOYBUTTONDOWN:
            return
        if event.type == pygame.JOYBUTTONDOWN:
            if self._press:
                self._press()
        elif event.type == pygame.JOYBUTTONUP:
            if self._release:
                self._release()

class GamepadChimpButton(GamepadButton):
    def __init__(self, act_btn : Button | None = None):
        self._act_btn = act_btn
        super().__init__(self._act_btn.press if self._act_btn else None,self._act_btn.release if self._act_btn else None)

    @property
    def act_btn(self):
        raise AttributeError("Write-only")

    @act_btn.setter
    def act_btn(self, act_btn : Button | None):
        self._act_btn = act_btn
        self.press = self._act_btn.press
        self.release = self._act_btn.release

class GamepadHat(GamepadInput):
    def __init__(self, left : GamepadButton | None = None, right: GamepadButton | None = None, up: GamepadButton | None = None, down: GamepadButton | None = None):
        self._left : GamepadButton | None = left
        self._right : GamepadButton | None = right
        self._up : GamepadButton | None = up
        self._down : GamepadButton | None = down

    @property
    def left(self):
        raise AttributeError("Write-only")
    
    @left.setter
    def left(self, left: GamepadButton | None):
        self._left = left

    @property
    def right(self):
        raise AttributeError("Write-only")
    
    @right.setter
    def right(self, right: GamepadButton | None):
        self._right = right

    @property
    def up(self):
        raise AttributeError("Write-only")
    
    @up.setter
    def up(self, up: GamepadButton | None):
        self._up = up

    @property
    def down(self):
        raise AttributeError("Write-only")
    
    @down.setter
    def down(self, down: GamepadButton | None):
        self._down = down

    def handle(self, event : Event):
        x, y = event.dict.get("value")
        match x:
            case -1:
                if self._right.release: self._right.release()
                if self._left.press: self._left.press()
            case 0:
                if self._right.release: self._right.release()
                if self._left.release: self._left.release()
            case 1:
                if self._right.press: self._right.press()
                if self._left.release: self._left.release()
        match y:
            case -1:
                if self._up.release: self._up.release()
                if self._down.press: self._down.press()
            case 0:
                if self._up.release: self._up.release()
                if self._down.release: self._down.release()
            case 1:
                if self._up.press: self._up.press()
                if self._down.release: self._down.release()


class GamepadAxis(GamepadInput):
    def __init__(self, target = None, mode : Literal["MID", "INCREASE","DECREASE"] = "MID"):
        self._target = target
        self._mode : Literal["MID", "INCREASE","DECREASE"] = mode

    @property
    def target(self):
        raise AttributeError("Write-only")
    
    @target.setter
    def target(self, target):
        self._target = target

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode: Literal["MID", "INCREASE","DECREASE"]):
        self._mode = mode

    def handle(self, event : Event):
        if event.type != pygame.JOYAXISMOTION:
            return
        value = event.dict.get("value")
        if abs(value) < 0.1:
            return
        if self._mode == "DECREASE":
            value = (value -1)/0.5
        elif self._mode == "INCREASE":
            value = (value+1)/0.5
        if self._target:
            self._target(value)       
    
class GamepadChimpFader(GamepadAxis):
    def __init__(self, fader: Fader | None = None, mode: Literal["MID", "INCREASE","DECREASE"] = "MID", scale : float = 1):
        self._fader = fader
        self.scale = scale
        super().__init__(self.update_value, mode)
    
    @property
    def fader(self):
        raise AttributeError("Write-only")
    
    @fader.setter
    def fader(self, fader: Fader|None = None):
        self._fader = fader

    def update_value(self, increment: float):
        if self._fader:
            self._fader.value += increment * self.scale
    
class GamepadChimpEncoder(GamepadAxis):
    def __init__(self, encoder: Encoder | None = None, mode = "MID", scale: float = 5):
        assert abs(scale) <=5
        self._encoder = encoder
        self._scale = scale
        super().__init__(self.update_value, mode)

    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value: float):
        assert abs(value) <= 5
        self._scale = value

    @property
    def encoder(self):
        raise AttributeError("Write-only")

    @encoder.setter
    def encoder(self, encoder: Encoder | None = None):
        self._encoder = encoder
    
    def update_value(self, increment: float):
        if self._encoder:
            self._encoder.inc = increment * self.scale

