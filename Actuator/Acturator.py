from Actuator.servo import MyServo
from Actuator.Speaker import speaker
from Actuator.steppermotor import stepper_motor

# completed_download_msg = {'downloaded': 1}
SM_direc_port = 21
SM_step_port = 20
SM_ms2 = 12
SM_ms1 = 1
SM_ms0 = 0


class acturator:
    def __init__(self, id, mode):
        # self.Sensors = sensor_group(self.name)
        self.Speaker = speaker()
        self.StepMotor = stepper_motor(SM_direc_port, SM_step_port, SM_ms1, SM_ms2, SM_ms0)
        self.received_message = ''
        self.playing_music = False
        self.swinging = False
        self.musicname = '夜的第七章'

    def controlActurator(self, received_message, lock_received, downloaded, music_on, motor_on):
        while True:
            with lock_received:
                self.received_message = received_message
        
            if 'rock' in self.received_message:
                if self.received_message["rock"] == "play" and self.swinging == False:
                #self.mySer.set_angle(8,0.1)
                    self.StepMotor.start_swing()
                    print("rock called start servo ")
                    self.swinging = True
                    with lock_received:
                        received_message.pop('rock')
                    motor_on.set()
                elif self.received_message["rock"] == "stop" and self.swinging == True:
                    self.StepMotor.end_swing()
                    print("rock stopped")
                    self.swinging = False
                    with lock_received:
                        received_message.pop('rock')
                    motor_on.clear()

            if 'music/play' in self.received_message:
                # print("inside music/play")
                if self.received_message['music/play'] == "play" and self.playing_music == False:
                    print("received play")
                    self.Speaker.playSong(songName=self.musicname)
                    self.playing_music = True
                    with lock_received:
                        received_message.pop('music/play')
                    music_on.set()
                    
                elif self.received_message['music/play'] == "stop" and self.playing_music == True:
                    print("playing ,about ot kill")
                    self.Speaker.kill()
                    self.playing_music = False
                    with lock_received:
                        received_message.pop('music/play')
                    music_on.clear()

            if 'music/name' in self.received_message:
                self.musicname = self.received_message["music/name"]
                print("Check In Local", self.musicname)
                if self.Speaker.checkInLocal(self.musicname):
                    downloaded.set()
                    with lock_received:
                        received_message.pop('music/name')

                        

                
            
        




        

            
