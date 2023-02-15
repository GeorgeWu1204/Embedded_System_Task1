from gpiozero import OutputDevice as stepper
from time import sleep
import math

# Define the DRV8825 pin connections
step_pin = stepper(19)
dir_pin = stepper(26)
# Define the step delay
delay = 0.05

# Define the step sequence for clockwise rotation
seq_cw = [[1,0,0,1], [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1]]

# Define the step sequence for anticlockwise rotation
seq_ccw = [[0,0,0,1], [0,0,1,1], [0,0,1,0], [0,1,1,0], [0,1,0,0], [1,1,0,0], [1,0,0,0], [1,0,0,1]]

# Set the initial direction of the motor to clockwise
dir_pin.value = 1

# Define the maximum speed of the motor (in steps per second)
max_speed = 200

# Define the number of degrees to rotate the motor
degrees = 45

# Calculate the number of steps needed to rotate the motor by the desired number of degrees
# Note: This calculation assumes that the motor has a step angle of 1.8 degrees per step
# steps_per_revolution = 360 / 1.8
# steps = int(steps_per_revolution * degrees / 360)
steps = 5
print("connect to the power source")
sleep(10)

# Loop through the sequence and activate the appropriate GPIO pins
for i in range(steps):
    # Gradually change the speed of the motor when changing direction
    if dir_pin.value == 1 and i >= 0 and i % 5 == 0:
        for j in range(20):
            delay *= 1.2
            sleep(0.01)
        dir_pin.value = 0
        seq = seq_ccw
        for j in range(20):
            delay /= 1.2
            sleep(0.01)
    elif dir_pin.value == 0 and i >= 0 and i % 5 == 0:
        for j in range(20):
            delay *= 1.2
            sleep(0.01)
        dir_pin.value = 1
        seq = seq_cw
        for j in range(20):
            delay /= 1.2
            sleep(0.01)
    
    # Activate the appropriate GPIO pins to take one step
    for halfstep in range(8):
        for pin in range(4):
            step_pin.value = seq[halfstep][pin]
            sleep(delay)

