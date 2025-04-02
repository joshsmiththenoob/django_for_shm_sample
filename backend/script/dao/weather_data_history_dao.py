from script.dao.base_dao import BaseDAO
from sqlalchemy import text
from datetime import datetime

class WeatherDataHistoryDAO(BaseDAO):
    def __init__(self):
         # call the constructor of the parent class that ._engine is initialized
        super().__init__()

    def insert_weather_history_data(self, new_record: list):
        sql = text(f"""
                    INSERT INTO weather_data (station_id, time, temperature, wind_speed, wind_direction, precipitation)
                    VALUES (:station_id, :time, :temperature, :wind_speed, :wind_direction, :precipitation)
                    """)

        return self.query(sql, new_record)

