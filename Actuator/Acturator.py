from Actuator.servo import MyServo
from Actuator.Speaker import speaker
import json

completed_download_msg = {'music/downloaded': 1}
completed_send_msg = json.dumps(completed_download_msg)


class acturator:
    def __init__(self, id, mode):
        # self.Sensors = sensor_group(self.name)
        self.Speaker = speaker()
        #self.mySer = MyServo(13,50) 
        # self.speaker = None 
        self.received_message = ''
        self.playing_music = False
        self.musicname = '夜的第七章'

    def controlActurator(self, received_message, send_message, lock_received, lock_sent):
        while True:
            with lock_received:
                self.received_message = received_message
        
            if 'rock' in self.received_message:
                if self.received_message["rock"]:
                #self.mySer.set_angle(8,0.1)
                    print("rock called start servo ")

            if 'music/play' in self.received_message:
                print("inside music/play")
                if self.received_message['music/play'] == "1" and self.playing_music == False:
                    print("received play")
                    self.Speaker.playSong(songName= self.musicname)
                    self.playing_music = True
            else:
                
                if self.playing_music:
                    print("playing ,about ot kill")
                    self.Speaker.kill()
                    self.playing_music = False

            if 'music/name' in self.received_message:
                self.musicname = self.received_message["music/name"]
                print("Check In Local", self.musicname)
                if self.Speaker.checkInLocal(self.musicname):
                    with lock_sent:
                        send_message = completed_send_msg
                    with lock_received:
                        received_message.pop(['music/name'])

                        

                
            
        




        

            
