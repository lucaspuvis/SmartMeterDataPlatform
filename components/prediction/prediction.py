from flask import Flask
from influxdb import InfluxDBClient
import os




def get_env_vars():
    '''
    Grabs the necessary environment vars set up in the docker-compose file

    Returns:
    dict: A dictionary with address, port, user, pass and topic.
    '''
    env = {
        "dbhost": os.getenv("DBHOST"),
        "dbport": os.getenv("DBPORT")
    }

    return env

app = Flask(__name__)
env = get_env_vars()
dbclient = InfluxDBClient(host=env["dbhost"], port=int(env["dbport"]))
dbclient.switch_database("pyexample")


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/prediction/<day>', methods=['GET'])
def index(day):
    '''
    Predicts power consumption for a specified weekday

    Parameters:
    day (string): The weekday to predict

    Returns:
    int: the power consumption predicted
    '''

    test = dbclient.query('SELECT "reading" FROM "smartmeter"."autogen"."meterEvent"')

    return "Return: {}".format(test)


app.run(host='0.0.0.0', debug=True)