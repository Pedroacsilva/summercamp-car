#!/usr/bin/env python

#Travão
#Deve ler a posição do pedal através da GUI ou potencialmente através do teclado.
import keyboard
import can
import time
from can.interface import Bus

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)

position = 0


while True:
    # Wait for the next event.
	time.sleep(0.1)
	if(keyboard.is_pressed('e')):
		if position < 100:
			position += 5
	if(keyboard.is_pressed('d')):
		if position > 0:
			position -= 5
	if(keyboard.is_pressed('q')):
		exit()

	message = can.Message(data = position.to_bytes(8, 'big'), arbitration_id = 0x02)
	try:
		bus.send(message)
		#print(f"TRAVAO: {bus.channel_info}. Position: ", position)
	except can.CanError:
		print("Message NOT sent")



	

