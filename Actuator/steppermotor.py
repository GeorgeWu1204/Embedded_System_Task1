from gpiozero import OutputDevice as stepper
from time import sleep
import threading

# Define the step sequence for clockwise rotation
seq_cw = [[1,0,0,1], [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1]]

# Define the step sequence for counterclockwise rotation
seq_ccw = [[0,0,0,1], [0,0,1,1], [0,0,1,0], [0,1,1,0], [0,1,0,0], [1,1,0,0], [1,0,0,0], [1,0,0,1]]

delay = 0.0001

class stepper_motor:
    def __init__(self, direction_port, step_port, ms_1, ms_2, ms_0):
        self.dir_pin = stepper(direction_port)
        self.step_pin = stepper(step_port)
        self.stop_event = threading.Event()
        self.stop_event.set()
        self.swing_thread = None
        self.ms0 = stepper(ms_0)
        self.ms1 = stepper(ms_1)
        self.ms2 = stepper(ms_2)
        
        
    def swing(self):
        sleep(5)
        self.ms2.on()
        self.ms1.on()
        self.ms0.on()
        i = 0
        self.dir_pin.value = 1
        while self.stop_event.is_set() == False:
            if i == 0 :
                for g in range(80):
                    for halfstep in range(8):
                        for pin in range(4):
                            self.step_pin.value = seq_cw[halfstep][pin]
                            sleep(delay)
                sleep (1)

            if i % 100 == 0:
                print("reach position")
                print("test if it could keep in this position")
                sleep(0.5)
                self.dir_pin.value = 1 - self.dir_pin.value
                seq = seq_ccw if self.dir_pin.value == 0 else seq_cw
            for halfstep in range(8):
                for pin in range(4):
                    self.step_pin.value = seq[halfstep][pin]
                    sleep(delay)
            i += 1
            
        print("complete swing")
        self.stop_event.clear()
    def start_swing(self):
        print("ready to start the motor, please connect the motor controller to the power source")
        self.stop_event.clear()
        self.swing_thread = threading.Thread(target=self.swing)
        self.swing_thread.start()
    def end_swing(self):
        self.stop_event.set()
        try:
            self.swing_thread.join()
            print("success killed")
        except:
            print("no swing thread in process.")

if __name__ == "__main__":
    MyStepper = stepper_motor(21, 20, 1, 12)
    print("ready to start")
    MyStepper.start_swing()
    sleep(15)
    print("ready to end")
    MyStepper.end_swing()



