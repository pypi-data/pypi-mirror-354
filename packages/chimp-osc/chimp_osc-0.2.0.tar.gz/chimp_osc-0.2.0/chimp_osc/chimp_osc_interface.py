from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from typing import  Any
import logging
import threading

class ChimpOSCInterface:
    def __init__(
        self,
        target_ip: str,
        listen_ip : str="0.0.0.0",
        out_port: int = 9000,
        in_port: int = 8000,
        start_server: bool = True
    ):
        self.target_ip: str = target_ip
        self.listen_ip: str = listen_ip
        self._in_port = in_port
        self._out_port = out_port
        self.client = udp_client.SimpleUDPClient(
            self.target_ip, self._in_port
        )
        self.dispatcher = Dispatcher()
        self.server = None
        self.thread = None
        if start_server:
            self.start_osc_server()

    def start_osc_server(self):
        self.server = BlockingOSCUDPServer(
            (self.listen_ip, self._out_port), self.dispatcher
        )
        self.thread = threading.Thread(target=self.server.serve_forever,daemon=True)
        logging.debug("Starting Server")
        self.thread.start()

    def shutdown_osc_server(self):
        if self.server and self.thread.is_alive():
            logging.debug("Shutting down OSC server...")
            self.server.shutdown()
            self.server = None
            self.thread.join()
            logging.debug("OSC Server Shut Down")

    def add_handler(self, address: str, handler: Any):
        self.dispatcher.map(address=address, handler=handler)

    def send_message(self, path: str, value):
        if not path.startswith("/"):
            path = "/" + path
        self.client.send_message(path, float(value) if str(value).isnumeric() else value)
        logging.debug(f"Send {value} to {path}")


    def fader_go(self, nr: int, data: bool):
        path = "/chimp/" + "fader/{nr}/go".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def fader_pause(self, nr: int, data: bool):
        path = "/chimp/" + "fader/{nr}/pause".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def fader_flash(self, nr: int, data: bool):
        path = "/chimp/" + "fader/{nr}/flash".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def fader_value(self, nr: int, data: int):
        path = "/chimp/" + "fader/{nr}/value".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def fader_page_next(self, data: bool):
        path = "/chimp/" + "fader/page/next".format(data=data)
        self.send_message(path, float(data))
                    
    def fader_page_previous(self, data: bool):
        path = "/chimp/" + "fader/page/previous".format(data=data)
        self.send_message(path, float(data))
                    
    def fader_page_template(self, data: bool):
        path = "/chimp/" + "fader/page/template".format(data=data)
        self.send_message(path, float(data))
                    
    def master_flash(self, nr: int, data: bool):
        path = "/chimp/" + "master/{nr}/flash".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def master_value(self, nr: int, data: int):
        path = "/chimp/" + "master/{nr}/value".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def executor_flash(self, nr: int, data: bool):
        path = "/chimp/" + "executor/{nr}/flash".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def executor_page_next(self, data: bool):
        path = "/chimp/" + "executor/page/next".format(data=data)
        self.send_message(path, float(data))
                    
    def executor_page_previous(self, data: bool):
        path = "/chimp/" + "executor/page/previous".format(data=data)
        self.send_message(path, float(data))
                    
    def executor_page_template(self, data: bool):
        path = "/chimp/" + "executor/page/template".format(data=data)
        self.send_message(path, float(data))
                    
    def virtual_executor_flash(self, nr: int, data: bool):
        path = "/chimp/" + "virtual_executor/{nr}/flash".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_record(self, data: bool):
        path = "/chimp/" + "programmer/keypad/record".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_edit(self, data: bool):
        path = "/chimp/" + "programmer/keypad/edit".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_delete(self, data: bool):
        path = "/chimp/" + "programmer/keypad/delete".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_copy(self, data: bool):
        path = "/chimp/" + "programmer/keypad/copy".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_move(self, data: bool):
        path = "/chimp/" + "programmer/keypad/move".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_name(self, data: bool):
        path = "/chimp/" + "programmer/keypad/name".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_open(self, data: bool):
        path = "/chimp/" + "programmer/keypad/open".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_select(self, data: bool):
        path = "/chimp/" + "programmer/keypad/select".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_link(self, data: bool):
        path = "/chimp/" + "programmer/keypad/link".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_load(self, data: bool):
        path = "/chimp/" + "programmer/keypad/load".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_off(self, data: bool):
        path = "/chimp/" + "programmer/keypad/off".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_skip(self, data: bool):
        path = "/chimp/" + "programmer/keypad/skip".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_goto(self, data: bool):
        path = "/chimp/" + "programmer/keypad/goto".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_time(self, data: bool):
        path = "/chimp/" + "programmer/keypad/time".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_fixture(self, data: bool):
        path = "/chimp/" + "programmer/keypad/fixture".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_group(self, data: bool):
        path = "/chimp/" + "programmer/keypad/group".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_preset(self, data: bool):
        path = "/chimp/" + "programmer/keypad/preset".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_cuelist(self, data: bool):
        path = "/chimp/" + "programmer/keypad/cuelist".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_cue(self, data: bool):
        path = "/chimp/" + "programmer/keypad/cue".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_effect(self, data: bool):
        path = "/chimp/" + "programmer/keypad/effect".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_minus(self, data: bool):
        path = "/chimp/" + "programmer/keypad/minus".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_plus(self, data: bool):
        path = "/chimp/" + "programmer/keypad/plus".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_thru(self, data: bool):
        path = "/chimp/" + "programmer/keypad/thru".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_full(self, data: bool):
        path = "/chimp/" + "programmer/keypad/full".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_at(self, data: bool):
        path = "/chimp/" + "programmer/keypad/at".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_fw_slash(self, data: bool):
        path = "/chimp/" + "programmer/keypad/fw_slash".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_backspace(self, data: bool):
        path = "/chimp/" + "programmer/keypad/backspace".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_0(self, data: bool):
        path = "/chimp/" + "programmer/keypad/0".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_1(self, data: bool):
        path = "/chimp/" + "programmer/keypad/1".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_2(self, data: bool):
        path = "/chimp/" + "programmer/keypad/2".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_3(self, data: bool):
        path = "/chimp/" + "programmer/keypad/3".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_4(self, data: bool):
        path = "/chimp/" + "programmer/keypad/4".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_5(self, data: bool):
        path = "/chimp/" + "programmer/keypad/5".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_6(self, data: bool):
        path = "/chimp/" + "programmer/keypad/6".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_7(self, data: bool):
        path = "/chimp/" + "programmer/keypad/7".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_8(self, data: bool):
        path = "/chimp/" + "programmer/keypad/8".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_9(self, data: bool):
        path = "/chimp/" + "programmer/keypad/9".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_dot(self, data: bool):
        path = "/chimp/" + "programmer/keypad/dot".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_enter(self, data: bool):
        path = "/chimp/" + "programmer/keypad/enter".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_shift(self, data: bool):
        path = "/chimp/" + "programmer/keypad/shift".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_home(self, data: bool):
        path = "/chimp/" + "programmer/keypad/home".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_keypad_set(self, data: bool):
        path = "/chimp/" + "programmer/keypad/set".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_blind_btn(self, data: bool):
        path = "/chimp/" + "programmer/blind/btn".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_highlight_btn(self, data: bool):
        path = "/chimp/" + "programmer/highlight/btn".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_fan_btn(self, data: bool):
        path = "/chimp/" + "programmer/fan/btn".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_select_all_none(self, data: bool):
        path = "/chimp/" + "programmer/select/all_none".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_select_next(self, data: bool):
        path = "/chimp/" + "programmer/select/next".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_select_previous(self, data: bool):
        path = "/chimp/" + "programmer/select/previous".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_select_even_odd(self, data: bool):
        path = "/chimp/" + "programmer/select/even_odd".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_select_first_second_half(self, data: bool):
        path = "/chimp/" + "programmer/select/first_second_half".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_select_random(self, data: bool):
        path = "/chimp/" + "programmer/select/random".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_select_shuffle_selection(self, data: bool):
        path = "/chimp/" + "programmer/select/shuffle_selection".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_select_invert(self, data: bool):
        path = "/chimp/" + "programmer/select/invert".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_feature_select_intensity(self, data: bool):
        path = "/chimp/" + "programmer/feature/select/intensity".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_feature_select_position(self, data: bool):
        path = "/chimp/" + "programmer/feature/select/position".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_feature_select_color(self, data: bool):
        path = "/chimp/" + "programmer/feature/select/color".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_feature_select_gobo(self, data: bool):
        path = "/chimp/" + "programmer/feature/select/gobo".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_feature_select_beam(self, data: bool):
        path = "/chimp/" + "programmer/feature/select/beam".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_feature_select_shaper(self, data: bool):
        path = "/chimp/" + "programmer/feature/select/shaper".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_feature_select_control(self, data: bool):
        path = "/chimp/" + "programmer/feature/select/control".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_feature_select_special(self, data: bool):
        path = "/chimp/" + "programmer/feature/select/special".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_clear_btn(self, data: bool):
        path = "/chimp/" + "programmer/clear/btn".format(data=data)
        self.send_message(path, float(data))
    
    def programmer_commandline_error_led(self, data: bool):
        path = "/chimp/" + "programmer/commandline/error_led".format(data=data)
        self.send_message(path, float(data))
                    
    def programmer_encoder_btn(self, nr: int, data: bool):
        path = "/chimp/" + "programmer/encoder/{nr}/btn".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def programmer_encoder_inc(self, nr: int, data: int):
        path = "/chimp/" + "programmer/encoder/{nr}/inc".format(nr=nr, data=data)
        self.send_message(path, float(data))
                    
    def programmer_pan_tilt(self, data: float):
        path = "/chimp/" + "programmer/pan_tilt".format(data=data)
        self.send_message(path, float(data))
        # TODO
                    
    def use_accel(self, data: bool):
        path = "/chimp/" + "use_accel".format(data=data)
        self.send_message(path, float(data))
        # TODO
                    
    def sync(self, data: bool):
        path = "/chimp/" + "sync".format(data=data)
        self.send_message(path, float(data))
                    