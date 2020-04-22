from flask import Flask
from influxdb import InfluxDBClient
import datetime, os




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
dbclient.switch_database("smartmeter")


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/prediction/<day>/<meterId>', methods=['GET'])
def index(day, meterId):
    '''
    Predicts power consumption for a specified weekday

    Parameters:
    day (string): The weekday to predict

    Returns:
    int: the power consumption predicted
    '''

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if day not in weekdays:
        return "Please use either monday, tuesday, wednesday, thursday, friday, saturday or sunday as parameter. It is CASE SENSETIVE"
    else:
        query = "SELECT mean(reading) FROM meterEvent WHERE (fakeData = \'True\') AND (weekday = \'{}\' AND (meterId = \'{}\'))".format(weekdays.index(day), meterId)
        response = dbclient.query(query)

        return "{}".format(response)


app.run(host='0.0.0.0', debug=True)