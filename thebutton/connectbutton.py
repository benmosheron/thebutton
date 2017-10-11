import requests
import time
import RPi.GPIO as GPIO

# URL for both GETs (status checks) and POSTs (button pushes)
url = "http://192.168.1.56:3000/"

# Time between health check polls (seconds)
healthCheckPollTimeDefault = 5

# Time between button pushes (if it's held down)
buttonCoolDown = 0.1

# Time to wait between main loop
sleep = 0

# States
init = "init"  # starting up
check = "check"  # checking the health check url via a GET
happy = "happy"  # health check OK
sad = "sad"  # health check failed

# Button states
buttReady = "buttReady"  # ready
buttClick = "buttClick"  # button clicked
buttCool = "buttCool"  # button cooling down

# LEDs
redLed = 2
yellowLed = 3
blueLed = 4
pins = [redLed, yellowLed, blueLed]

# THEBUTTON
theButton = 14

state = init
buttState = buttReady
healthCheckPollTime = healthCheckPollTimeDefault
time_at_last_check = time.time()
time_at_button_push = time.time() - buttonCoolDown

# GPIO init
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(theButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)


def get_time_since_check():
    return time.time() - time_at_last_check


def poll():
    try:
        return requests.get(url).status_code == 200
    except requests.exceptions.RequestException:
        return False


# Pi stuff
def turnOn(led):
    GPIO.output(led, GPIO.HIGH)


def turnOff(led):
    GPIO.output(led, GPIO.LOW)


def check_ok():
    turnOff(redLed)
    turnOn(blueLed)


def check_not_ok():
    turnOn(redLed)
    turnOff(blueLed)


def is_button_pushed():
    return not GPIO.input(theButton)


def click():
    # POST to url
    try:
        turnOn(yellowLed)
        return requests.post(url).status_code == 200
    except requests.exceptions.RequestException:
        return False


def click_success():
    turnOff(yellowLed)
    turnOn(blueLed)
    return True


def click_failure():
    turnOff(yellowLed)
    turnOn(redLed)
    return True


while True:
    # Check if button cooldown has passed
    if buttState == buttCool:
        if time.time() > time_at_button_push + buttonCoolDown:
            buttState = buttReady

    # Check if poll interval has passed
    if state == happy or state == sad:
        if get_time_since_check() > healthCheckPollTime:
            state = init

    if state == init:
        time_at_last_check = time.time()
        state = check
        if poll():
            state = happy
            check_ok()
        else:
            state = sad
            check_not_ok()

    if is_button_pushed():
        # valid trigger states: happy & buttReady
        if state == happy and buttState == buttReady:
            buttState = buttClick
            time_at_button_push = time.time()
            if click():
                click_success()
            else:
                click_failure()
            buttState = buttCool
            
    if sleep > 0:
        time.sleep(sleep)
