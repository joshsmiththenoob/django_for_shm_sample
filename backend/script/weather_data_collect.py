from dotenv import load_dotenv
from script.api_client.cwa_api_client import CWAAPIClient
import os
import json

if __name__ == "__main__":
    weather_url = os.getenv("CWA_API_WEATHER_DATA_URL")
    rainfall_url = os.getenv("CWA_API_RAINFALL_DATA_URL")
    client = CWAAPIClient()
    station_id_list = ["C0C620", "C0C720", "C0D660"]

    for station_id in station_id_list:
        # get weather station data
        response = client.get_weather_data(weather_url, rainfall_url, station_id)
        print(response)



