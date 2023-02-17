import paho.mqtt.client as mqtt
from time import time
import threading
import json



download_completed_msg =  {'downloaded': 1}



class communication:

    def __init__(self):
        self.decoded_msg = {}
        self.event = threading.Event()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected: {mqtt.error_string(rc)}")
        client.subscribe("music/name")
        client.subscribe("music/play")
        client.subscribe("rock")

    def on_message(self, client, userdata, msg):
        print(f'{msg.topic}: {msg.payload}')
        msg_key = msg.topic
        msg_val = msg.payload.decode('ascii')
        self.decoded_msg[msg_key] = msg_val
        print("received decoded data ", self.decoded_msg)
        self.event.set()

    def start_communication(self, send_msg_from_sensor, receive_message, downloadflag, lock_send_from_sensor, lock_receive ):
        try:
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            client.tls_set(ca_certs='./Communication/ca.crt', certfile='./Communication/pi.crt', keyfile='./Communication/pi.key')
            client.username_pw_set('pi', '123456')
            client.connect("goldcrest101.duckdns.org", 8883) 
            lastMessage = time()
            message = ''
            while True:   
                client.loop()
                if time() - lastMessage > 3:
                    # print("about to publish")
                    
                    with lock_send_from_sensor:
                        message_sensor = send_msg_from_sensor 
                        message_sensor = json.dumps(message_sensor)

                    if(downloadflag.is_set()):
                        message_acturator = json.dumps(download_completed_msg)
                        MSG_INFO = client.publish("music/downloaded", payload = message_acturator)
                        print(f"Publish info: {mqtt.error_string(MSG_INFO.rc)}")
                        downloadflag.clear()
                        print("complete sending")

                    #send message from sensor 
                    MSG_INFO = client.publish("sensor", payload =message_sensor)
                    print(f"Publish info: {mqtt.error_string(MSG_INFO.rc)}")
                    lastMessage = time()
                    # print("published heihei")
                    if(self.event.is_set()):
                        with lock_receive:
                            receive_message.update(self.decoded_msg)
                            print("Communication ", receive_message)
                            self.decoded_msg = {}
                            self.event.clear()
        except:
            print("Connection failed")

