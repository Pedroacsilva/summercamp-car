#!/usr/bin/env python

#Acelerador
#Deverá receber uma mensagem CAN da ECU principal (slider na GUI). Por enquanto, recebi input do teclado (W)
#A cada frame a que W é premido, incrementa a posição do acelerador
import keyboard
import can
import time
from can.interface import Bus

position = 0


bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)



while True:
    # Wait for the next event.
    time.sleep(0.1)
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'w':
        if position < 100:
        	position += 5
        	print("Posição do pedal: ", position)
        	message = can.Message(data = position)
        	try:
	        	bus.send(msg)
	        	print(f"Message sent on {bus.channel_info}.")
        	except can.CanError:
        			print("Message NOT sent")

    if event.event_type == keyboard.KEY_DOWN and event.name == 's':
        if position > 0:
        	position -= 5
        	print("Posição do pedal: ", position)
    if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
   		exit()
