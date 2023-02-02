import paho.mqtt.client as mqtt
from time import time
import random

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected: {mqtt.error_string(rc)}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("sensor")
    client.subscribe("music")
    client.subscribe("rock")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f'{msg.topic}: {msg.payload}')


def generate_fake_data():
    temperature = random.randint(20,28)
    humidity = random.randint(10,30)
    heart_rate = random.randint(55, 120)
    return temperature, humidity, heart_rate


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs='./cert/ca.crt', certfile='./cert/mosquitto.crt', keyfile='./cert/mosquitto.key')
client.username_pw_set('cathy', '123456')

client.connect("goldcrest101.duckdns.org", 8883) # 60 is ping interval

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
lastMessage = time()
while(1):   
    client.loop()
    if time() - lastMessage > 3:
        print("about to publish")
        message = '{"id":"1", "data":{"onbed":false, "crying":true, "awake": true, "heart_rate":62, "temperature":36, "humidity":25}}'
        MSG_INFO = client.publish('sensor', payload=message)
        print(f"Publish info: {mqtt.error_string(MSG_INFO.rc)}")
        lastMessage = time()
        print("published heihei")
