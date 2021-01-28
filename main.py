from fastapi import FastAPI
import os
from controller.caller import fetch_sensor_data, fetch_sensor_history, fetch_sensor_list

# Initialize FastAPI
app = FastAPI()


""" Dummy route for root path """


@app.get("/")
def read_root():
    return fetch_sensor_list(return_raw=True, return_list=True)


@app.get("/sensors")
def get_sensors():
    return fetch_sensor_list(return_raw=True)


@app.get("/sensor/info/{sensor_id}")
def get_sensor_info(sensor_id: int):
    return {fetch_sensor_data(sensor_id, return_raw=True)}


@app.get("/sensor/history/{sensor_id}")
def get_sensor_history(sensor_id: int):
    return {
        'sensor_id': sensor_id,
        'result': fetch_sensor_history(sensor_id)
    }
