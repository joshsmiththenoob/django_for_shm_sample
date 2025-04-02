from script.dao.base_dao import BaseDAO
from sqlalchemy import text

class WeatherStationDAO(BaseDAO):
    def __init__(self):
         # call the constructor of the parent class that ._engine is initialized
        super().__init__()
    def insert_new_station_info(self, new_record: dict):
        sql = text(f"""
                    INSERT INTO weather_station (station_id, name, longitude, latitude, deleted)
                    VALUES (:station_id, :name, :longitude, :latitude, 0)
                   """).bindparams(station_id = new_record["data"]["aqi"][0]["station"]["stationId"],
                                   name = new_record["data"]["aqi"][0]["station"]["locationName"],
                                   longitude = new_record["data"]["aqi"][0]["station"]["longitude"],
                                   latitude = new_record["data"]["aqi"][0]["station"]["latitude"]
                                   )

        return self.query(sql)