#!/usr/bin/env python

#Travagem
#Deverá receber uma mensagem CAN do travão e produzir uma desaceleração de acordo com a posição do pedal
#Desaceleração máxima é 6 m/s²
import can
import time
import struct
from can.bus import BusState


bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)
#bus.state = BusState.PASSIVE
try:
    while True:
        msg = bus.recv(0.000001)

        if msg is not None and msg.arbitration_id == 0x02:
#            print(msg)
            posicao_pedal = int.from_bytes(msg, 'big')
            travagem = posicao_pedal / (100 / 6)
#            print("Travagem: ", travagem)
        desacl_bytes = bytearray(struct.pack("f", travagem))
        msg_out = can.Message(data = desacl_bytes, arbitration_id = 0x04)
        bus.send(msg_out)
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

