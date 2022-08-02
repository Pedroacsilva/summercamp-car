# import CAN #
import can
import time
import os
import struct
from can.bus import BusState


bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from math import exp

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy_garden.speedmeter import SpeedMeter
from kivy_garden.led import Led
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
import operator


class NoValueSpeedMeter(SpeedMeter):

    def value_str(self, n): return ''

_displayed = { 
    0: '0',
    30: u'\u03a0 / 6', 60: u'\u03a0/3', 90: u'\u03a0/2', 120: u'2\u03a0/3',
    150: u'5\u03a0/6',
    180: u'\u03a0', 210: u'7\u03a0/6', 240: u'4\u03a0/3'
    }

Position = False

class car_gui(App):

      
    def set_speed(self):
        ids = self.root.ids
        ids.rpm.value = exp(ids.speed_value.value / 200.0) * 4.5 - 4.5


    def btn(self, value):
        if value == '1':
            Position_final = operator.not_(Position)
            message = can.Message(data = Position_final, arbitration_id=0x05)

            try:
                bus.send(message)
                print("CAN BUS 1", Position_final)
            except can.CanError:
                print("Message NOT sent")
            return 1

        if value == '0':
            Position_final = False
            message = can.Message(data = Position_final, arbitration_id=0x05)

            try:
                bus.send(message)
                print("CAN BUS 2 ", Position_final)
            except can.CanError:
                print("Message NOT sent")
            return


        

example = car_gui()
example.run()
