#!/usr/bin/env python

#Motor
#Deverá receber uma mensagem CAN do acelerador e produzir uma aceleração de acordo com a posição do pedal
#Aceleração máxima é 5 m/s²(a 8000RPM)
import can
import time
import struct
from can.bus import BusState


bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500)
#bus.state = BusState.PASSIVE
try:
    while True:
        msg = bus.recv(None)

        if msg is not None and msg.arbitration_id == 0x01:
#            print(msg)
            posicao_pedal = int.from_bytes(msg, 'big')
            rpm = posicao_pedal * 80
            aceleracao = posicao_pedal / 20
            print("RPM: ", rpm, "\nAceleração: ", aceleracao)
#        msg_out = can.Message(data = aceleracao.to_bytes(8, 'big'), arbitration_id = 0x03)
        acl_bytes = bytearray(struct.pack("f", aceleracao))
        msg_out = can.Message(data = acl_bytes, arbitration_id = 0x03)
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

