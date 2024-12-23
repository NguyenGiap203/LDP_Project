import sys
import time
import random
from Adafruit_IO import MQTTClient
from ai import *

AIO_FEED_IDs = []
AIO_USERNAME = ""
AIO_KEY = ""


def connected(client):
    print("Ket noi thanh cong...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)


def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong ...")


def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)


def message(client, feed_id, payload):
    print("Nhan du lieu: " + payload + "feed_id:" + feed_id)


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

if __name__ == "__main__":
    counter_ai = 3
    while True:

        counter_ai = counter_ai - 1
        if counter_ai <= 0:
            counter_ai = 3
            ai_result = image_detector()
            print("AI Output: ", ai_result)
            client.publish("ai", ai_result)

        time.sleep(1)
        pass

