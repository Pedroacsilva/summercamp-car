from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from math import exp

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory

from kivy_garden.speedmeter import SpeedMeter
from kivy_garden.led import Led


class NoValueSpeedMeter(SpeedMeter):

    def value_str(self, n): return ''

_displayed = { 
    0: '0',
    30: u'\u03a0 / 6', 60: u'\u03a0/3', 90: u'\u03a0/2', 120: u'2\u03a0/3',
    150: u'5\u03a0/6',
    180: u'\u03a0', 210: u'7\u03a0/6', 240: u'4\u03a0/3'
    }

class car_gui(App):
        
    def set_speed(self):
        ids = self.root.ids
        ids.rpm.value = exp(ids.speed_value.value / 200.0) * 4.5 - 4.5


example = car_gui()
example.run()
