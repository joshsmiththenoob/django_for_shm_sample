from web.models import MinuteHistoryData, QuartileData, Sensor, WeatherDailyHistoryData, Bridge
from web.api.serializer.sensor_data_report_serializer import SensorDataReportSerializer
from bridge.utils.response_formatter import ResponseFormatter
from datetime import datetime, timedelta
from django.db.models import OuterRef, Subquery, FloatField, Value
from django.db.models.functions import TruncDate, Coalesce

class SensorDataReportService:
    serializer_class = SensorDataReportSerializer
    prefixes = ["up_", "mid_", "down_"] # regards prefix as a class variable so that every object get the same prefix to query
    additional_features = ["time"]

    def __init__(self):
        datetime_str = "2025-03-10 14:00:00"
        self.current_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        # self.current_time = now()

    def get(self, bid: int, sid: int):
        """
        Search specific columns based on prefixes, suffixes above 
        """

        try:
            # Get filtered_features
            filtered_features = self.__get_filtered_fields(bid, sid)
            last_day_data = self.__get_last_day_data(bid, sid, filtered_features)
            last_hour_data = self.__get_last_hour_data(bid, sid, filtered_features)
            
            data = dict()
            data["hours"] = last_day_data
            data["minutes"] = last_hour_data

            serializer = self.serializer_class(data= data)
            if serializer.is_valid():
                json = ResponseFormatter.format_get_response(serializer.data)
            else:
                print(serializer.errors)
                json = ResponseFormatter.format_400_response(serializer.data)

        except Exception as e:
            print(e)
            json = ResponseFormatter.format_500_response()

        return json
    
    
    def __get_filtered_fields(self, bid: int, sid: int):
        """
        Get all fields that contain specific prefixes & suffixes.
        And add time field
        """
        location = Sensor.objects.filter(bid= bid, sensor= sid).values_list("sensor_location", flat= True).first()
        suffixes = ["health", "seismic", "centroid_frequency", "damping_ratio", "temperature", "wind_speed", "wind_direction", "precipitation"]

        # add suffix which depends on sensor_location
        if (location == "deck"):
            suffixes.append("load_carry_capacity")
        elif (location == "cable"):
            suffixes.append("cable_force")
        elif (location == "pier"):
            suffixes.append("effective_length")
        else :
            raise ValueError("Invallid sensor type!!")

        minute_features = [field.name for field in MinuteHistoryData._meta.get_fields()]
        filtered_features = [feature for feature in minute_features 
                             if any(feature.startswith(prefix) for prefix in self.prefixes) and 
                                any(feature.endswith(suffix) for suffix in suffixes)]

        weather_features = [field.name for field in WeatherDailyHistoryData._meta.get_fields()]
        filtered_weather_features = [feature for feature in weather_features 
                             if any(feature.startswith(prefix) for prefix in self.prefixes) and 
                                any(feature.endswith(suffix) for suffix in suffixes)]
        
        filtered_features.extend(filtered_weather_features)

        if (self.additional_features):
            filtered_features.extend(self.additional_features)

        return filtered_features
    

    def __get_end_time(self, current_time, interval: str):
        if (interval == "minute"):
            return current_time - timedelta(hours= 1)
        elif (interval == "hour"):
            return current_time - timedelta(days= 1)
        

    def __format_data(self, filtered_features: list, results: object):
        data = dict()
        data["result"] = list()
        temp_result_dict = dict()
        temp_weather_result_dict = dict()

        for feature in filtered_features:
            if (feature == "time"):
                # if feature == time: just get list directly
                feature_values = list(results.values_list(feature, flat= True))
                data["time"] = feature_values

            else:
                # otherise, should create another dictionary depends on category
                # get catecory behind "_"
                # ex: up_load_carry_capacity -> the category will be load_carry_capacity
                category = "_".join(feature.split("_")[1:])

                detail_features = ["temperature", "wind_speed", "wind_direction", "precipitation"]

                if (category in detail_features):
                    result_dict = temp_weather_result_dict    

                    if (category not in temp_weather_result_dict):
                        temp_weather_result_dict[category] = dict()
                        temp_weather_result_dict[category]["title"] = category                       
                    
                elif (category not in temp_result_dict):                    
                    temp_result_dict[category] = dict()
                    temp_result_dict[category]["title"] = category     
                    result_dict = temp_result_dict               
                    
                if (feature.startswith("up_")):
                    result_dict[category]["Q3"] = list(results.values_list(feature, flat= True))

                elif (feature.startswith("mid_")):
                    result_dict[category]["Q2"] = list(results.values_list(feature, flat= True))
                    result_dict[category]["latest_data"] = results.values_list(feature, flat=True).last()

                elif (feature.startswith("down_")):
                    result_dict[category]["Q1"] = list(results.values_list(feature, flat= True))
                
        # convert temp_result_dict dictionary into list of values and store them in data["result"]
        data["result"] = list(temp_result_dict.values())
        data["weather_result"] = list(temp_weather_result_dict.values())

        return data
    

    def __get_last_day_data(self, bid: int, sid: int, filtered_features: list):
        """
        Get last day data- interval: per hour
        """
        weather_filter_features = [
                'up_temperature', 'mid_temperature', 'down_temperature',
                'up_wind_speed', 'mid_wind_speed', 'down_wind_speed',
                'up_wind_direction', 'mid_wind_direction', 'down_wind_direction',
                'up_precipitation', 'mid_precipitation', 'down_precipitation'
                ]

        one_day_ago = self.__get_end_time(self.current_time, interval= "hour")

        # 先過濾 QuartileData 符合條件的資料
        quartile_filtered = QuartileData.objects.filter(
            bid=bid, 
            sensor=sid, 
            time__gte= one_day_ago,
            time__lt= self.current_time
        ).annotate(
                station_id=Subquery(
                    Bridge.objects.filter(id=OuterRef('bid')).values('station_id')[:1]
                ),
                date_only=TruncDate('time')  # 轉換成 YYYY-MM-DD
        ).values()

        # 再透過 Subquery 來匹配 WeatherDailyHistoryData
        weather_subquery = WeatherDailyHistoryData.objects.filter(
            station_id=OuterRef('station_id'),
            time=OuterRef('date_only')  # 只比較日期
        ).values( *weather_filter_features)

        # 最終合併查詢
        annotations = {
                feature: Coalesce(
                    Subquery(weather_subquery.values(feature)[:1]), 
                    Value(0),
                    output_field=FloatField()  # 強制指定輸出的字段型別為 FloatField
                )
                for feature in weather_filter_features
            }

        results = quartile_filtered.annotate( **annotations)
        
        return self.__format_data(filtered_features, results)


    def __get_last_hour_data(self, bid: int, sid: int, filtered_features: list):
        """
        Get last hour data- interval: per minute
        """
        weather_filter_features = [
                'up_temperature', 'mid_temperature', 'down_temperature',
                'up_wind_speed', 'mid_wind_speed', 'down_wind_speed',
                'up_wind_direction', 'mid_wind_direction', 'down_wind_direction',
                'up_precipitation', 'mid_precipitation', 'down_precipitation'
                ]
        
        one_hour_ago = self.__get_end_time(self.current_time, interval= "minute")
        # print(one_hour_ago)
        # Get query result
        # 先過濾 QuartileData 符合條件的資料
        minute_filtered = MinuteHistoryData.objects.filter(
            bid=bid, 
            sensor=sid, 
            time__gte= one_hour_ago,
            time__lt= self.current_time
        ).annotate(
                station_id=Subquery(
                    Bridge.objects.filter(id=OuterRef('bid')).values('station_id')[:1]
                ),
                date_only=TruncDate('time')  # 轉換成 YYYY-MM-DD
        ).values()

        # 再透過 Subquery 來匹配 WeatherDailyHistoryData
        weather_subquery = WeatherDailyHistoryData.objects.filter(
            station_id=OuterRef('station_id'),
            time=OuterRef('date_only')  # 只比較日期
        ).values(*weather_filter_features)

        # 最終合併查詢
        annotations = {
                # Coalesce 可以處理多個NULL，將查詢結果為NULL更改為0
                feature: Coalesce(
                    Subquery(weather_subquery.values(feature)[:1]), 
                    Value(0),
                    output_field=FloatField() # 使用Coalesce必須指定輸出的字段型別
                )
                for feature in weather_filter_features
            }

        results = minute_filtered.annotate( **annotations)
        
        return self.__format_data(filtered_features, results)
