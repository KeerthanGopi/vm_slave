import paho.mqtt.client as mqtt
from multiprocessing import Queue

def setup(queue):
    global pinged
    client = mqtt.Client("ss")
    client.connect("127.0.0.1", 1883)
    pinged = False
    main(client, queue, pinged)


def main(client, queue, pinged):
    print(queue.empty())
    if not queue.empty():
        pinged = queue.get()
    if not pinged:
        recieve = input("Enter: ")
    else:
        recieve = ""
    if recieve != "":
        client.publish("Ping-Pong", (recieve + ".slave"))
        if recieve != "ping":
            pinged = False
        else:
            pinged = True
    main(client, queue, pinged)
