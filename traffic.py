#!/usr/bin/python3
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from time import sleep
from random import randint, choice

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
# pins = {
#     17 : {'name' : 'red', 'state' : GPIO.LOW},
#     27 : {'name' : 'yellow', 'state' : GPIO.LOW},
#     22 : {'name' : 'green', 'state' : GPIO.LOW},
# }

pins = {
    'red' : [17, GPIO.LOW],
    'yellow' : [27, GPIO.LOW],
    'green' : [22, GPIO.LOW]
}


# Set each pin as an output and make it low:
for pin, state in pins.values():
    # print(pin)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def humanize_pin_state(pins):
    for name, values in pins.items():
        pin_state = values[1]
        if pin_state == GPIO.HIGH:
            pins[name][1] = 'on'
        else:
            pins[name][1] = 'off'
    return pins

@app.route("/")
def main():
    getPinState()
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins' : humanize_pin_state(pins)
        }
    # Pass the template data into the template main.html and return it to the user
    return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
# changePin is now color name
@app.route("/toggle/<color>/<action>")
def action(color, action):
    # Convert the pin from the URL into an integer:
    changePin = pins[color][0]
    # Get the device name for the pin being changed:
    # deviceName = pins[changePin]['name']
    deviceName = color
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."
    if action == "toggle":
        # Read the pin and set it to whatever it isn't (that is, toggle it):
        GPIO.output(changePin, not GPIO.input(changePin))
        message = "Toggled " + deviceName + "."
    if action == "party":
        for i in range(1,20):
            blinkyBlink(changePin)
        message = "Partied Hard"

    getPinState()

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'message' : message,
        'pins' : humanize_pin_state(pins)
    }

    return render_template('main.html', **templateData)

@app.route("/rager/")
@app.route("/rager/<iterations>")
def partyHard(iterations = 5): #Add untested partyHard mode
    countDown()
    sleep(1)
    try:
        iterations = int(iterations)
    except:
        iterations = 5
    for i in range(iterations):
        # pin = choice(list(pins.values()))
        pin = choice(list(pins.values()))[0]
        blinkyBlink(pin)
    templateData = {
        # 'message' : message,
        'pins' : humanize_pin_state(pins)
    }
    return render_template('main.html', **templateData)

def getPinState():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin][1] = GPIO.input(pins[pin][0])

def blinkyBlink(pin):
    GPIO.output(pin, GPIO.HIGH)
    sleep(0.25)
    GPIO.output(pin, GPIO.LOW)
    sleep(0.25)

def goLow():
    for pin, state in pins.values(): 
        GPIO.output(pin, GPIO.LOW)

def countDown():
    goLow()
    sleep(.25)
    for pin, state in pins.values():
        GPIO.output(pin, GPIO.HIGH)
        sleep(1)
        GPIO.output(pin, GPIO.LOW)

# def rager(curr, prev):
#     for i in range(1,randint(4,16)):
#         curr = curr if curr != prev else choice(list(pins.keys())) #give it a second shot of being something else for a little more fun.
#         blinkyBlink(curr)
#     return curr

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
