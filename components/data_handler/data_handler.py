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
    # env = {
    #     "address": os.getenv("ADDRESS"),
    #     "port": os.getenv("PORT"),
    #     "user": os.getenv("USER"),
    #     "pass": os.getenv("PASSWORD"),
    #     "topic": os.getenv("TOPIC"),
    #     "dbhost": os.getenv("DBHOST"),
    #     "dbport": os.getenv("DBPORT")
    # }

    env = {
        "address": "influx.itu.dk",
        "port": 9001,
        "user": "smartreader",
        "pass": "4mp3r3h0ur",
        "topic": "IoT2020sec/meters",
        "dbhost": "influxdb",
        "dbport": "8086"
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
    # TODO
    '''
    Handles decoding messages and storing them in a database.
    '''
    c = BitArray(base64.b64decode(message.payload))

    identifier = 0
    timestamp = 0
    reading = 0
    # Fake data
    if c[0] == 1:
        identifier = c[1:7].int
        print("Identifier: {}".format(identifier))
        timestamp = c[8:40].int
        print("Timestamp: {}".format(datetime.datetime.utcfromtimestamp(timestamp)))
        reading = c[41:].int
        print("Reading: {}".format(reading))
    # Real data
    else:
        identifier = c[1:7].int
        print("Identifier: {}".format(identifier))
        timestamp = c[8:40].int
        print("Timestamp: {}".format(timestamp))
        reading = c[41:].int
        print("Reading: {}".format(reading))

    json_body = [
        {
            "measurement": "meterEvent",
            "tags": {
                "meterId": identifier
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
    dbclient.create_database('smartmeters')
    dbclient.switch_database('smartmeters')
    connect(env)

