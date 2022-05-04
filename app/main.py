from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.caller import fetch_sensor_data, fetch_sensor_history, fetch_sensor_list

# Initialize FastAPI
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root will show a listing of sensors connected to supplied API key
# TODO: Add error handling
@app.get("/")
async def read_root():
    return fetch_sensor_list(return_raw=True, return_list=True)


# /sensor endpoint will show sensor listing with details
# TODO: Add error handling
@app.get("/sensors")
async def get_sensors():
    return fetch_sensor_list(return_raw=True)


# /sensor/info/{sensor_id} will show specific sensor details
# TODO: Add error handling
@app.get("/sensor/info/{sensor_id}")
async def get_sensor_info(sensor_id: int):
    return {fetch_sensor_data(sensor_id, return_raw=True)}


# /sensor/history/{sensor_id} will show specific sensor history
# TODO: Add error handling
@app.get("/sensor/history/{sensor_id}")
async def get_sensor_history(sensor_id: int):
    return {
        'sensor_id': sensor_id,
        'result': fetch_sensor_history(sensor_id)
    }
