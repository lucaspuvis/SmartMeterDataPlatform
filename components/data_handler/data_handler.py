import paho.mqtt.client as mqtt
import time, sys, os

'''
This script has the responsibility of grabbing the data via MQTT
from the smartmeters, decoding them and storing them in a database.
Uses docker-compose to store variables in ENV
'''

def get_env_vars():
    '''
    Grabs the necessary environment vars set up in the docker-compose file

    Returns:
    dict: A dictionary with address, port, user, pass and topic.
    '''
    env = {
        "address": os.getenv("ADDRESS"),
        "port": os.getenv("PORT"),
        "user": os.getenv("USER"),
        "pass": os.getenv("PASSWORD"),
        "topic": os.getenv("TOPIC")
    }
    return env


def on_connect(client, userdata, flags, rc):
    '''
    Boilerplate code executed when a connection
    is established or the connection failed.
    '''
    if rc == 0:
        print("Connected")
        global connected
        connected = True
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    # TODO
    '''
    Handles decoding messages and storing them in a database.
    '''
    print("Message: {}".format(message.payload))


def connect(env):
    connected = False
    client = mqtt.Client("Python")
    client.username_pw_set(env["user"], password=env["pass"])

    # Defines what methods will happen when connecting to the broker and when receiving messages.
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(env["address"], port=env["port"])
    client.loop_start()

    # Wait for connection
    while connected != True:
        print("Connecting...")
        time.sleep(1)

    client.subscribe(env["topic"])

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    env = get_env_vars()
    connect(env)

