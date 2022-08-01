#!/usr/bin/env python

#Travagem
#Deverá receber uma mensagem CAN do travão e produzir uma desaceleração de acordo com a posição do pedal
#Desaceleração máxima é 6 m/s²
from io import BufferedReader
import can
import time
import struct
from can.bus import BusState

travagem = 0
posicao_pedal = 0

def msg_handler(msg):
    if msg.arbitration_id == 0x02:
        posicao_pedal = int.from_bytes(msg, 'big')
        desacl_bytes = bytearray(struct.pack("f", travagem))



bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)
#listener = BufferedReader()
try:
    while True:

        msg = bus.recv(0.05)
        #listener(msg)
        if msg is not None and msg.arbitration_id == 0x02:
            posicao_pedal = int.from_bytes(msg, 'big')
            travagem = posicao_pedal / (100 / 6)
            
        try:
            desacl_bytes = bytearray(struct.pack("f", travagem))
            msg_out = can.Message(data = desacl_bytes, arbitration_id = 0x04, check = True)
            bus.send(msg_out)
          #  print(f"TRAVAGEM. {bus.channel_info}. Travagem: ", travagem)
        except can.CanError:
            print("Message NOT sent")
#        time.sleep(0.05)

except KeyboardInterrupt:
    pass

