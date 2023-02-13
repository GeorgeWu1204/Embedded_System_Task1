from Sensors.sensor import sensor_group
# from Actuator.servo import MyServo
# from Actuator.Speaker import speaker
from Actuator.Acturator import acturator
from Communication.Communication import communication

import threading
import paho.mqtt.client as mqtt

import time

class top_design:
    def __init__(self, id, mode):
        self.name = id
        self.mode = mode
        self.Sensors = sensor_group(self.name, max30101_=True, si7021_=True, hx711_=False, pir501_= True, noise_ = True)
        self.Actuators = acturator (self.name, self.mode)
        self.Comm = communication()
        self.send_message_from_sensors = {}
        self.send_message_from_actuator = {}
        self.receive_message = {}
        
    def debug_perpose(self, lock_1, lock_2, lock_3):
        while True:
            with lock_1:
                msg_1 = self.send_message_from_sensors
                print("send_message_from_sensor :", msg_1)

            with lock_2:
                msg_2 = self.send_message_from_actuator
                print("send_message_from_actuator :", msg_2)

            with lock_3:
                msg_3 = self.receive_message
                print("Received message :", msg_3)
            time.sleep(10)


    def start_monitor(self):
        downloaded = threading.Event()
        lock_receive = threading.Lock()
        lock_send_from_sensor = threading.Lock()
        lock_send_from_acturator = threading.Lock()

        monitor_thread = threading.Thread(target=self.Sensors.low_power_monitor_mode, args=(self.send_message_from_sensors, lock_send_from_sensor))  
        actuator_thread = threading.Thread(target=self.Actuators.controlActurator, args=(self.receive_message, lock_receive, downloaded)) 
        debug_thread = threading.Thread(target=self.debug_perpose, args=(lock_send_from_sensor, lock_send_from_acturator, lock_receive))   
        monitor_thread.start()
        # print("monitor start")
        #actuator_thread.start()
        debug_thread.start()
        print("actuator_thread start")
        print("start Communication")
        self.Comm.start_communication(self.send_message_from_sensors,  self.receive_message, downloaded, lock_send_from_sensor, lock_receive   )

    
    

test = top_design("5", "ggg")
test.start_monitor()
# test.Actuators.Speaker.checkInLocal(" ")





