import requests
import time

# URL for both GETs (status checks) and POSTs (button pushes)
url = "http://127.0.0.1:3000/"

# Time between health check polls (seconds)
healthCheckPollTimeDefault = 5

# Time between button pushes (if it's held down)
buttonCoolDown = 1

# Time to wait between main loop
sleep = 0.5

# States
init = "init"  # starting up
check = "check"  # checking the health check url via a GET
happy = "happy"  # health check OK
sad = "sad"  # health check failed

# Button states
buttReady = "buttReady"  # ready
buttClick = "buttClick"  # button clicked
buttCool = "buttCool"  # button cooling down

state = init
buttState = buttReady
healthCheckPollTime = healthCheckPollTimeDefault
time_at_last_check = time.time()
time_at_button_push = time.time() - buttonCoolDown


def get_time_since_check():
    return time.time() - time_at_last_check


def poll():
    print("polling")
    try:
        return requests.get(url).status_code == 200
    except requests.exceptions.RequestException:
        return False


def is_button_pushed():
    return True


def click():
    # POST to url
    print("button click")
    try:
        return requests.post(url).status_code == 200
    except requests.exceptions.RequestException:
        return False


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
            print("happy")
            state = happy
        else:
            print("sad")
            state = sad

    if is_button_pushed():
        # valid trigger states: happy & buttReady
        if state == happy and buttState == buttReady:
            buttState = buttClick
            time_at_button_push = time.time()
            if click():
                print("click was OK")
            buttState = buttCool
    time.sleep(sleep)
