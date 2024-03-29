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
    #return fetch_sensor_list(return_raw=True, return_list=True)
    return {"info":"Unspecified endpoint"}

# Health check for uptime monitors
@app.get("/healthcheck")
def healthcheck():
    return {"status":"OK"}

# /sensorlist endpoint listing sensors without data
@app.get("/sensorlist")
async def get_sensorlist():
    return fetch_sensor_list(return_raw=True, return_list=True)

# /sensor endpoint will show sensor listing with details
# TODO: Add error handling
@app.get("/sensors")
async def get_sensors():
    return fetch_sensor_list(return_raw=True)


# /sensor/info/{sensorId} will show specific sensor details
# TODO: Add error handling
@app.get("/sensor/info/{sensorId}")
async def get_sensor_info(sensorId: int):
    return {fetch_sensor_data(sensorId, return_raw=True)}


# /sensor/history/{sensorId} will show specific sensor history
# TODO: Add error handling
@app.get("/sensor/history/{sensorId}")
async def get_sensor_history(sensorId: int):
    return {
        'sensorId': sensorId,
        'result': fetch_sensor_history(sensorId)
    }
