import paho.mqtt.client as mqtt
import time, sys, os
import base64
import datetime
from influxdb import InfluxDBClient
from bitstring import BitArray

'''
This script has the responsibility of grabbing the data via MQTT
from the smartmeters, decoding them and storing them in a database.
Uses docker-compose to store variables in ENV
'''

global connected
global dbclient

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
        "topic": os.getenv("TOPIC"),
        "dbhost": os.getenv("DBHOST"),
        "dbport": os.getenv("DBPORT")
    }

    return env


def on_connect(client, userdata, flags, rc):
    '''
    Boilerplate code executed when a connection
    is established or the connection failed.
    '''
    if rc == 0:
        print("Connected")
        connected = True
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    '''
    Handles decoding messages and storing them in a database.
    '''
    c = BitArray(base64.b64decode(message.payload))

    fakeData = c[0] # 1 bit
    meterId = c[1:8].int # 7 bit
    timestamp = c[8:40].int # 32 bit
    reading = c[40:].int # 16 bit
    weekday = datetime.datetime.fromtimestamp(timestamp).weekday()

    json_body = [
        {
            "measurement": "meterEvent",
            "tags": {
                "meterId": meterId,
                "fakeData": fakeData,
                "weekday": weekday
            },
            "time": datetime.datetime.utcfromtimestamp(timestamp),
            "fields": {
                "reading": reading
            }
        }
    ]

    dbclient.write_points(json_body)



def connect(env):
    connected = False
    client = mqtt.Client(transport="websockets")
    client.username_pw_set(env["user"], password=env["pass"])
    client.ws_set_options(path="mq")

    # Defines what methods will happen when connecting to the broker and when receiving messages.
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(env["address"], port=int(env["port"]))
    client.loop_start()

    client.subscribe(env["topic"])

    try:
        while True: # do whatever epic shit we need for project smil :)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
        print(dbclient.query("select reading from meterEvent"))
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    env = get_env_vars()
    dbclient = InfluxDBClient(host=env["dbhost"], port=int(env["dbport"]))
    dbclient.create_database('smartmeter')
    dbclient.switch_database('smartmeter')
    connect(env)

