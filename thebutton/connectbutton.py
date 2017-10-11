import requests
import time

# URL for both GETs (status checks) and POSTs (button pushes)
url = "http://192.168.1.56:3000/"

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
    try:
        return requests.get(url).status_code == 200
    except requests.exceptions.RequestException:
        return False


# Pi stuff
def check_ok():
    return True;


def check_not_ok():
    return True


def is_button_pushed():
    return True


def click():
    # POST to url
    try:
        return requests.post(url).status_code == 200
    except requests.exceptions.RequestException:
        return False


def click_success():
    return True


def click_failure():
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
    time.sleep(sleep)
