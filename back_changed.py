import paho.mqtt.client as mqtt
from multiprocessing import Queue
from time import sleep

def message(client, userdata, message):
    global undone, pinged, queue
    message_recieved = str(message.payload.decode("utf-8")).split(".")
    client1 = message_recieved[1].lower()
    message1 = message_recieved[0].lower()
    if client1 == "slave":
        if message1 == "ping":
            pinged = True
            queue.put(pinged)
            sleep(0.125)
    elif client1 == "master":
        if pinged == False:
            if message1 == "ping":
                client.publish("Ping-Pong", "pong.slave")
        elif pinged ==  True:
            if message1 == "ping":
                undone += 1
                client.publish("Ping-Pong", "Awaiting Response")
            elif message1 == "pong":
                pinged = False
                for i in range(0, undone):
                    client.publish("Ping-Pong", "pong.slave")
                undone = 0


def setup(Queue):
    global pinged, undone, queue
    queue = Queue
    pinged = False
    undone = 0
    client = mqtt.Client("sr")
    client.connect("127.0.0.1", 1883)
    client.subscribe("Ping-Pong")
    main(client)

def main(client):
    client.on_message = message
    client.loop_forever()

