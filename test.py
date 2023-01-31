# import time
# import smbus2

# si7021_ADD = 0x40
# si7021_READ_TEMPERATURE = 0xF3

# bus = smbus2.SMBus(1)

# #Set up a write transaction that sends the command to measure temperature
# cmd_meas_temp = smbus2.i2c_msg.write(si7021_ADD,[si7021_READ_TEMPERATURE])

# #Set up a read transaction that reads two bytes of data
# read_result = smbus2.i2c_msg.read(si7021_ADD,2)

# #Execute the two transactions with a small delay between them
# bus.i2c_rdwr(cmd_meas_temp)
# time.sleep(0.1)
# bus.i2c_rdwr(read_result)

# #convert the result to an int
# temperature = int.from_bytes(read_result.buf[0]+read_result.buf[1],'big')
# print(temperature)










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
            print("Si7021 Humidity and Temperature Sensor initialized")
        else:
            self.Si = None
        if(max30101_ == True):
            self.Max = max30101(Max30101_I2C_port)
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


        self.detect_danger = False

    def low_power_monitor_mode(self):
        print("Starting low_power monitoring")
        #multi_threading by GPIO
        event = threading.Event()


        t_1 = threading.Thread(target=self.Noise.start_detection, args=(1000, event))
        t_2 = threading.Thread(target=self.Pir.start_detection, args = (1000, event))
        # t_3 = threading.Thread(target=self.Hx.)
        
        t_1.start()
        t_2.start()

        t_1.join()
        print("finnished t_1")
        t_2.join()
        print("finnished t_2")


        if event.is_set():
            print("Perform I2C testing")



    def test(self):

        


# x = sensor_group(pir501_=True, noise_=True)
# x.test()



        
        

        