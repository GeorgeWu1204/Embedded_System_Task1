import time
import smbus2

# Write
# SensorAddr : Command : CmdData : CmdData .   All 1 byte
# 
# Read
# Status : SensorData : SensorData : SensorData . Sensor 3 pressure reading data + sensor status byte
#

class gen_sensor_control:
    def __init__(self, sensor_port, sensor_mode, id, bus, measure_interval = 0.2, data_size = 2):
    #initialize the sensor
        self.sensor_port = sensor_port
        self.sensor_mode = sensor_mode
        self.measure_interval = measure_interval
        self.id = id
        self.datasize = data_size
        self.bus = bus
    
    def modify_measure_time(self,time):
    #modify the measurement time
        self.measure_interval = time

    def modify_operation_mode(self,new_mode, new_data_size = 2):
    #modify the measurement mode
        self.sensor_mode = new_mode
        self.datasize = new_data_size
    
    def take_one_measurement(self):
    #manually start to take measurement 
        write_msg = smbus2.i2c_msg.write(self.sensor_port, self.sensor_mode)
        read_msg = smbus2.i2c_msg.read(self.sensor_port, self.datasize)
        self.bus.i2c_rdwr(write_msg)
        time.sleep(self.measure_interval)
        self.bus.i2c_rdwr(read_msg)
        combined_pre_result = read_msg.buf[0]
        for i in range(1, self.datasize):
            combined_pre_result += read_msg.buf[i]
        result = int.from_bytes(combined_pre_result,'big')
        return result
    
    def return_infor(self):
        print("This device is ", self.id)
        print("Locate at ", self.sensor_port, "Operate in ", self.sensor_mode) 
        


    

