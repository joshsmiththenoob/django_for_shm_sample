import os
import random
from web.models import Bridge
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from web.models import AuthAgencyUsers, AuthAgencyBridges, Bridge, WeatherStation
from rest_framework.request import Request
from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.project_list_serializer import ProjectListSerializer
from web.api.handler.image_handler import ImageHandler


"""
The rule of Reponse Body structure:
{
    "success"(boolean): if client get response successful or not
    "message"(string):  message detail
    "data"(any): return data
}

"""

class ProjectListService:
    serializer_class = ProjectListSerializer
    
    
    def __init__(self):
        pass


    def get(self, request: Request):
        """
        Get list of proejct
        """
        user = request.user
        try:
            if (user.is_superuser):
                # Admin sees all non-deleted bridges
                bridge_objects = Bridge.objects.filter(deleted=0).select_related('station_id')
            else:
                # Regular users see bridges related through AuthAgencyBridges
                bridge_ids = AuthAgencyBridges.objects.filter(
                    agency__authagencyusers__user=user,
                    bridge__deleted=0
                ).values_list('bridge_id', flat=True).distinct()

                bridge_objects = Bridge.objects.filter(id__in=bridge_ids).select_related('station_id')

            results = self.__format_data(bridge_objects)
            # set argument:many to True for getting multiple results from ORM objects
            serializer = self.serializer_class(data= results, many= True) 
            # form json

            if serializer.is_valid():
                return ResponseFormatter.format_get_response(serializer.data)
            else:
                return ResponseFormatter.format_400_response(serializer.errors)
        except Exception as e:
            print(e)


    def __format_data(self, bridge_objects: list):
        """
        Use Constant JSON for now
        will be modified in the furture
        """
        data_list = list()

        for bridge in bridge_objects:
            result_dict = dict()
            result_dict["bid"] = bridge.id
            result_dict["name"] = bridge.name
            result_dict["type"] = self.__map_type_into_chinese(bridge.type)
            result_dict["station"] = self.__get_fake_weather_data(bridge.station_id.name)
            result_dict["anomaly_sensor_list"] = self.__get_fake_anomaly_sensor_lists(bridge.id)
            result_dict["latest_health"] = 93 if bridge.id == 1 else random.randint(85, 100)
            result_dict["slope"] = self.__get_fake_trend_data()
            result_dict["earthquake"] = self.__get_fake_earthquake_data()
            result_dict["typhoon"] = self.__get_fake_typhoon_data()
            data_list.append(result_dict)
            
        return data_list

    def __map_type_into_chinese(self, building_type: str):
        """
        Mapping building type to Chinese name
        """
        building_type_map = {
            "bridge": "橋梁",
            "building": "建物",
            "neighbor": "鄰損"
        }

        return building_type_map[building_type]
        
    def __get_fake_weather_data(self, station_name: str):

        return {
            "name": station_name,
            "detail": {
                "precipitation": round(random.uniform(0.0, 1.5), 2),
                "temperature": round(random.uniform(17.5, 25.5), 2),
                "wind_speed": round(random.uniform(0.0, 5.9), 2),
                "wind_direction": round(random.uniform(0.1, 360.0), 1)
            }
        }



    def __get_fake_anomaly_sensor_lists(self, bid: int= None):
        """
        Constants for now
        will be deleted in the future
        """
        if (bid == 1):
            counts = 1  # 設定 counts 的範圍，例如 0 到 10
            # connection_count = random.randint(0, counts)  # 隨機選擇 connection_errors 的數量
            connection_count = 0  # 隨機選擇 connection_errors 的數量
            health_count = counts - connection_count  # 確保總數等於 counts
        else:
            counts = 0  # 設定 counts 的範圍，例如 0 到 10
            connection_count = random.randint(0, counts)  # 隨機選擇 connection_errors 的數量
            health_count = counts - connection_count  # 確保總數等於 counts

        connection_errors = [random.randint(100, 199) for _ in range(connection_count)] if connection_count > 0 else None
        health_errors = [random.randint(200, 299) for _ in range(health_count)] if health_count > 0 else None

        return {
            "counts": counts,
            "detail": {
                "connection_errors": connection_errors,
                "health_errors": health_errors
            }
        }
    

    def __get_fake_trend_data(self):
        """
        Constants for now
        will be deleted in the future
        """
        last_year = round(random.uniform(-0.5, 0.1), ndigits= 2)
        last_month = round(random.uniform(-0.5, 0.1), ndigits= 2)

        return {
            "last_year": last_year,
            "last_month": last_month
        }
    

    def __get_fake_earthquake_data(self):
        """
        Constants for now
        will be deleted in the future
        """
        eq_before_after = round(random.uniform(0.8, 1.1), ndigits= 2)
        eq_max_during = round(random.uniform(0.5, 1.1), ndigits= 2)

        return {
            "eq_before_after": eq_before_after,
            "eq_max_during": eq_max_during
        }


    
    def __get_fake_typhoon_data(self):
        """
        Constants for now
        will be deleted in the future
        """
        ty_before_after = round(random.uniform(0.8, 1.1), ndigits= 2)
        ty_max_during = round(random.uniform(0.5, 1.1), ndigits= 2)

        return {
            "ty_before_after": ty_before_after,
            "ty_max_during": ty_max_during
        }
