#!/usr/bin/env python

#ECU Central
#Deverá receber mensagens do motor, travagem e do travão de mão e desenhar no GUI
import can
import time
import struct
from can.bus import BusState


bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)
#bus.state = BusState.PASSIVE
acelerador = 0
travao = 0
aceleracao = 0
travagem = 0
try:
    while True:
        msg = bus.recv(0.000001)
        if msg is not None:
            id = msg.arbitration_id
            print("ID: ", id)
            if id == 0x01:
                acelerador = int.from_bytes(msg.data, 'big')
            if id == 0x02:
                travao = int.from_bytes(msg.data, 'big')
            if id == 0x03:
                aceleracao = struct.unpack('>f', msg.data)
            if id == 0x04:
                travagem = struct.unpack('>f', msg.data)
        print("\rPosição do acelerador:", acelerador,".\tPosição do travão: ", travao, ".\tAceleração: ", aceleracao, ".\tTravagem: ", travagem, ".")
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

