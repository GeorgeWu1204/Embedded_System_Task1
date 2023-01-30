import qwiic_max3010x
import time
import sys

def millis():
	return int(round(time.time() * 1000))

class max30101(qwiic_max3010x.QwiicMax3010x):
    # def __init__(self, address=None, i2c_driver=None):
    #     super().__init__(address, i2c_driver)
    def Check_device_connection(self):
        if self.begin() == False:
            print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
                file=sys.stderr)
            return False
        else:
            print("The Qwiic MAX3010x is connected.")
            return True

        
    def take_heartbeat_rate(self, sample_num = None):
        print("Place your index finger on the sensor with steady pressure.")
        if self.setup() == False:
            print("Device setup failure. Please check your connection", \
                file=sys.stderr)
            return
        else:
            print("Setup complete.")
        self.setPulseAmplitudeRed(0x0A) # Turn Red LED to low to indicate sensor is running
        self.setPulseAmplitudeGreen(0) # Turn off Green LED
        RATE_SIZE = 4 # Increase this for more averaging. 4 is good.
        rates = list(range(RATE_SIZE)) # list of heart rates
        rateSpot = 0
        lastBeat = 0 # Time at which the last beat occurred
        beatsPerMinute = 0.00
        beatAvg = 0
        samplesTaken = 0 # Counter for calculating the Hz or read rate
        startTime = millis() # Used to calculate measurement rate
        while sample_num == None or (samplesTaken < sample_num and sample_num != None):
                    
            irValue = self.getIR()
            samplesTaken += 1
            if self.checkForBeat(irValue) == True:
                # We sensed a beat!
                print('BEAT')
                delta = ( millis() - lastBeat )
                lastBeat = millis()	
        
                beatsPerMinute = 60 / (delta / 1000.0)
                beatsPerMinute = round(beatsPerMinute,1)
        
                if beatsPerMinute < 255 and beatsPerMinute > 20:
                    rateSpot += 1
                    rateSpot %= RATE_SIZE # Wrap variable
                    rates[rateSpot] = beatsPerMinute # Store this reading in the array

                    # Take average of readings
                    beatAvg = 0
                    for x in range(0, RATE_SIZE):
                        beatAvg += rates[x]
                    beatAvg /= RATE_SIZE
                    beatAvg = round(beatAvg)
            
            Hz = round(float(samplesTaken) / ( ( millis() - startTime ) / 1000.0 ) , 2)
            if (samplesTaken % 200 ) == 0:
            
                print(\
                    'IR=', irValue , ' \t',\
                                'BPM=', beatsPerMinute , '\t',\
                                                                                    #'DCE', getDCE() , '\t',\
                                'Avg=', beatAvg , '\t',\
                    'Hz=', Hz, \
                    )
        return [beatsPerMinute, beatAvg]

# if __name__ == '__main__':
#     try:
#         runExample()
#     except (KeyboardInterrupt, SystemExit) as exErr:
#         print("\nEnding Example 5")
#         sys.exit(0)


