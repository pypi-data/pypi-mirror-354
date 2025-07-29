from nicegui import ui
from nicegui.events import JoystickEventArguments
import time

from chimp_osc.console.encoder import Encoder

class EncoderUI:
    def __init__(self, encoder: Encoder):
        self._encoder = encoder
        self._start = 0
        with ui.column():
            self.joystick = ui.joystick(color='#dddd44',
                                        on_start=self.on_start,
                                        on_move=self.on_move,
                                        on_end=self.on_end).style("width: 166px; height: 166px").classes("bg-primary")
            self._text1 = ui.label().bind_text_from(self._encoder,"text1")
            self._text2 = ui.label().bind_text_from(self._encoder,"text2")

    def on_start(self, e:JoystickEventArguments):
        self._start = time.time()

    def on_move(self, e:JoystickEventArguments):
        if abs(e.x) > 0.05 or abs(e.y) > 0.05:
            self._encoder.inc = max(min(e.x + 5* e.y,5),-5)

    async def on_end(self, e: JoystickEventArguments):
        self._encoder.inc = 0
        end = time.time()
        if (end - self._start) < 0.1:
            await self._encoder.btn.tip_async()