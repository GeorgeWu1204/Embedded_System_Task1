
from gpiozero import OutputDevice as stepper
from time import sleep

# Define the DRV8825 pin connections
step_pin = stepper(20)
dir_pin = stepper(21)
ms2 = stepper(12)
ms1 = stepper(1)
ms0 = stepper(7)

ms2.on()
ms1.on()
ms0.on()

delay = 0.0001

seq_cw = [[1,0,0,1], [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1]]

seq_ccw = [[0,0,0,1], [0,0,1,1], [0,0,1,0], [0,1,1,0], [0,1,0,0], [1,1,0,0], [1,0,0,0], [1,0,0,1]]

dir_pin.value = 1
print("connect to the power source")
sleep(8)
print("start")

#initial movement
print("initial ")
for i in range(80):
    for halfstep in range(8):
        for pin in range(4):
            step_pin.value = seq_cw[halfstep][pin]
            sleep(delay)
sleep (0.5)
print("complete intial")

for i in range(600):
    print("inside the loop ", i % 3)
    if i % 100 == 0:
        print("reach position")
        print("test if it could keep in this position")
        sleep(0.5)
        dir_pin.value = 1 - dir_pin.value
        seq = seq_ccw if dir_pin.value == 0 else seq_cw
    for halfstep in range(8):
        for pin in range(4):
            step_pin.value = seq[halfstep][pin]
            sleep(delay)

