#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from Sensors.hx711Pack.hx711 import HX711  # import the class HX711
import time
import queue

class hx711Interface:
    def __init__(self, dout=5, sck_pin=6):
        GPIO.setmode(GPIO.BCM)
        self.dout_pin = dout
        self.pd_sck_pin = sck_pin
        self.hx = HX711(dout_pin=self.dout_pin, pd_sck_pin=self.pd_sck_pin)
        self.event = None
        
    def setup(self):
        try:
            # measure tare and save the value as offset for current channel
            # and gain selected. That means channel A and gain 128
            err = self.hx.zero()
            # check if successful
            if err:
                raise ValueError('Tare is unsuccessful.')

            reading = self.hx.get_raw_data_mean()
            if reading:  # always check if you get correct value or only False
                # now the value is close to 0
                print('Data subtracted by offset but still not converted to units:',
                    reading)
            else:
                print('invalid data', reading)

            # In order to calculate the conversion ratio to some units, in my case I want grams,
            # you must have known weight.
            input('Put known weight on the scale and then press Enter')
            reading = self.hx.get_data_mean()
            if reading:
                print('Mean value from HX711 subtracted by offset:', reading)
                known_weight_grams = input(
                    'Write how many grams it was and press Enter: ')
                try:
                    value = float(known_weight_grams)
                    print(value, 'grams')
                except ValueError:
                    print('Expected integer or float and I have got:',
                        known_weight_grams)

                # set scale ratio for particular channel and gain which is
                # used to calculate the conversion to units. Required argument is only
                # scale ratio. Without arguments 'channel' and 'gain_A' it sets
                # the ratio for current channel and gain.
                ratio = reading / value  # calculate the ratio for channel A and gain 128
                self.hx.set_scale_ratio(ratio)  # set ratio for current channel
                print('Ratio is set.')
            else:
                raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)
        except (KeyboardInterrupt, SystemExit):
            print('Bye :)')

        # finally:
        #     GPIO.cleanup()

    def movingAverage(self, queue, reading, result):
        q1 = queue
        sum = 0
        if queue.full():
            for i in range(queue.qsize()):
                sum+=q1.get(i)
            return sum / queue.qsize()
        else:
            queue.put(reading)
            return result 


    def start_detection(self, time_requirement = None, event = None, detection_period = 10):
        current_val = queue.Queue(3)
        avg_val = queue.Queue(10)
        self.event = event

        try:
            # Read data several times and return mean value
            # subtracted by offset and converted by scale ratio to
            # desired units. In my case in grams.
            print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
            input('Press Enter to begin reading')
            print('Current weight on the scale in grams is: ')
            
            timer = 0
            short_result = 0
            long_result = 0
            while time_requirement == None or (timer < time_requirement and time_requirement != None):
                weight_val = self.hx.get_weight_mean(20)
                # print(self.hx.get_weight_mean(20), 'g')
                short_result = self.movingAverage(current_val,weight_val, short_result)
                long_result = self.movingAverage(avg_val,weight_val, long_result)
                print("check load, short result", short_result, "long_resl ", long_result)
                if(long_result -5 < short_result and short_result < long_result + 5):
                    self.event.set()
                time.sleep(0.5)
                timer += 1
                


        except (KeyboardInterrupt, SystemExit):
            print('Bye :)')
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    hx = hx711Interface(dout=5,sck_pin=6)
    hx.setup()
    hx.start_detection()