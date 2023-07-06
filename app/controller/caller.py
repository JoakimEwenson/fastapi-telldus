import concurrent.futures
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

# Load .env file
load_dotenv()

# Set up OAuth against Telldus Live API
telldus_oauth1_session = os.environ.get('TELLDUS_OAUTH1_SESSION')
telldus_client_secret = os.environ.get('TELLDUS_CLIENT_SECRET')
telldus_resource_owner_key = os.environ.get('TELLDUS_RESOURCE_OWNER_KEY')
telldus_resource_owner_secret = os.environ.get('TELLDUS_RESOURCE_OWNER_SECRET')

telldus_user = OAuth1Session(telldus_oauth1_session,
                             client_secret=telldus_client_secret,
                             resource_owner_key=telldus_resource_owner_key,
                             resource_owner_secret=telldus_resource_owner_secret)


# Base URL for the API
base_url = "https://api.telldus.com/json"


class SensorObject():
    '''
    SensorObject with default data in case of empty or invalid response.
    Note that lastUpdated-values of all sorts are a Unix timestamp and might
    need some adjusting to display correct values.
    '''
    id: int
    clientName: str
    name: str
    lastUpdated: datetime
    ignored: bool
    editable: bool
    tempValue: float
    tempLastUpdated: datetime
    tempMaxValue: float
    tempMaxTime: datetime
    tempMinValue: float
    tempMinTime: datetime
    humidityValue: float
    humidityLastUpdated: datetime
    humidityMaxValue: float
    humidityMaxTime: datetime
    humidityMinValue: float
    humidityMinTime: datetime
    timezoneOffset: int


def fetch_sensor_list(return_raw=False, return_list=False):
    ''' 
    Function for collecting a list of sensors connected to your Telldus account and fetch latest available information from them.
    This function returns a list of SensorObjects to the user.
    '''

    # TODO: Add error handling and clean up code
    telldus_url = f'{base_url}/sensors/list'
    telldus_call = telldus_user.get(telldus_url)
    result = json.loads(telldus_call.text)
    sensor_list = []
    if (return_list):
        for res in result['sensor']:
            sensor_list.append({
                'id': res['id'],
                'name': res['name'],
                'lastupdate': res['lastUpdated'],
                'model': res['model']
            })
    else:
        # Create empty array for storing sensor IDs
        sensors = []
        # Iterate result and append array with response
        for res in result['sensor']:
            sensors.append(res['id'])
            # Old method
            # if (return_raw):
            #     sensor_list.append(fetch_sensor_data(res['id'], True))
            # else:
            #     sensor_list.append(fetch_sensor_data(res['id']))
        # Use concurrent to fetch sensor data for all sensors in list
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for item in executor.map(fetch_sensor_data, sensors):
                sensor_list.append(item)

    return sensor_list


def fetch_sensor_data(sensorId, return_raw=False):
    '''
    Function for collecting the latest available information from a specified Telldus sensor ID.
    Returns a SensorObject containing the information to the user
    '''

    # TODO: Add error handling and clean up code

    telldus_url = f'{base_url}/sensor/info?id={sensorId}'

    telldus_call = telldus_user.get(telldus_url)

    json_data = json.loads(telldus_call.text)

    if json_data and json_data['name'] != None:
        result = SensorObject()
        result.id = int(json_data['id'])
        result.name = json_data['name']
        result.clientName = json_data['clientName']
        result.lastUpdated = json_data['lastUpdated'] if return_raw else datetime.fromtimestamp(
            int(json_data['lastUpdated']))
        try:
            if json_data['data'][0]['name'] == 'temp':
                # Handle temperature values
                result.tempValue = float(json_data['data'][0]['value'])
                result.tempMaxValue = float(json_data['data'][0]['max'])
                result.tempMinValue = float(json_data['data'][0]['min'])
                # Handle datetime values
                if (return_raw):
                    result.tempLastUpdated = json_data['data'][0]['lastUpdated']
                    result.tempMaxTime = json_data['data'][0]['maxTime']
                    result.tempMinTime = json_data['data'][0]['minTime']
                else:
                    result.templastUpdated = datetime.fromtimestamp(
                        int(json_data['data'][0]['lastUpdated']))
                    result.tempMaxTime = datetime.fromtimestamp(
                        int(json_data['data'][0]['maxTime']))
                    result.tempMinTime = datetime.fromtimestamp(
                        int(json_data['data'][0]['minTime']))
        except Exception:
            pass
        try:
            if json_data['data'][1]['name'] == 'humidity':
                # Handle humidity values
                result.humidityValue = int(json_data['data'][1]['value'])
                result.humidityMaxValue = int(json_data['data'][1]['max'])
                result.humidityMinValue = int(json_data['data'][1]['min'])
                # Handle datetime values
                if (return_raw):
                    result.humidityLastUpdated = json_data['data'][1]['lastUpdated']
                    result.humidityMaxTime = json_data['data'][1]['maxTime']
                    result.humidityMinTime = json_data['data'][1]['minTime']
                else:
                    result.humidityLastUpdated = datetime.fromtimestamp(
                        int(json_data['data'][1]['lastUpdated']))
                    result.humidityMaxTime = datetime.fromtimestamp(
                        int(json_data['data'][1]['maxTime']))
                    result.humidityMinTime = datetime.fromtimestamp(
                        int(json_data['data'][1]['minTime']))
        except Exception:
            pass
        result.timezoneOffset = json_data['timezoneoffset']

        return result
    # Default empty
    return SensorObject()


def fetch_sensor_history(sensorId):
    """ 
    A function for fetching sensor history stored at Telldus 
    """
    try:
        telldus_url = f'{base_url}/sensor/history?id={sensorId}'
        telldus_call = telldus_user.get(telldus_url)
        return json.loads(telldus_call.text)
    except Exception:
        return {'error': 'Error while fetching data.'}
