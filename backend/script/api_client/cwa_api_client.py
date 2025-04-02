from dotenv import load_dotenv
# from dao.weather_station_dao import WeatherStationDAO
from script.dao.weather_station_dao import WeatherStationDAO
from script.dao.weather_station_data_dao import WeatherStationDataDAO
from script.dao.weather_data_history_dao import WeatherDataHistoryDAO
import os
import requests
import pandas as pd

# Load .env file
load_dotenv()

# CWA(Central Weather Administration) API Client
class CWAAPIClient:

    def __init__(self, url= "", headers= None, data= None):
        self.api_key = os.getenv("CWA_API_KEY")
        self.url = url
        self.weather_station_dao = WeatherStationDAO()
        self.weather_station_data_dao = WeatherStationDataDAO()
        self.weather_data_history_dao = WeatherDataHistoryDAO()

    def __request_weather_station_info(self, longitude, latitude):
        # GraphQL query
        query = f"""query aqi {{
            aqi(longitude: {longitude}, latitude: {latitude}) {{
                station {{ stationId, locationName, latitude, longitude, time {{ obsTime }} }}
            }}
        }}"""
        data = {"query": query}

        headers = {
            "Authorization": self.api_key,  # API 金鑰
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            # Get response
            response = requests.post(self.url, json=data, headers=headers, timeout=10)
            response.raise_for_status()  # raise error if HTTP error
            return response.json() 
        
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def update_station_info(self, longitude, latitude):
        """
        update station info by longitude and latitude
        """
        record = self.__request_weather_station_info(longitude, latitude)
        self.weather_station_dao.insert_new_station_info(record)

        print("save station info successfully")
        
    def __request_weather_data(self, weather_url, rainfall_url, station_id: str):
        """
        request weather and rainfall data by station_id from CWA API O-A0001 and O-A0002
        """

        params = {
        "Authorization": self.api_key,
        "limit": 1,
        "format": "JSON",
        "StationId": station_id
        }
        # 發送 GET 請求
        try:
            weather_response = requests.get(weather_url, params=params)
            rainfall_response = requests.get(rainfall_url, params=params)
            
            if weather_response.status_code == 200 and rainfall_response.status_code == 200:
                data1 = weather_response.json()
                data2 = rainfall_response.json()
                combined_data = {"weather_data": data1, "rainfall_data": data2}
                # print(combined_data)
            else:
                print(f"Error: weather_data {weather_response.status_code}, rainfall_data {rainfall_response.status_code}")

            return combined_data
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    
    def __format_weather_data(self, json: dict):
        """
        Format weather data from CWA API: O-A0001 
        """
        # format record
        record = dict()
         
        weather_json = json["weather_data"]["records"]["Station"][0]
        rainfall_json = json["rainfall_data"]["records"]["Station"][0]

        record["station_id"] = weather_json["StationId"]
        record["time"] = weather_json["ObsTime"]["DateTime"]    
        record["temperature"] = weather_json["WeatherElement"]["AirTemperature"]
        record["wind_speed"] = weather_json["WeatherElement"]["WindSpeed"]
        record["wind_direction"] = weather_json["WeatherElement"]["WindDirection"]
        record["acc_precipitation"] = weather_json["WeatherElement"]["Now"]["Precipitation"]
        record["precipitation"] = rainfall_json["RainfallElement"]["Past1hr"]["Precipitation"]

        return record
    
    def get_weather_data(self, weather_url, rainfall_url, station_id: str):
        response = self.__request_weather_data(weather_url, rainfall_url, station_id)
        record = self.__format_weather_data(response)
        result = self.weather_station_data_dao.insert_weather_data(record)
        # print(result)
        print("save weather data successfully")

        return record
    
    def get_batch_history_weather_data(self, start_time, end_time, station_id: str):
        response = self.__request_history_weather_data(start_time, end_time, station_id)
        record = self.__format_history_weather_data(response)
        result = self.weather_data_history_dao.insert_weather_history_data(record)
        print("save weather data successfully")

        return record    

    def __request_history_weather_data(self, start_time, end_time, station_id: str):
        """
        request weather and rainfall history data by CODis
        """

        url = "https://codis.cwa.gov.tw/api/station?"

        data = {
            "date": "2025-02-16T00:00:00.000+08:00",
            "type": "report_date",
            "stn_ID": station_id,
            "stn_type": "auto_C0", # C0=自動氣象站
            "more": "",
            "start": start_time,
            "end": end_time,
            "item": ""
        }
        # 發送 GET 請求
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200 :
                json = response.json()
                json['station_id'] = station_id

                if json['code'] != 200:
                    print(f"Error: 'code': '{json['code']}', 'message': '{json['message']}'")
                    exit()

            else:
                print(f"Error: weather_data {response.status_code}")

            return json
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def __format_history_weather_data(self, json: dict):
        """
        Format weather data from CODis
        """
        # format record
        record = list()
        print(json)
        weather_json = json['data'][0]['dts']

        for _ in range (0, json['metadata']['count']):
            weather_dict = dict()
            weather_dict["station_id"] = json['station_id']
            weather_dict["time"] = weather_json[_]['DataTime'] 
            weather_dict["temperature"] = weather_json[_]['AirTemperature']['Instantaneous']
            weather_dict["wind_speed"] = weather_json[_]['WindSpeed']['Mean']
            weather_dict["wind_direction"] = weather_json[_]['WindDirection']['Mean']
            weather_dict["precipitation"] = weather_json[_]['Precipitation']['Accumulation']

            record.append(weather_dict) 


        """
        {'DataTime': '2025-01-16T23:00:00', 
        'StationPressure': {'Instantaneous': 1009.8}, 
        'AirTemperature': {'Instantaneous': 11.1}, 
        'RelativeHumidity': {'Instantaneous': 80}, 
        'WindSpeed': {'Mean': 1.7}, 
        'WindDirection': {'Mean': 55}, 
        'PeakGust': {'Maximum': 4.9, 'Direction': 58, 'MaximumTime': '2025-01-16T22:36:00'}, 
        'Precipitation': {'Accumulation': 0, 'MeltFlag': 0}, 
        'SunshineDuration': {'Total': None}, 
        'GlobalSolarRadiation': {'Accumulation': 0}, 
        'SoilTemperatureAt0cm': {'Instantaneous': 10.3}, 
        'SoilTemperatureAt5cm': {'Instantaneous': 12.1}, 
        'SoilTemperatureAt10cm': {'Instantaneous': 13}, 
        'SoilTemperatureAt20cm': {'Instantaneous': 13.7}, 
        'SoilTemperatureAt50cm': {'Instantaneous': 15.6}, 
        'SoilTemperatureAt100cm': {'Instantaneous': 18.6}}
        """

        return record
    
    def split_time_by_month(self, start_time, end_time):
        """
        request weather and rainfall history data by CODis.
        Duration between starttime and endtime should less than 31 days.
        """

        # 轉換為 datetime 物件
        start_date = pd.to_datetime(start_time)
        end_date = pd.to_datetime(end_time)

        # 生成每個月的起始日期
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        month_range_list = list()
        
        for month_start in date_range:
            # 設置每月的結束日期為當月的最後一秒（23:59:59）
            month_end = month_start + pd.DateOffset(months=1) - pd.DateOffset(seconds=1)
            
            # 如果結束日期超過 `end_time`，就將其設為 `end_time`
            if month_end > end_date:
                month_end = end_date

            start_str = month_start.strftime("%Y-%m-%dT%H:%M:%S")
            end_str = month_end.strftime("%Y-%m-%dT%H:%M:%S")
            
            month = {
                'month_start': start_str,
                'month_end': end_str
            }

            month_range_list.append(month)

        return month_range_list
