#I2C
from Sensors.Si7021TemHumid import Si7021
from Sensors.Max30101 import max30101
#GPIO
from Sensors.noise_sensor import noise_sensor
from Sensors.PIR501 import pir501
from Sensors.hx711Pack.hx711Interface import hx711Interface

import smbus2
import threading
import time
import json
import time


Si7021_I2C_port = 0x40
Max30101_I2C_port = 0x57
Noise_sensor_GPIO = 26
Pir501_GPIO = 19
Hx711_DT_GPIO = 5
Hx711_SCK_GPIO = 6
Servo_GPIO = 13
GPIO_Detection_Period = 10
Heart_beat_lower_bound = 60
Heart_beat_upper_bound = 100

def Average(lst):
    return sum(lst) / len(lst)

class sensor_group():
    def __init__(self, id, si7021_ = False ,max30101_ = False, hx711_ = False, pir501_ = False, noise_ = False):
        bus = smbus2.SMBus(1)
        if(si7021_ == True):
            self.Si = Si7021(Si7021_I2C_port, [0xF3], 'TemHum_1', bus)
            print("Si7021 Humidity and Temperature Sensor initialized")
        else:
            self.Si = None
        if(max30101_ == True):
            self.Max = max30101(address=Max30101_I2C_port, bus_=bus)
            self.Max.buildingup()
            print("Max30101 Heart Rate Sensor initialized")
        else:
            self.Max = None
        if(hx711_ == True):
            self.Hx = hx711Interface(Hx711_DT_GPIO, Hx711_SCK_GPIO)
            print("Hx711 Load Force sensor initialized")
            self.Hx.setup()
        else:
            self.Hx = None
        if(pir501_ == True):
            self.Pir = pir501(Pir501_GPIO)
            print("Pir501 Movement sensor initialized")
        else:
            self.Pir = None
        if(noise_ == True):
            self.Noise = noise_sensor(Noise_sensor_GPIO)
            print("Noise sensor initialized")
        else:
            self.Noise = None
        
        self.name = id
        self.data_storage = None
        # self.detect_danger = False
        self.heart_rate_per_minute = 0
        self.heart_avg = 0
        self.avg_temperature = 0
        self.avg_humidity = 0
        self.msg = None
        self.onbed = threading.Event()
        self.crying = threading.Event()
        self.awake = threading.Event()


    def I2C(self,time_requirement):
        print("Perform I2C testing")
        timer = 0
        T_list = [0]*5
        H_list = [0]*5
        record_index = 0
        self.Max.setup()

        while timer < time_requirement: 
            # time.sleep(0.1)
            timer += 1
            record_index += 1
            # print("heart_rater str ")
            self.heart_rate_per_minute, self.heart_avg = self.Max.take_heartbeat_rate(400)  
            # print("heart_rater done ")
            if(record_index % 5 == 0):
                self.avg_temperature = Average(T_list)
                self.avg_humidity = Average(H_list)

                record_index = 0
                print("heart_rate_ ", self.heart_avg)
                print("temperature_ ", self.avg_temperature)
                print("humidity_ :", self.avg_humidity)
            else:
                T_list[record_index] = self.Si.get_temperature_celsius()
                H_list[record_index] = self.Si.get_humidity_percentage()       






            # if(self.heart_avg < Heart_beat_lower_bound or self.heart_avg > Heart_beat_upper_bound):
            #     self.detect_danger.set()
            
        


    def low_power_monitor_mode(self, message, lock):
        input('Press Enter to begin reading to Starting low_power monitoring')
        print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
        #multi_threading by GPIO
        self.onbed = threading.Event()
        self.crying = threading.Event()
        self.awake = threading.Event()
        #GPIO threading start
        t_1 = threading.Thread(target=self.Noise.start_detection, args=(100, self.crying, GPIO_Detection_Period))
        t_2 = threading.Thread(target=self.Pir.start_detection, args = (100, self.awake, GPIO_Detection_Period))
        t_3 = threading.Thread(target=self.Hx.start_detection, args = (100, self.onbed, GPIO_Detection_Period))
        t_4 = threading.Thread(target=self.pack_data, args=(message, lock))
        t_1.start()
        t_2.start()
        t_3.start()
        t_4.start()

        # Start I2C detection on main thread.
        while True:
            # print("check status ")
            # print("crying ", self.crying)
            # print("awake ", self.awake)
            # print("onbed", self.onbed)
            self.I2C(time_requirement=5) # running time 1000*0.5 m
            
            

        t_1.join()
        print("Stop detecting noise")
        t_2.join()
        print("Stop detecting movement")
    
    
    def pack_data(self, message, lock):
        while True:
            self.data_storage = {
                "onbed" : self.onbed.is_set(), 
                "crying" : self.crying.is_set(), 
                "awake" : self.awake.is_set(),
                "heart_rate" : self.heart_avg, 
                "temperature" : self.avg_temperature, 
                "humidity" : self.avg_humidity
            }
            send_msg = {"id" : self.name, "data": self.data_storage}
            self.msg = json.dumps(send_msg)
            print(self.msg)
            lock.acquire()
            message = self.msg
            lock.release()
            time.sleep(10)







    # def pack_data(self):

    #     self.data_storage = {
    #         "onbed" : self.onbed.is_set(), 
    #         "crying" : self.crying.is_set(), 
    #         "awake" : self.awake.is_set(),
    #         "heart_rate" : self.heart_avg, 
    #         "temperature" : self.avg_temperature, 
    #         "humidity" : self.avg_humidity
    #     }
    #     send_msg = {"id" : self.name, "data": self.data_storage}
    #     self.msg = json.dumps(send_msg)
    #     print(self.msg)

# test_group = sensor_group("1")
# test_group.pack_data()


        





        
        

        