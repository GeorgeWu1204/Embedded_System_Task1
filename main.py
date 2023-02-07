from Sensors.sensor import sensor_group
# from Actuator.servo import MyServo
# from Actuator.Speaker import speaker
from Actuator.Acturator import acturator
from Communication.Communication import communication

import threading
import paho.mqtt.client as mqtt

from time import time




class top_design:
    def __init__(self, id, mode):
        self.name = id
        self.mode = mode
        self.Sensors = sensor_group(self.name, max30101_=True, si7021_=True, hx711_=True, pir501_= True, noise_ = True)
        self.Actuators = acturator (self.name, self.mode)
        
        self.Comm = communication()
        self.send_message = ''
        self.receive_message = ''
        

    def start_monitor(self):
        lock_receive = threading.Lock()
        lock_send = threading.Lock()

        monitor_thread = threading.Thread(target=self.Sensors.low_power_monitor_mode, args=(self.send_message, lock_send))  
        actuator_thread = threading.Thread(target=self.Actuators.controlActurator, args=(self.receive_message, lock_receive))    

        monitor_thread.start()
        print("monitor start")
        # actuator_thread.start()
        # print("actuator_thread start")

        # print("start Communication")
        # self.Comm.start_communication(self.send_message, self.receive_message)

    
    

test = top_design("5", "ggg")
test.start_monitor()





