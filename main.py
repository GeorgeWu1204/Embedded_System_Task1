from Sensors.si7021TemHumid import Si7021
import smbus2
import time
import sys

# bus = smbus2.SMBus(1)

# abc = Si7021(0x40, [0xF3], 'TemHum_1', bus)
# abc.modify_measure_time(0.2)
# abc.return_infor()
# result = abc.get_temperature_celsius()
# result2 = abc.get_humidity_percentage()
# print("test result temperature", result)
# print("test result humidity", result2)





referenceUnit = 1
import RPi.GPIO as GPIO
from hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
        
    print("Bye!")
    sys.exit()


hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")


hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")


while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)
        print(val)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()