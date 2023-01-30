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


Si7021_I2C_port = 0x40
Max30101_I2C_port = 0x57
Noise_sensor_GPIO = 26
Pir501_GPIO = 5
Hx711_DT_GPIO = 6
Hx711_SCK_GPIO = 21
Servo_GPIO = 13


class sensor_group():
    def __init__(self,si7021_ = False ,max30101_ = False, hx711_ = False, pir501_ = False, noise_ = False, servo_ = False ):
        bus = smbus2.SMBus(1)
        if(si7021_ == True):
            self.Si = Si7021(Si7021_I2C_port, [0xF3], 'TemHum_1', bus)
        else:
            self.Si = None
        if(max30101_ == True):
            self.Max = max30101(Max30101_I2C_port)
        else:
            self.Max = None
        if(hx711_ == True):
            self.Hx = HX711(Hx711_DT_GPIO, Hx711_SCK_GPIO)
        else:
            self.Hx = None
        if(pir501_ == True):
            self.Pir = pir501(Pir501_GPIO)
        else:
            self.Pir = None
        if(noise_ == True):
            self.Noise = noise_sensor(Noise_sensor_GPIO)
        else:
            self.Noise = None
        if (servo_):
            print("not implemented yert")
    def test(self):
        #multi_threading by GPIO
        t_1 = threading.Thread(target=self.Noise.start_detection, args=(1000,))
        t_2 = threading.Thread(target=self.Pir.start_detection, args = (1000,))
        t_1.start()
        t_2.start()

        t_1.join()
        print("finnished t_1")
        t_2.join()
        print("finnished t_2")
        


x = sensor_group(pir501_=True, noise_=True)
x.test()



        
        

        