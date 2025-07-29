import asyncio
import time
import threading

class Button:
    def __init__(self, btn: callable):
        self.btn : callable = btn
        self._state : bool = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state:bool):
        self._state = state
        self.btn(state)

    def press(self):
        self.state = True

    def release(self):
        self.state = False

    def toggle(self):
        self.state = not(self.state)

    def tip_block(self, t:float=0):
        self.press()
        time.sleep(t)
        self.release()

    def tip_thread(self, t: float=0):
        threading.Thread(target=self.tip_block,kwargs={"t":t}).start()

    async def tip_async(self, t:float=0):
        self.press()
        await asyncio.sleep(t)
        self.release()
