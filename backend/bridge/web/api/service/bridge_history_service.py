import numpy as np
from web.models import Sensor, StructureMinuteHistoryData, StructureHourlyHistoryData, StructureDailyHistoryData, WeatherDailyHistoryData, Bridge
from rest_framework.request import Request
from web.api.serializer.bridge_history_serializer import BridgeHistorySerializer
from bridge.utils.response_formatter import ResponseFormatter
from datetime import datetime, timedelta
from django.db.models import OuterRef, Subquery, Value, FloatField
from django.db.models.functions import TruncDate, Coalesce

class BridgeHistoryService:
    serializer_class = BridgeHistorySerializer
    prefixes = ["up_", "mid_", "down_"] # regards prefix as a class variable so that every object get the same prefix to query
    additional_features = ["time"]
    def get(self, request: Request, bid: int):
        """
        Search specific columns based on prefixes, suffixes above 
        """
        try:
            # parse query params
            start_date_str = request.query_params.get("start")
            end_date_str = request.query_params.get("end")

            filtered_features = self.__get_filtered_fields(bid)
            # print(filtered_features)

            time_dict = self.__get_time_range_dict(start_date_str, end_date_str)

            data = self.__get_data_from_custom_range(bid, time_dict, filtered_features)
            serializer = self.serializer_class(data= data)
            if serializer.is_valid():
                json = ResponseFormatter.format_get_response(serializer.data)
            else:
                print(serializer.errors)
                json = ResponseFormatter.format_400_response(serializer.data)


            
        except Exception as e:
            print(e)
            json = ResponseFormatter.format_500_response(str(e))

        return json
        
        

    def __get_time_range_dict(self, start_time: str, end_time: str):
        """
        get time range between custom start time and custom end time
        """
        time_dict = dict()
        start_date = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
        
        time_dict["start_date"] = start_date
        time_dict["end_date"] = end_date
        time_dict["time_range"] = (end_date - start_date)

        return time_dict
    

    def __get_data_from_custom_range(self, bid: int, time_dict: dict, filtered_features: list):
        """
        get query results from Django ORM
        """

        weather_filter_features = [
                'up_temperature', 'mid_temperature', 'down_temperature',
                'up_wind_speed', 'mid_wind_speed', 'down_wind_speed',
                'up_wind_direction', 'mid_wind_direction', 'down_wind_direction',
                'up_precipitation', 'mid_precipitation', 'down_precipitation'
                ]

        if (time_dict["time_range"] <= timedelta(days = 1)):
            minute_filtered = StructureMinuteHistoryData.objects.filter(
                bid= bid,
                time__range=(time_dict["start_date"], time_dict["end_date"])
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
            time_filtered = minute_filtered

        elif (time_dict["time_range"] <= timedelta(weeks= 1)):
            quartile_filtered = StructureHourlyHistoryData.objects.filter(
                bid= bid,
                time__range=(time_dict["start_date"], time_dict["end_date"])
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

            time_filtered = quartile_filtered

        elif (time_dict["time_range"] > timedelta(weeks= 1)):
            daily_filtered = StructureDailyHistoryData.objects.filter(
                bid= bid,
                time__range=(time_dict["start_date"], time_dict["end_date"])
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

            time_filtered = daily_filtered
            
        # 最終合併查詢

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
        
        results = time_filtered.annotate( **annotations)

        if (not results):
            raise ValueError("No data found for the given parameters.")

        return self.__format_data(filtered_features, results)


    def __get_filtered_fields(self, bid: int):
        """
        Get all fields that contain specific prefixes & suffixes.
        And add time field
        """
        suffixes = ["health", "seismic", "centroid_frequency", "damping_ratio", "temperature", "wind_speed", "wind_direction", "precipitation"]

        all_features = [field.name for field in StructureMinuteHistoryData._meta.get_fields()]
        filtered_features = [feature for feature in all_features 
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

                    # if category not in data(dictionary)'s key : create the key(category) and value(dictionary)
                    if (category not in temp_weather_result_dict):
                        temp_weather_result_dict[category] = dict()
                        temp_weather_result_dict[category]["title"] = category                       

                # if category not in data(dictionary)'s key : create the key(category) and value(dictionary)    
                elif (category not in temp_result_dict):                    
                    temp_result_dict[category] = dict()
                    temp_result_dict[category]["title"] = category     
                    result_dict = temp_result_dict 
                
                values = list(results.values_list(feature, flat= True))
                if (feature.startswith("up_")):
                    result_dict[category]["Q3"] = values

                elif (feature.startswith("mid_")):
                    result_dict[category]["Q2"] = values
                    polyfit_result = self.__polyfit(np.array(values, dtype=float))
                    if (category == "health"):
                        result_dict[category]["fit_curve"] = polyfit_result["fit_curve"]
                        result_dict[category]["slope"] = polyfit_result["slope"]
                    else:
                        result_dict[category]["fit_curve"] = list()
                        result_dict[category]["slope"] = None
                    result_dict[category]["latest_data"] = results.values_list(feature, flat=True).last()

                elif (feature.startswith("down_")):
                     result_dict[category]["Q1"] = values
                
        # convert temp_result_dict dictionary into list of values and store them in data["result"]
        data["result"] = list(temp_result_dict.values())
        data["weather_result"] = list(temp_weather_result_dict.values())

        return data
    

    
    def __polyfit(self, data: np.array, power: int = 1):
        """
        Curve fitting by power factor
        """
        # get x-axis
        x = np.arange(0, (len(data)))
        param = np.polyfit(x, data, power)

        # get the value of fit curve corresponding to x-axis
        fit_curve = np.polyval(param, x)     
        fit_curve = np.round(fit_curve, 2)

        # get slope when use linear fitting
        slope = round(param[0], ndigits= 2) if power == 1 else None
        

        # format polyfit result
        polyfit_result = dict()
        polyfit_result["fit_curve"] = fit_curve
        polyfit_result["slope"] = slope

        return polyfit_result
    
