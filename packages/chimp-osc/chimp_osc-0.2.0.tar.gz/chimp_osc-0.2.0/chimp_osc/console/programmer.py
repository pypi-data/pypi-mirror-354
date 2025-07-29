from chimp_osc import ChimpOSCInterface
from chimp_osc.console.encoder import Encoder
from chimp_osc.console.button import Button
from chimp_osc.console.led_button import LedButton

class Programmer:
    def __init__(self, itf: ChimpOSCInterface):
        self._itf = itf
        self.record = Button(lambda value: self._itf.programmer_keypad_record(value))
        self.edit = Button(lambda value: self._itf.programmer_keypad_edit(value))
        self.delete = Button(lambda value: self._itf.programmer_keypad_delete(value))
        self.copy = Button(lambda value: self._itf.programmer_keypad_copy(value))
        self.move = Button(lambda value: self._itf.programmer_keypad_move(value))
        self.name = Button(lambda value: self._itf.programmer_keypad_name(value))
        self.open = Button(lambda value: self._itf.programmer_keypad_open(value))
        self.select = Button(lambda value: self._itf.programmer_keypad_select(value))
        self.link = Button(lambda value: self._itf.programmer_keypad_link(value))
        self.load = Button(lambda value: self._itf.programmer_keypad_load(value))
        self.off = Button(lambda value: self._itf.programmer_keypad_off(value))
        self.skip = Button(lambda value: self._itf.programmer_keypad_skip(value))
        self.goto = Button(lambda value: self._itf.programmer_keypad_goto(value))
        self.time = Button(lambda value: self._itf.programmer_keypad_time(value))
        self.fixture = Button(lambda value: self._itf.programmer_keypad_fixture(value))
        self.group = Button(lambda value: self._itf.programmer_keypad_group(value))
        self.preset = Button(lambda value: self._itf.programmer_keypad_preset(value))
        self.cuelist = Button(lambda value: self._itf.programmer_keypad_cuelist(value))
        self.cue = Button(lambda value: self._itf.programmer_keypad_cue(value))
        self.effect = Button(lambda value: self._itf.programmer_keypad_effect(value))
        self.minus = Button(lambda value: self._itf.programmer_keypad_minus(value))
        self.plus = Button(lambda value: self._itf.programmer_keypad_plus(value))
        self.thru = Button(lambda value: self._itf.programmer_keypad_thru(value))
        self.full = Button(lambda value: self._itf.programmer_keypad_full(value))
        self.at = Button(lambda value: self._itf.programmer_keypad_at(value))
        self.fw_slash = Button(lambda value: self._itf.programmer_keypad_fw_slash(value))
        self.backspace = Button(lambda value: self._itf.programmer_keypad_backspace(value))
        self.num0 = Button(lambda value: self._itf.programmer_keypad_0(value))
        self.num1 = Button(lambda value: self._itf.programmer_keypad_1(value))
        self.num2 = Button(lambda value: self._itf.programmer_keypad_2(value))
        self.num3 = Button(lambda value: self._itf.programmer_keypad_3(value))
        self.num4 = Button(lambda value: self._itf.programmer_keypad_4(value))
        self.num5 = Button(lambda value: self._itf.programmer_keypad_5(value))
        self.num6 = Button(lambda value: self._itf.programmer_keypad_6(value))
        self.num7 = Button(lambda value: self._itf.programmer_keypad_7(value))
        self.num8 = Button(lambda value: self._itf.programmer_keypad_8(value))
        self.num9 = Button(lambda value: self._itf.programmer_keypad_9(value))
        self.dot = Button(lambda value: self._itf.programmer_keypad_dot(value))
        self.enter = Button(lambda value: self._itf.programmer_keypad_enter(value))
        self.shift = Button(lambda value: self._itf.programmer_keypad_shift(value))
        self.home = Button(lambda value: self._itf.programmer_keypad_home(value))
        self.set = Button(lambda value: self._itf.programmer_keypad_set(value))
        self.all_none = Button(lambda value: self._itf.programmer_select_all_none(value))
        self.next = Button(lambda value: self._itf.programmer_select_next(value))
        self.previous = Button(lambda value: self._itf.programmer_select_previous(value))
        self.even_odd = Button(lambda value: self._itf.programmer_select_even_odd(value))
        self.first_second_half = Button(lambda value: self._itf.programmer_select_first_second_half(value))
        self.random = Button(lambda value: self._itf.programmer_select_random(value))
        self.shuffle_selection = Button(lambda value: self._itf.programmer_select_shuffle_selection(value))
        self.invert = Button(lambda value: self._itf.programmer_select_invert(value))
        self.intensity = Button(lambda value: self._itf.programmer_feature_select_intensity(value))
        self.position = Button(lambda value: self._itf.programmer_feature_select_position(value))
        self.color = Button(lambda value: self._itf.programmer_feature_select_color(value))
        self.gobo = Button(lambda value: self._itf.programmer_feature_select_gobo(value))
        self.beam = Button(lambda value: self._itf.programmer_feature_select_beam(value))
        self.shaper = Button(lambda value: self._itf.programmer_feature_select_shaper(value))
        self.control = Button(lambda value: self._itf.programmer_feature_select_control(value))
        self.special = Button(lambda value: self._itf.programmer_feature_select_special(value))
        self.blind = LedButton(lambda value: self._itf.programmer_blind_btn(value),self._itf,"/chimp/programmer/blind/led")
        self.highlight = LedButton(lambda value: self._itf.programmer_highlight_btn(value),self._itf,"/chimp/programmer/highlight/led")
        self.fan = LedButton(lambda value: self._itf.programmer_fan_btn(value),self._itf,"/chimp/programmer/fan/led")
        self.clear = LedButton(lambda value: self._itf.programmer_clear_btn(value),self._itf,"/chimp/programmer/clear/led")
        
        self._content: str = None
        self._error_led: bool = None
        self.encoders = {i: Encoder(self._itf, i) for i in range(1, 5)}
        self._itf.add_handler(
            "/chimp/programmer/commandline/content", self.handle_osc_content
        )
        self._itf.add_handler(
            "/chimp/programmer/commandline/error_led", self.handle_osc_error_led
        )

    def handle_osc_content(self, address, *args):
        assert isinstance(args[0], str)
        self._content = args[0]

    @property
    def content(self):
        return self._content

    def handle_osc_error_led(self, address, *args):
        assert args[0] in (0.0,1.0)
        self._error_led = bool(args[0])

    @property
    def error_led(self):
        return self._error_led

    def pan_tilt(self):
        # TODO
        raise NotImplementedError
        self._itf.programmer_pan_tilt()
