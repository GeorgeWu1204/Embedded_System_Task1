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
        self.Sensors = sensor_group(self.name, max30101_=True, si7021_=True, hx711_=False, pir501_= False, noise_ = False)
        self.Actuators = acturator (self.name, self.mode)
        self.Comm = communication()
        self.send_message_from_sensors = ''
        self.send_message_from_actuator = ''
        self.receive_message = ''
        
    def debug_perpose(self):
        print("send_message_from_sensor :", self.send_message_from_sensors)
        print("send_message_from_actuator :", self.send_message_from_actuator)
        print("Received message :", self.receive_message)
        time.sleep(10)



    def start_monitor(self):
        lock_receive = threading.Lock()
        lock_send_from_sensor = threading.Lock()
        lock_send_from_acturator = threading.Lock()
        self.receive_message = {'music':True, 'rock':False}

        monitor_thread = threading.Thread(target=self.Sensors.low_power_monitor_mode, args=(self.send_message_from_sensors, lock_send_from_sensor))  
        actuator_thread = threading.Thread(target=self.Actuators.controlActurator, args=(self.receive_message, self.send_message_from_actuator, lock_receive, lock_send_from_acturator)) 
        debug_thread = threading.Thread(target=self.debug_perpose)   
        # monitor_thread.start()
        # print("monitor start")
        actuator_thread.start()
        debug_thread.start()
        print("actuator_thread start")
        print("start Communication")
        self.Comm.start_communication(self.send_message_from_sensors, self.send_message_from_actuator, self.receive_message, lock_send_from_sensor, lock_receive ,lock_send_from_acturator  )

    
    

test = top_design("5", "ggg")
test.start_monitor()





