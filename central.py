#!/usr/bin/env python

#ECU Central
#Deverá receber mensagens do motor, travagem e do travão de mão e desenhar no GUI
import can
import time
import os
import struct
from can.bus import BusState

def mps_2_kph(mps):
    mph = mps * 3600
    kph = mph / 1000
    return kph



bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)
#bus.state = BusState.PASSIVE
acelerador = 0
travao = 0
aceleracao = 0
travagem = 0
carro_x = 0
velocidade_carro = 0
velocidade_max = 250000 / 3600
t_new = time.clock_gettime(time.CLOCK_MONOTONIC)
t_old = t_new
try:
    while True:
        msg = bus.recv(0.05)
        if msg is not None:
            id = msg.arbitration_id

#            print("ID: ", id)
            if id == 0x01:
                acelerador = int.from_bytes(msg.data, 'big')
            if id == 0x02:
                travao = int.from_bytes(msg.data, 'big')
            if id == 0x03:
                aceleracao = struct.unpack('f', msg.data)[0]
            if id == 0x04:
                travagem = struct.unpack('f', msg.data)[0]

        t_old = t_new
        t_new = time.clock_gettime(time.CLOCK_MONOTONIC)
        delta_t = t_new - t_old
        velocidade_carro = max(velocidade_carro + (aceleracao - travagem) * delta_t, 0)
        if(velocidade_carro > velocidade_max):
            velocidade_carro = velocidade_max
        print("Posição do acelerador:", acelerador,".\tPosição do travão: ", travao, ".\tAceleração: ", round(aceleracao, 2), ".\tTravagem: ", round(travagem, 2), ".")
        print("Velocidade: ", round(mps_2_kph(velocidade_carro), 2), " k/h.\tAceleração Resultante: ", round(aceleracao - travagem, 2), " ms⁻²")
        vlc_bytes = bytearray(struct.pack("f", round(mps_2_kph(velocidade_carro), 2)))
        try:
            msg_out = can.Message(data = vlc_bytes, arbitration_id = 0x07, check = True)
            bus.send(msg_out)
        except can.CanError:
            print("Message NOT sent")


#        bus.flush_tx_buffer()
except KeyboardInterrupt:
    pass

