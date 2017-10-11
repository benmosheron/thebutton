import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pins = [2,3,4]
act = { pins[0]:10000, pins[1]:5000, pins[2]:10 }
buttPin = 14
sleepTime = 0.1

buttDelayInit = 0.1
buttDelayMax = 0.1
buttDelayMin = 0.0000001
buttDelay = buttDelayInit

GPIO.setup(buttPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

while True:
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(buttDelay)
        if not GPIO.input(buttPin):
            buttDelay *= 0.99
            if buttDelay < buttDelayMin:
                buttDelay = buttDelayMin
        else:
            buttDelay *= 1.01
            if buttDelay > buttDelayMax:
                buttDelay = buttDelayMax

        if buttDelay > buttDelayMin * act[pin]:
            GPIO.output(pin, GPIO.LOW)
            time.sleep(buttDelay)