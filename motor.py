#!/usr/bin/env python

#Motor
#Deverá receber uma mensagem CAN do acelerador e produzir uma aceleração de acordo com a posição do pedal
#Aceleração máxima é 5 m/s²(a 8000RPM)
import can
import time
import struct
from can.bus import BusState


bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)
#bus.state = BusState.PASSIVE
aceleracao = 0
try:
    while True:
        msg = bus.recv(0.000001)
        if msg is not None and msg.arbitration_id == 0x01:
            posicao_pedal = int.from_bytes(msg, 'big')
            rpm = posicao_pedal * 80
            aceleracao = posicao_pedal / 20
            print("RPM: ", rpm)

        acl_bytes = bytearray(struct.pack("f", aceleracao))
#        print(f"Aceleracao: ", aceleracao)
        try:
            msg_out = can.Message(data = acl_bytes, arbitration_id = 0x03, check = True)
            bus.send(msg_out)
            print(f"MOTOR. {bus.channel_info}. Aceleração: ", aceleracao)
        except can.CanError:
            print("Message NOT sent")

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

