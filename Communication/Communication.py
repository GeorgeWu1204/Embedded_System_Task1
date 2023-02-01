import paho.mqtt.client as mqtt
from time import time

class communication:

    def __init__(self):
        self.decoded_msg = {}

    def on_connect(client, userdata, flags, rc):
        print(f"Connected: {mqtt.error_string(rc)}")
        client.subscribe("music")
        client.subscribe("rock")

    def on_message(self, client, userdata, msg):
        print(f'{msg.topic}: {msg.payload}')
        self.decoded_msg = {msg.topic.decode('ascii'), msg.payload.decode('ascii')}

    def start_communication(self, send_msg, receive_msg, lock_send, lock_receive):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.tls_set(ca_certs='./Communication/ca.crt', certfile='./Communication/pi.crt', keyfile='./Communication/pi.key')
        client.username_pw_set('pi', '123456')
        client.connect("goldcrest101.duckdns.org", 8883) 
        lastMessage = time()
        message = ''
        while(1):   
            client.loop()
            if time() - lastMessage > 3:
                print("about to publish")
                lock_send.acquire()
                message = send_msg 
                lock_send.release()
                # MSG_INFO = client.publish('sensor/data', payload="hihihi")
                MSG_INFO = client.publish("sensor", payload =message)
                print(f"Publish info: {mqtt.error_string(MSG_INFO.rc)}")
                lastMessage = time()
                print("published heihei")
                lock_receive.acquire()
                receive_msg = self.decoded_msg
                lock_receive.release()


