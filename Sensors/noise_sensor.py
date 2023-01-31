import RPi.GPIO as GPIO
import time
import threading


class noise_sensor():
    def __init__(self, channel = 17):
        self.channel = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)
        self.event = None
        self.detection_count = 0

    def callback(self, channel):
        if GPIO.input(channel):
                print("Sound Detected!")
        else:
                print("Sound Detected!")
        
        self.detection_count += 1
        if (self.detection_count >= 5) and (self.event.is_set() == False):
            self.event.set()
            self.detection_count = 0

    def start_detection(self, time_requirement = None, event = None, detection_period = 10):
        self.event = event
        GPIO.add_event_detect(self.channel, GPIO.BOTH, bouncetime=500)  # let us know when the pin goes HIGH or LOW
        GPIO.add_event_callback(self.channel, self.callback)  # assign function to GPIO PIN, Run function on change
        # infinite loop
        timer = 0
        detect_val = 0
        while time_requirement == None or (timer < time_requirement and time_requirement != None):
                original_cout = self.detection_count
                time.sleep(0.5)
                timer += 1
                if(timer % detection_period == 0):
                    self.detection_count = 0


        GPIO.remove_event_detect (self.channel)
    
