import time
from Sensors.generalsensor import gen_sensor_control



class Si7021(gen_sensor_control):    
    def get_temperature_celsius(self):
        measured_data = self.take_one_measurement()
        RealTem = (175.72 * measured_data)/65536 - 46.85
        return RealTem 
    
    def get_humidity_percentage(self):
        self.modify_operation_mode([0xF5])
        measured_data = self.take_one_measurement()
        RealHum = (125 * measured_data)/65536 - 6
        return RealHum

    
        

    










