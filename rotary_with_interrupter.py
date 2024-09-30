from gpiozero import LED, OutputDevice, DigitalInputDevice, Button
from time import sleep
from signal import pause
from datetime import datetime

# Define GPIO pins
IN1 = OutputDevice(27)
IN2 = OutputDevice(17)
IN3 = OutputDevice(22)
IN4 = OutputDevice(18)

interrupter_left = Button(23)
interrupter_right = Button(24)

interrupter_value = {
    "left": False,
    "right": False
}

interrupter_count = 0
interrupter_direction = 1

def print_value(btn_value):
    print("Time", datetime.now().strftime("%H:%M:%S.%f")[:-3],
          "Left", 1 if interrupter_value["left"] else 0,
          "Right", 1 if interrupter_value["right"] else 0
          )

def set_interrupter_value(value):
    global interrupter_direction
    if value == "press_left":
        # check last value
        if not interrupter_value["left"] and not interrupter_value["right"]:
            print("Turn to the right 34")
            # Turn to the Right
            interrupter_direction = 1
        elif interrupter_value["left"] and interrupter_value["right"]:
            print("Turn to the left 38")
            # Turn to the left
            interrupter_direction = -1
        
        # assign new value
        interrupter_value["left"] = False
    elif value == "release_left":
        # check last value
        if interrupter_value["left"] and interrupter_value["right"]:
            print("Turn to the right 47")
            # Turn to the right
            interrupter_direction = 1
        elif not interrupter_value["left"] and not interrupter_value["right"]:
            print("Turn to the left 51")
            # Turn to the left
            interrupter_direction = -1
        
        # assign new value
        interrupter_value["left"] = True     
    elif value == "press_right":
        # check last value
        if interrupter_value["left"] and interrupter_value["right"]:
            print("Turn to the right 60")
            # Turn to the right
            interrupter_direction = 1
        elif not interrupter_value["left"] and not interrupter_value["right"]:
            print("Turn to the left 64")
            # Turn to the left
            interrupter_direction = -1
        
        # assign new value
        interrupter_value["right"] = False
    elif value == "release_right":
        # check last value
        if not interrupter_value["left"] and not interrupter_value["right"]:
            print("Turn to the right 73")
            # Turn to the right
            interrupter_direction = 1
        elif interrupter_value["left"] and interrupter_value["right"]:
            print("Turn to the left 77")
            # Turn to the left
            interrupter_direction = -1
        
        # assign new value
        interrupter_value["right"] = True
        
        global interrupter_count
        interrupter_count += interrupter_direction
        print(interrupter_count)

interrupter_left.when_pressed = lambda : set_interrupter_value("press_left")
interrupter_left.when_released = lambda : set_interrupter_value("release_left")
interrupter_right.when_pressed = lambda : set_interrupter_value("press_right")
interrupter_right.when_released = lambda : set_interrupter_value("release_right")

# Define stepper direcection
step_dir = True # True its means step direction to the right and False step direction to the left

# Define step sequence
step_seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

def set_step(w1, w2, w3, w4):
    IN1.value = w1
    IN2.value = w2
    IN3.value = w3
    IN4.value = w4

def stepper_step(delay, steps):
    for _ in range(steps):
        stepper_dir = (step_seq, step_seq[::-1])[step_dir]
        for step in stepper_dir:
            set_step(step[0], step[1], step[2], step[3])
            sleep(delay)
            
step_revolution = 0

try:
    while step_revolution < 1:
        stepper_step(0.001, 50)
        if step_revolution == 10:
            step_revolution = 0
            #step_dir = not step_dir
        step_revolution += 1
        
    print("Count", interrupter_count)
    set_step(0, 0, 0, 0)
    pass
        
except KeyboardInterrupt:
    set_step(0, 0, 0, 0)
    pass

#pause()