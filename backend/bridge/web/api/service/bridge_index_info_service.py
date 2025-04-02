from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.bridge_index_info_serializer import BridgeIndexInfoSerializer
from web.api.dao.bridge_index_info_dao import BridgeIndexInfoDao
from datetime import datetime, timedelta
import math
import random


"""
The rule of Reponse Body structure:
{
    "success"(boolean): if client get response successful or not
    "message"(string):  message detail
    "data"(any): return data
}

"""

class BridgeIndexInfoService:
    serializer_class = BridgeIndexInfoSerializer
    def __init__(self):
        pass
    def get(self, bid: int):
        dao = BridgeIndexInfoDao()
        # try:
        data = dao.get_bridge_info(bid)
        print(data)
        result = [dict(zip(data["columns"], row)) for row in data["rows"]]
        # serializer = self.serializer_class(instance= result, many= True) 
        # format json
        data = self.__format_data(result)

        # serialize data
        serializer = BridgeIndexInfoSerializer(data= data)

        if serializer.is_valid():
            json = ResponseFormatter.format_get_response(serializer.data)
        else:
            print(serializer.errors)
            json = ResponseFormatter.format_400_response(serializer.data)

        # except Exception as e:
        #     print(e)
        #     json = ResponseFormatter.format_500_response()


        return json
    

    def __format_data(self, result: list):
        """
        Format Data: reformat data from query result
        """

        sensor_list = list()
        recent_health = 0    
        for sensor in result:
            sensor_dict = dict()
            print(sensor["sensor"])
            if (sensor["sensor"]):
                sensor_dict["sensor"] = sensor["sensor"]
                sensor_dict["latest_time"] = sensor["latest_time"]
                sensor_dict["latest_health"] = sensor["latest_health"]
                sensor_dict["type"] = sensor["type"]
                sensor_dict["ip"] = sensor["ip"]
                sensor_dict["sensor_location"] = sensor["sensor_location"]
                sensor_dict["detailed_location"] = sensor["detailed_location"]
                sensor_dict["cable_mass_per_length"] = sensor["cable_mass_per_length"]
                sensor_dict["cable_length"] = sensor["cable_length"]
                sensor_dict["elasticity"] = sensor["elasticity"]
                sensor_dict["inertia"] = sensor["inertia"]
                sensor_dict["mass"] = sensor["mass"]
                sensor_dict["health_alert_index"] = sensor["health_alert_index"]
                sensor_dict["health_move_index"] = sensor["health_move_index"]
                sensor_dict["event_alert_index"] = sensor["event_alert_index"]
                sensor_dict["event_move_index"] = sensor["event_move_index"]
                sensor_dict["bridge_alert_index"] = sensor["bridge_alert_index"]
                sensor_dict["bridge_move_index"] = sensor["bridge_move_index"]
                image_coordinate = {"x": sensor["image_x"], "y": sensor["image_y"]}
                sensor_dict["image_coordinate"] = self.__set_sensor_img_coordinate(image_coordinate)
                # sensor_dict["status"] = self.__set_sensor_status(sensor["latest_time"])
                sensor_dict["status"] = sensor["status"]
                sensor_list.append(sensor_dict)
                if sensor["latest_health"]:
                    recent_health += (sensor["latest_health"]) ** 2



        # format data
        bridge = dict()
        bridge["bid"] = result[0]["bid"]
        bridge["bridge_name"] = result[0]["bridge_name"]
        bridge["address_name"] = result[0]["address_name"]
        bridge["id_address_name"] = result[0]["id_address_name"]
        bridge["longitude"] = result[0]["longitude"]
        bridge["latitude"] = result[0]["latitude"]
        bridge["photo_name"] = result[0]["photo_name"]
        bridge["base64"] = result[0]["base64"]
        bridge["latest_health"] = int(math.sqrt(recent_health / len(sensor_list))) if recent_health else None

        
        weather = dict()
        weather["latest_weather_time"] = result[0]["latest_weather_time"]
        weather["latest_precipitation"] = result[0]["precipitation"]
        weather["latest_temperature"] = result[0]["temperature"]
        weather["latest_wind_speed"] = result[0]["wind_speed"]
        weather["latest_wind_direction"] = result[0]["wind_direction"]



        earthquake = dict()
        earthquake["eq_event_id"] = result[0]["eq_event_id"]
        earthquake["eq_origintime"] = result[0]["eq_origintime"]
        earthquake["eq_endtime"] = self.__set_earthquake_endtime(result[0]["eq_origintime"])
        earthquake["eq_magnitudevalue"] = result[0]["eq_magnitudevalue"]
        earthquake["eq_post_event_health"] = result[0]["eq_post_event_health"]
        earthquake["eq_longitude"] = result[0]["eq_longitude"]
        earthquake["eq_latitude"] = result[0]["eq_latitude"]
        earthquake["eq_post_event_health"] = result[0]["eq_post_event_health"]


        typhoon = dict()
        typhoon["ty_event_id"] = result[0]["ty_event_id"]
        typhoon["ty_cht_name"] = result[0]["ty_cht_name"]
        typhoon["ty_eng_name"] = result[0]["ty_eng_name"]
        typhoon["ty_sea_start_datetime"] = result[0]["ty_sea_start_datetime"]
        typhoon["ty_sea_end_datetime"] = result[0]["ty_sea_end_datetime"]
        typhoon["ty_max_intensity"] = result[0]["ty_max_intensity"]
        typhoon["ty_post_event_health"] = result[0]["ty_post_event_health"]

        data = {
            "bridge": bridge,
            "weather": weather,
            "sensor_list": sensor_list,
            "earthquake": earthquake,
            "typhoon": typhoon
        }
        
        return data
    

    # def __set_sensor_status(self, latest_time: datetime):
    #     """
    #     Get sensor status which depends on delta time
    #     """
    #     try:
    #         now = datetime.now()
    #         print(now - latest_time)
    #         if (now - latest_time) >= timedelta(hours=1):
    #             return 2
    #         elif (now - latest_time) >= timedelta(minutes= 10):
    #             return 1
    #         else:
    #             return 0
    #     except:
    #         return None
        
    def __set_earthquake_endtime(self, origintime: datetime):
        """
        For now, 
        assume that earthquake's endtim occurs 2 minutes after its origintime."
        """
        if (origintime):
            return origintime + timedelta(minutes = 2)
        else:
            return None
    

    def __set_sensor_img_coordinate(self, origin_coordinate: dict, set_random: bool= True):
        """
        ***
        Temporary method for setting image coordinate of sensor 
        Will be deleted in the future
        ***
        """
        if (origin_coordinate["x"]) or (origin_coordinate["y"]):
            return origin_coordinate
        
        elif ((not origin_coordinate["x"]) and (not origin_coordinate["y"]) and (set_random == True)):
            x = random.randint(10, 90)
            y = random.randint(10, 90)

            return {"x": x, "y": y}
        
        else: 
            return origin_coordinate
            
# 1-100
# 10-90