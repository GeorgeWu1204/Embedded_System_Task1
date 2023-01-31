#I2C
from Sensors.si7021TemHumid import Si7021
from Sensors.Max30101 import max30101
#GPIO
from Sensors.noise_sensor import noise_sensor
from Sensors.PIR501 import pir501
from Sensors.hx711 import HX711
#Actuator
# from Actuator.servo import MyServo
import smbus2
import threading
import time


Si7021_I2C_port = 0x40
Max30101_I2C_port = 0x57
Noise_sensor_GPIO = 26
Pir501_GPIO = 5
Hx711_DT_GPIO = 6
Hx711_SCK_GPIO = 21
Servo_GPIO = 13
GPIO_Detection_Period = 10
Heart_beat_lower_bound = 60
Heart_beat_upper_bound = 100
def Average(lst):
    return sum(lst) / len(lst)


class sensor_group():
    def __init__(self,si7021_ = False ,max30101_ = False, hx711_ = False, pir501_ = False, noise_ = False, servo_ = False ):
        bus = smbus2.SMBus(1)
        if(si7021_ == True):
            self.Si = Si7021(Si7021_I2C_port, [0xF3], 'TemHum_1', bus)
            print("Si7021 Humidity and Temperature Sensor initialized")
        else:
            self.Si = None
        if(max30101_ == True):
            self.Max = max30101(Max30101_I2C_port, bus)
            print("Max30101 Heart Rate Sensor initialized")
        else:
            self.Max = None
        if(hx711_ == True):
            self.Hx = HX711(Hx711_DT_GPIO, Hx711_SCK_GPIO)
            print("Hx711 Load Force sensor initialized")
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
        if (servo_):
            print("not implemented yert")
        self.detect_danger = None
        self.heart_rate_per_minute = 0
        self.heart_avg = 0
        self.avg_temperature = 0
        self.avg_humidity = 0


    def I2C(self,time_requirement):
        print("Perform I2C testing")
        timer = 0
        T_list = [0]*20
        H_list = [0]*20
        record_index = 0
        
        while timer < time_requirement: 
            time.sleep(0.5)
            timer += 1
            
            record_index += 1
            if(record_index % 20 == 0):
                self.avg_temperature = Average(T_list)
                self.avg_humidity = Average(H_list)
                record_index = 0
            else:
                T_list[record_index] = self.Si.get_temperature_celsius()
                H_list[record_index] = self.Si.get_humidity_percentage()
                
            self.heart_rate_per_minute, self.heart_avg = self.Max.take_heartbeat_rate()
            if(self.heart_avg < Heart_beat_lower_bound or self.heart_avg > Heart_beat_upper_bound):
                self.detect_danger.set()
        


    def low_power_monitor_mode(self):
        print("Starting low_power monitoring")
        #multi_threading by GPIO
        self.detect_danger = threading.Event()
        self.detect_danger.clear()
        t_1 = threading.Thread(target=self.Noise.start_detection, args=(100, self.detect_danger, GPIO_Detection_Period))
        t_2 = threading.Thread(target=self.Pir.start_detection, args = (100, self.detect_danger, GPIO_Detection_Period))
        # t_3 = threading.Thread(target=self.Hx.)
        t_1.start()
        t_2.start()
        # while self.detect_danger.is_set() == False:
        #     time.sleep(5)
        # if event.is_set():
        self.I2C(1000)
        t_1.join()
        print("Stop detecting noise")
        t_2.join()
        print("Stop detecting movement")



        


x = sensor_group(pir501_=True, noise_=True)
x.low_power_monitor_mode()



        
        

        