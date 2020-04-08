# IoT Assignment 2: Smart Meter Data Platform
This repository contains two microservices for our second Internet of Things assignment, orchestrated as docker images to easily keep them going as services on a remote server. Both services are written in python.
The docker-compose orchestrates these images alongside an influxdb for storing.

## DATA_HANDLER
The data_handler.py microservice handles the receiving and storing of electricity data from various smart meters.
It uses paho mqtt to connect to the broker, and then decodes the string of bytes to readable data. This data is then stored in our influx database.

## ML_PREDICTION
TODO

# Building and running the images
The supplied docker-compose.yml file should handle both of these problems. It is alpha and omega that they're run in such a way that the database is set up before the micro services, so we propose the following command:

docker-compose up -d influxdb && sleep 5 && docker-compose up

This sets up the database, waits 5 seconds and then sets up the microservices.

# Troubleshooting
It is possible that building the two microservice images will fail to build. If the error occurs during a step that requires an internet connection (ie. pip install) and results in an error like "Temporary failure in name resolution", this stackoverflow post has an answer that has worked for us.

https://stackoverflow.com/questions/28668180/cant-install-pip-packages-inside-a-docker-container-with-ubuntu

You simply need to add your own and googles DNS servers to your docker daemons config.