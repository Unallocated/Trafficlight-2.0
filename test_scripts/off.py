#!/usr/bin/python3
print('script start')
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

seq = ['red', 'yellow', 'green', 'yellow',]

pins = {
	2 : {'name' : 'red', 'state' : GPIO.LOW},
	3 : {'name' : 'green', 'state' : GPIO.LOW},
	4 : {'name' : 'yellow', 'state' : GPIO.LOW}
	}

for pin in pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

#color = input('Color? ')
def light_off():
	for i in pins:
		GPIO.output(i, GPIO.LOW)

def light_on(color):
	for i in pins:
		if pins[i]['name'] == color:
			GPIO.output(i, GPIO.HIGH)	
			time.sleep(.5)
			GPIO.output(i, GPIO.LOW)

def sequence(seq):
	while True:
		for i in seq:
			light_on(i)

#light_on(color)
#sequence(seq)
light_off()
print('script end')
