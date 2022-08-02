#!/usr/bin/env python

#Travão de mão
#Deve reagir a travão de mão + publicar com cadência 100ms
import keyboard
import can
import time
from can.interface import Bus

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)

parking_brake = False


while True:
    # Wait for the next event.
	time.sleep(0.1)
	if(keyboard.is_pressed('f')):
		parking_brake = ~parking_brake

	message = can.Message(data = parking_brake, arbitration_id = 0x05)
	try:
		bus.send(message)
		#print(f"ACELERADOR. {bus.channel_info}. Posição: ", position)
	except can.CanError:
		print("Message NOT sent")



	

