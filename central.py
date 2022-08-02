#!/usr/bin/env python

#ECU Central
#Deverá receber mensagens do motor, travagem e do travão de mão e desenhar no GUI
import can
import time
import os
import struct
from can.bus import BusState
from enum import Enum

class State(Enum):
    PARKED = 1
    READY = 2
    DRIVING = 3

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
state = State.READY
handbrake = False
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
            if id == 0x05:
                handbrake = msg.data

        t_old = t_new
        t_new = time.clock_gettime(time.CLOCK_MONOTONIC)
        delta_t = t_new - t_old
        velocidade_carro = max(velocidade_carro + (aceleracao - travagem) * delta_t, 0)
        if(velocidade_carro > velocidade_max):
            velocidade_carro = velocidade_max
        if handbrake == True and state != State.DRIVING:
            velocidade_carro = 0        #Forçar velocidade a 0
        print("Posição do acelerador:", acelerador,".\tPosição do travão: ", travao, ".\tAceleração: ", round(aceleracao, 2), ".\tTravagem: ", round(travagem, 2), ".")
        print("Velocidade: ", round(mps_2_kph(velocidade_carro), 2), " k/h.\tAceleração Resultante: ", round(aceleracao - travagem, 2), " ms⁻²")

        if velocidade_carro != 0:
            time_stopped == 0
        if velocidade_carro == 0:
            time_stopped = time_stopped + delta_t


        if velocidade_carro == 0 and time_stopped > 30 and state == State.DRIVING:
            state = State.READY

        if mps_2_kph(velocidade_carro) > 10 and state == State.READY:
            state = State.DRIVING

        if state == State.PARKED and handbrake == False:
            state = State.READY

        if state == State.READY and handbrake == True:
            state = State.PARKED


        try:
            msg_out = can.Message(data = state, arbitration_id = 0x06, check = True)
            bus.send(msg_out)
        except can.CanError:
            print("Message NOT sent")



        vlc_bytes = bytearray(struct.pack("f", round(mps_2_kph(velocidade_carro), 2)))
        try:
            msg_out = can.Message(data = vlc_bytes, arbitration_id = 0x07, check = True)
            bus.send(msg_out)
        except can.CanError:
            print("Message NOT sent")


#        bus.flush_tx_buffer()
except KeyboardInterrupt:
    pass

