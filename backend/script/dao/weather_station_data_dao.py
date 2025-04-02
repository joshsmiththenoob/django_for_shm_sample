from script.dao.base_dao import BaseDAO
from sqlalchemy import text
from datetime import datetime

class WeatherStationDataDAO(BaseDAO):
    def __init__(self):
         # call the constructor of the parent class that ._engine is initialized
        super().__init__()

    def insert_weather_data(self, new_record: dict):
        sql = text(f"""
                    INSERT INTO weather_data (station_id, time, temperature, wind_speed, wind_direction, precipitation, acc_precipitation)
                    VALUES (:station_id, :time, :temperature, :wind_speed, :wind_direction, :precipitation, :acc_precipitation)
                    """).bindparams(station_id = new_record["station_id"],
                                    time = datetime.fromisoformat(new_record["time"]),
                                    temperature = new_record["temperature"],
                                    wind_speed = new_record["wind_speed"],
                                    wind_direction = new_record["wind_direction"],
                                    precipitation = new_record["precipitation"],
                                    acc_precipitation = new_record["acc_precipitation"]
                                    )

        return self.query(sql)
    
    def get_last_weather_data(self, station_id: str):
        sql = text(f"""
                    SELECT acc_precipitation FROM weather_data WHERE station_id = :station_id ORDER BY time DESC LIMIT 1
                   """).bindparams(station_id = station_id)
        return self.query(sql)

