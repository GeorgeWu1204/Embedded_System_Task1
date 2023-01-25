from Sensors.Si7021TemHumid import Si7021
import smbus2

bus = smbus2.SMBus(1)

abc = Si7021(0x40, [0xF3], 'TemHum_1', bus)
abc.modify_measure_time(0.2)
abc.return_infor()
result = abc.get_temperature_celsius()
result2 = abc.get_humidity_percentage()
print("test result temperature", result)
print("test result humidity", result2)

