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

'''
 SensorObject with default data in case of empty or invalid response.
 Note that last_updated-values of all sorts are a Unix timestamp and might 
 need some adjusting to display correct values.
'''


class SensorObject():
    sensor_id: str
    client_name: str
    name: str
    last_updated: datetime
    ignored: bool
    editable: bool
    temp_value: float
    temp_last_updated: datetime
    temp_max_value: float
    temp_max_time: datetime
    temp_min_value: float
    temp_min_time: datetime
    humidity_value: float
    humidity_last_updated: datetime
    humidity_max_value: float
    humidity_max_time: datetime
    humidity_min_value: float
    humidity_min_time: datetime
    timezone_offset: int


''' 
 Function for collecting a list of sensors connected to your Telldus account and fetch latest available information from them.
 This function returns a list of SensorObjects to the user.
'''

# TODO: Add error handling and clean up code


def fetch_sensor_list(return_raw=False, return_list=False):
    telldus_url = f'{base_url}/sensors/list'
    telldus_call = telldus_user.get(telldus_url)
    result = json.loads(telldus_call.text)
    sensor_list = []
    if (return_list):
        for res in result['sensor']:
            sensor_list.append({
                'sensor_id': res['id'],
                'sensor_name': res['name'],
                'sensor_lastupdate': res['lastUpdated'],
                'sensor_model': res['model']
            })
    else:
        for res in result['sensor']:
            if (return_raw):
                sensor_list.append(fetch_sensor_data(res['id'], True))
            else:
                sensor_list.append(fetch_sensor_data(res['id']))

    return sensor_list


'''
 Function for collecting the latest available information from a specified Telldus sensor ID.
 Returns a SensorObject containing the information to the user
'''

# TODO: Add error handling and clean up code


def fetch_sensor_data(sensor_id, return_raw=False):
    telldus_url = f'{base_url}/sensor/info?id={sensor_id}'

    telldus_call = telldus_user.get(telldus_url)

    json_data = json.loads(telldus_call.text)

    if json_data:
        result = SensorObject()
        result.sensor_id = json_data['id']
        result.name = json_data['name']
        result.client_name = json_data['clientName']
        result.last_updated = json_data['lastUpdated'] if return_raw else datetime.fromtimestamp(
            int(json_data['lastUpdated']))
        try:
            if json_data['data'][0]['name'] == 'temp':
                # Handle temperature values
                result.temp_value = float(json_data['data'][0]['value'])
                result.temp_max_value = float(json_data['data'][0]['max'])
                result.temp_min_value = float(json_data['data'][0]['min'])
                # Handle datetime values
                if (return_raw):
                    result.temp_last_updated = json_data['data'][0]['lastUpdated']
                    result.temp_max_time = json_data['data'][0]['maxTime']
                    result.temp_min_time = json_data['data'][0]['minTime']
                else:
                    result.templast_updated = datetime.fromtimestamp(
                        int(json_data['data'][0]['lastUpdated']))
                    result.temp_max_time = datetime.fromtimestamp(
                        int(json_data['data'][0]['maxTime']))
                    result.temp_min_time = datetime.fromtimestamp(
                        int(json_data['data'][0]['minTime']))
        except Exception:
            pass
        try:
            if json_data['data'][1]['name'] == 'humidity':
                # Handle humidity values
                result.humidity_value = int(json_data['data'][1]['value'])
                result.humidity_max_value = int(json_data['data'][1]['max'])
                result.humidity_min_value = int(json_data['data'][1]['min'])
                # Handle datetime values
                if (return_raw):
                    result.humidity_last_updated = json_data['data'][1]['lastUpdated']
                    result.humidity_max_time = json_data['data'][1]['maxTime']
                    result.humidity_min_time = json_data['data'][1]['minTime']
                else:
                    result.humidity_last_updated = datetime.fromtimestamp(
                        int(json_data['data'][1]['lastUpdated']))
                    result.humidity_max_time = datetime.fromtimestamp(
                        int(json_data['data'][1]['maxTime']))
                    result.humidity_min_time = datetime.fromtimestamp(
                        int(json_data['data'][1]['minTime']))
        except Exception:
            pass
        result.timezone_offset = json_data['timezoneoffset']

    else:
        result = SensorObject()

    return result


""" 
 A function for fetching sensor history stored at Telldus 
"""


def fetch_sensor_history(sensor_id):
    try:
        telldus_url = f'{base_url}/sensor/history?id={sensor_id}'
        telldus_call = telldus_user.get(telldus_url)
        return json.loads(telldus_call.text)
    except Exception:
        return {'error': 'Error while fetching data.'}
