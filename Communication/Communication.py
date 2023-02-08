import paho.mqtt.client as mqtt
from time import time
import json



clear_completed_msg =  {'music/downloaded': 0}
clear_completed_msg = json.dumps(clear_completed_msg)


class communication:

    def __init__(self):
        self.decoded_msg = {}

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected: {mqtt.error_string(rc)}")
        client.subscribe("music/#")
        client.subscribe("rock")

    def on_message(self, client, userdata, msg):
        print(f'{msg.topic}: {msg.payload}')
        msg_key = msg.topic
        msg_val = msg.payload.decode('ascii')
        self.decoded_msg[msg_key] = msg_val
        print("received decoded data ", self.decoded_msg)

    def start_communication(self, send_msg_from_sensor, send_msg_from_acturator, receive_msg, lock_send_from_sensor, lock_receive, lock_send_from_acturator):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.tls_set(ca_certs='./Communication/ca.crt', certfile='./Communication/pi.crt', keyfile='./Communication/pi.key')
        client.username_pw_set('pi', '123456')
        client.connect("goldcrest101.duckdns.org", 8883) 
        lastMessage = time()
        message = ''
        while(1):   
            client.loop()
            if time() - lastMessage > 10:
                # print("about to publish")
                
                with lock_send_from_sensor:
                    message_sensor = send_msg_from_sensor 
                
                #detect message from the acturator (msg about download music)
             
                with lock_send_from_acturator:
                    message_acturator = send_msg_from_acturator

                # if(message_acturator != clear_completed_msg):
                #     MSG_INFO = client.publish("sensor", payload =message_acturator)
                #     print(f"Publish info: {mqtt.error_string(MSG_INFO.rc)}")
                    
                #     # time.sleep(5)
                #     with lock_send_from_acturator:
                #         send_msg_from_acturator = clear_completed_msg
                #     print("Sending completed download music")

                #send message from sensor 
                #for testing
                # MSG_INFO = client.publish("music/downloaded", payload =1)
                # #MSG_INFO = client.publish("sensor", payload =message_sensor)
                # print(f"Publish info: {mqtt.error_string(MSG_INFO.rc)}")
                lastMessage = time()
                # print("published heihei")
                with lock_receive:
                    receive_msg = self.decoded_msg
                    # print(receive_msg)


