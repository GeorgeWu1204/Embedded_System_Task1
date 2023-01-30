#!/usr/bin/python
import RPi.GPIO as GPIO
import time


# def callback(channel):
#         if GPIO.input(channel):
#                 print("Sound Detected!")
#         else:
#                 print("Sound Detected!")


class noise_sensor():
    def __init__(self, channel = 17):
        self.channel = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)

    def callback(self, channel):
        if GPIO.input(channel):
                print("Sound Detected!")
        else:
                print("Sound Detected!")

    def start_detection(self, time_requirement = None):
        GPIO.add_event_detect(self.channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
        GPIO.add_event_callback(self.channel, self.callback)  # assign function to GPIO PIN, Run function on change

        # infinite loop
        timer = 0
        while time_requirement == None or (timer < time_requirement and time_requirement != None):
                time.sleep(1)
                timer += 1
                print("inside the loop time = %d", timer)

        GPIO.remove_event_detect (self.channel)
    
