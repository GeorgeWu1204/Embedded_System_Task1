from Actuator.servo import MyServo
from Actuator.Speaker import speaker

class acturator:
    def __init__(self, id, mode):
        
        # self.Sensors = sensor_group(self.name)
        # self.Speaker = speaker()
        self.mySer = MyServo(13,50) 
        self.speaker = None 
        self.received_message = ''

    def controlActurator(self, received_message, lock):
        with lock:
            self.received_message = received_message
    
        if self.received_message["rock"]:
            #self.mySer.set_angle(8,0.1)
            print("rock called start servo ")
        if self.received_message["music"]:
            print("music called start speaker")
            self.speaker.playSong("飘移")




        

            
