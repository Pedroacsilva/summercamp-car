#!/usr/bin/env python

#Acelerador
#Deve ler a posição do pedal através da GUI ou potencialmente através do teclado.
import keyboard
import can
import time
from can.interface import Bus

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500)

position = 0


while True:
    # Wait for the next event.
	time.sleep(0.1)
	if(keyboard.is_pressed('w')):
		if position < 100:
			position += 5
	if(keyboard.is_pressed('s')):
		if position > 0:
			position -= 5
	if(keyboard.is_pressed('q')):
		exit()

	message = can.Message(data = position.to_bytes(8, 'big'), arbitration_id = 0x01)
	try:
		bus.send(message)
		print(f"Message sent on {bus.channel_info}. Position: ", position)
	except can.CanError:
		print("Message NOT sent")



	

