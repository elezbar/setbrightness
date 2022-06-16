# #импорт библиотеки 

# import keyboard


# config = [
#     {'monitor': 0,
#      'min':10,
#      'max':90},
#     {'monitor': 1,
#      'min':0,
#      'max':80},
#     ]
# hotkeys ={
#     '-':'alt+2',
#     '+':'alt+8',}

# step = 10
# def set_brightness(step, znak):
#     for m in config:
#         new_step = int((m['max'] - m['min']) / 100 * step)
#         print(new_step)
#         sbc.set_brightness(znak+str(new_step), display=m['monitor'])

# keyboard.add_hotkey(hotkeys['+'], lambda: set_brightness(step,'+'))
# keyboard.add_hotkey(hotkeys['-'], lambda: set_brightness(step,'-'))
# #recorded = keyboard.record(until='esc')
# #print(recorded)

# keyboard.wait()
# input()

from ast import MatMult
import screen_brightness_control as sbc


class Monitor():

    @staticmethod
    def get_list_monitors() -> list:
        list_monitors = []
        for mon in sbc.filter_monitors():
            name = "Неизвестно"
            if mon['manufacturer']:
                name = mon['manufacturer']
            monitor = Monitor(
                name = name,
                model = mon['name'],
                manufactur = mon['manufacturer_id']
            )
            list_monitors.append(monitor)
        return list_monitors

    def __init__(self, name: str,
                 model: str,
                 manufactur: str,
                 min_bri: int = 0,
                 max_bri: int = 100,
                 step_prosent: int = 10):
        self.name = name
        self.model = model
        self.manufactur = manufactur
        self._min_bri = min_bri
        self._max_bri = max_bri
        self._step_prosent = step_prosent
        self.brightness = sbc.get_brightness(display=model)
        self._set_step_int()

    def _set_step_int(self):
        _stp_float = (self._max_bri - self._min_bri) / 100 * self._step_prosent
        self._step_int = int(_stp_float)

    def set_brightness(self, brightness_level: int):
            
            _diff_bri = self._max_bri - self._min_bri
            _coof_bri = _diff_bri / 100
            self.brightness = int(brightness_level)*_coof_bri
            print(self.brightness, self.name)
            sbc.set_brightness(self.brightness, display=self.model)

    def down_brightness(self):
        self.brightness -= self.step
        if self.brightness < self.min_bri:
            self.brightness = self.min_bri
        sbc.set_brightness(self.brightness, display=self.model)

    def up_brightness(self):
        self.brightness += self.step
        if self.brightness > self.max_bri:
            self.brightness = self.max_bri
        sbc.set_brightness(self.brightness, display=self.model)

    def set_min_bri(self, min_bri: int):
        self._min_bri = min_bri
        self._set_step_int()

    def set_max_bri(self, max_bri: int):
        self._max_bri = max_bri
        self._set_step_int()

    def set_step_prosent(self, step_prosent: int):
        self._step_prosent = step_prosent
        self._set_step_int()

    def get_min_bri(self) -> int:
        return self._min_bri

    def get_max_bri(self) -> int:
        return self._max_bri

    def get_step_prosent(self) -> int:
        return self._step_prosent
