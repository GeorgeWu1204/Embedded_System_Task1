from Actuator.servo import MyServo
from Actuator.Speaker import speaker

# completed_download_msg = {'downloaded': 1}


class acturator:
    def __init__(self, id, mode):
        # self.Sensors = sensor_group(self.name)
        self.Speaker = speaker()
        #self.mySer = MyServo(13,50) 
        # self.speaker = None 
        self.received_message = ''
        self.playing_music = False
        self.musicname = '夜的第七章'

    def controlActurator(self, received_message, lock_received, downloaded):
        while True:
            with lock_received:
                self.received_message = received_message
        
            if 'rock' in self.received_message:
                if self.received_message["rock"]:
                #self.mySer.set_angle(8,0.1)
                    print("rock called start servo ")

            if 'music/play' in self.received_message:
                # print("inside music/play")
                if self.received_message['music/play'] == "play" and self.playing_music == False:
                    print("received play")
                    self.Speaker.playSong(songName=self.musicname)
                    self.playing_music = True
                    
                elif self.received_message['music/play'] == "stop" and self.playing_music == True:
                    print("playing ,about ot kill")
                    self.Speaker.kill()
                    self.playing_music = False

            if 'music/name' in self.received_message:
                self.musicname = self.received_message["music/name"]
                print("Check In Local", self.musicname)
                if self.Speaker.checkInLocal(self.musicname):
                    downloaded.set()
                    # with lock_sent:
                    #     send_message.update(completed_download_msg)
                    with lock_received:
                        received_message.pop('music/name')

                        

                
            
        




        

            
