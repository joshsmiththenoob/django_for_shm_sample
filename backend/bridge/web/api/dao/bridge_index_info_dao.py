from django.db import connection


class BridgeIndexInfoDao:
    def __init__(self):
        pass

    def get_bridge_info(self, bid: int):
        
        query = """
                SELECT 
            BridgeInfo.bid,
            SensorInfo.sensor,
            BridgeInfo.bridge_name, 
            BridgeInfo.address_name, 
            BridgeInfo.id_address_name,
            BridgeInfo.longitude,
            BridgeInfo.latitude,
            BridgeInfo.photo_name,
            BridgeInfo.base64,
            WeatherInfo.time AS latest_weather_time,
            WeatherInfo.precipitation,
            WeatherInfo.temperature,
            WeatherInfo.wind_speed,
            WeatherInfo.wind_direction,
            SensorInfo.latest_time, 
            SensorInfo.latest_health, 
            SensorInfo.type,
            SensorInfo.ip,
            SensorInfo.sensor_location,
            SensorInfo.detailed_location,
            SensorInfo.cable_mass_per_length,
            SensorInfo.cable_length,
            SensorInfo.elasticity,
            SensorInfo.inertia,
            SensorInfo.mass,
            SensorInfo.health_alert_index,
            SensorInfo.health_move_index,
            SensorInfo.event_alert_index,
            SensorInfo.event_move_index,
            SensorInfo.bridge_alert_index,
            SensorInfo.bridge_move_index,
            SensorInfo.image_x,
            SensorInfo.image_y,
            SensorInfo.status,
            EarthquakeEvent.event_id AS eq_event_id, 
            EarthquakeEvent.origintime AS eq_origintime, 
            EarthquakeEvent.magnitudevalue AS eq_magnitudevalue, 
            EarthquakeEvent.post_event_health AS eq_post_event_health,
            EarthquakeEvent.longitude AS eq_longitude,
            EarthquakeEvent.latitude AS eq_latitude,
            TyphoonEvent.event_id AS ty_event_id,
            TyphoonEvent.cht_name AS ty_cht_name,
            TyphoonEvent.eng_name AS ty_eng_name,
            TyphoonEvent.sea_start_datetime AS ty_sea_start_datetime,
            TyphoonEvent.sea_end_datetime AS ty_sea_end_datetime,
            TyphoonEvent.max_intensity AS ty_max_intensity,
            TyphoonEvent.post_event_health AS ty_post_event_health
        FROM (
            SELECT 
                bridge.id AS bid,
                bridge.name AS bridge_name, 
                bridge.address_name, 
                bridge.id_address_name, 
                bridge.longitude,
                bridge.latitude,
                bridge.photo_name,
                bridge.base64,
                bridge.station_id
            FROM 
                bridge
            WHERE 
                bridge.id = %s AND bridge.deleted = 0
        ) AS BridgeInfo
        LEFT JOIN (
            SELECT 
                sensor.bid,
                sensor.sensor,
                latest_minute_data.time AS latest_time,
                latest_minute_data.mid_health AS latest_health,
                sensor.type,
                sensor.ip,
                sensor.sensor_location,
                sensor.detailed_location,
                sensor.cable_mass_per_length,
                sensor.cable_length,
                sensor.elasticity,
                sensor.inertia,
                sensor.mass,
                sensor.health_alert_index,
                sensor.health_move_index,
                sensor.event_alert_index,
                sensor.event_move_index,
                sensor.bridge_alert_index,
                sensor.bridge_move_index,
                sensor.image_x,
                sensor.image_y,
                sensor.current_status AS status
            FROM 
                sensor
				LEFT JOIN (
				    SELECT mhd.*
				    FROM minute_history_data mhd
				    INNER JOIN (
				        SELECT bid, sensor, MAX(time) AS max_time
				        FROM minute_history_data
				        GROUP BY bid, sensor
				    ) latest_data 
				    ON mhd.bid = latest_data.bid
				    AND mhd.sensor = latest_data.sensor
				    AND mhd.time = latest_data.max_time
				) latest_minute_data
				ON sensor.bid = latest_minute_data.bid
				AND sensor.sensor = latest_minute_data.sensor
				WHERE sensor.deleted = 0 AND sensor.bid = %s

        ) AS SensorInfo ON BridgeInfo.bid = %s
        LEFT JOIN (
        SELECT 
				 weather_station.station_id,
                 weather_data.time,
   				 weather_data.precipitation,
   				 weather_data.temperature,
   				 weather_data.wind_speed,
   				 weather_data.wind_direction
   			FROM 
   				 weather_station
   			LEFT JOIN
   				 weather_data ON weather_station.station_id = weather_data.station_id
					 WHERE weather_data.time = (
					 	SELECT MAX(time)
					 	FROM weather_data
					 	WHERE weather_data.station_id = weather_station.station_id
						)
	      )AS WeatherInfo ON WeatherInfo.station_id = BridgeInfo.station_id
        LEFT JOIN (
        SELECT 
                earthquake_event.event_id,
                earthquake.origintime,
                earthquake.magnitudevalue,
                earthquake.longitude,
                earthquake.latitude,
                final_seismic_resistance.sensor,
                final_seismic_resistance.post_event_health
            FROM
                earthquake_event
            LEFT JOIN
                earthquake ON earthquake_event.event_id = earthquake.earthquakeno
            LEFT JOIN
                final_seismic_resistance ON earthquake_event.bid = final_seismic_resistance.bid
            WHERE 
                earthquake_event.bid = %s
                AND earthquake_event.event_id = (
                    SELECT MAX(event_id) 
                    FROM earthquake_event 
                    WHERE bid = %s
                )
            GROUP BY 
                final_seismic_resistance.sensor
        ) AS EarthquakeEvent ON EarthquakeEvent.sensor = SensorInfo.sensor
        LEFT JOIN (
            SELECT 
                typhoon_event.event_id,
                typhoon.cht_name,
                typhoon.eng_name,
                typhoon.sea_start_datetime,
                typhoon.sea_end_datetime,
                typhoon.max_intensity,
                final_flood_resistance.sensor,
                final_flood_resistance.post_event_health
            FROM
                typhoon_event
            LEFT JOIN
                typhoon ON typhoon_event.event_id = typhoon.id
            LEFT JOIN
                final_flood_resistance ON typhoon_event.bid = final_flood_resistance.bid
            WHERE 
                typhoon_event.bid = %s
                AND typhoon_event.event_id = (
                    SELECT MAX(event_id)
                    FROM typhoon_event
                    WHERE bid = %s
            )
            GROUP BY 
                final_flood_resistance.sensor
        ) AS TyphoonEvent ON TyphoonEvent.sensor = SensorInfo.sensor
        GROUP BY 
	        SensorInfo.detailed_location
        """

        # return results of query
        with connection.cursor() as cursor:
            cursor.execute(query, [bid, bid, bid, bid, bid, bid, bid])
            rows = cursor.fetchall()

            # 將查詢結果轉換為字典格式
            columns = [col[0] for col in cursor.description]  # 獲取列名
        
            return {
                "rows": rows,
                "columns": columns
            }
        