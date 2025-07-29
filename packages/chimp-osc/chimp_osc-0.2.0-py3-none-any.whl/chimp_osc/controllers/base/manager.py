import logging
import pygame
import threading
from chimp_osc.controllers.base import BaseController

class ControllerManager:
    def __init__(self, controller: BaseController, joystick_nr : int = 0,autostart: bool = True):
        self._controller : BaseController = controller
        self._joystick_nr = joystick_nr
        self._thread = None
        self._run = False
        if autostart:
            self.start()

    def start(self):
        self._run = True
        self._thread = threading.Thread(target=self._run_manager,daemon=True)
        logging.debug("Starting Controller")
        self._thread.start()

    def _run_manager(self):
        pygame.init()
        pygame.joystick.init()
        cnt = pygame.joystick.get_count()
        if cnt == 0:
            raise ModuleNotFoundError("No Controllers found")
        if self._joystick_nr not in range(cnt):
            raise IndexError
        joystick = pygame.joystick.Joystick(self._joystick_nr)
        joystick.init()
        logging.info(f"Initialized Joystick {joystick.get_id()}: {joystick.get_name()}")
        while self._run:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.JOYBUTTONUP or event.type == pygame.JOYBUTTONDOWN:
                    if event.dict["button"] in self._controller._buttons:
                        self._controller._buttons[event.dict["button"]].handle(event)
                if event.type == pygame.JOYHATMOTION:
                    if event.dict["hat"] in self._controller._hats:
                        self._controller._hats[event.dict["hat"]].handle(event)
                if event.type == pygame.JOYAXISMOTION:
                    if event.dict["axis"] in self._controller._axes:
                        self._controller._axes[event.dict["axis"]].handle(event)

    def stop(self):
        if self._run and self._thread.is_alive():
            logging.debug("Stopping Controller")
            self._run = False
            self._thread.join()

