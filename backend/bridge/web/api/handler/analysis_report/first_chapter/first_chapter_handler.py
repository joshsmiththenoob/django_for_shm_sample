#     Deal with 1st Chapter of Analysis Report
import os
import time
from datetime import datetime
from django.conf import settings
from rest_framework.request import Request
from web.models import Bridge, Sensor, Agency, EngineeringFirm
from web.api.handler.date_handler import DateHandler
from web.api.handler.image_handler import ImageHandler
from web.api.handler.analysis_report.analysis_report_json_formatter import AnalysisReportJSONFormatter
from django.db.models import Prefetch
from django.contrib.auth.models import User


import base64
import io
import matplotlib.pyplot as plt
from PIL import Image


class FirstChapterHandler:

    def __init__(self, image_index):
        self.image_index = image_index
        self.__date_handler = DateHandler()
        self.__img_handler = ImageHandler()
    

    def get_report(self, user: User, bid: int, date: datetime):
        return  self.__get_bridge_informations_for_user(user, bid, date)
 

    def get_current_image_index(self):
        return self.image_index

    def __get_bridge_informations_for_user(self, user: User, bid: int, date: datetime):

        # 一律從 AuthAgencyUsers 表來找使用者所屬的 agency
        agency = Agency.objects.filter(authagencyusers__user=user).first()

        if not agency:
            raise ValueError("User has no agency associated")


        if (user.is_superuser):
            # 如果是 superuser，抓取指定的 bridge 即可

            bridge = Bridge.objects.filter(id=bid, deleted= 0).prefetch_related('sensors').first()
            if not bridge:
                raise ValueError("Bridge not found")

        else:

            bridge = Bridge.objects.filter(
                id=bid, 
                agencies=agency,  # 利用 related_name='agencies'
                deleted=0
            ).prefetch_related('sensors').first()

            if not bridge:
                raise ValueError("Bridge not found or unauthorized")

        sensors = bridge.sensors.all()
        engineering_firms = EngineeringFirm.objects.filter(agency=agency).first()

        bridge_location_base64 = self.__img_handler.get_image_with_bridge_location(bridge.longitude, bridge.latitude, bridge.name)
        
        bridge_info_dict = dict()
        bridge_info_dict["report_time"] = date
        bridge_info_dict["agency"] = agency
        bridge_info_dict["bridge"] = bridge
        bridge_info_dict["sensors"] = sensors
        bridge_info_dict["engineering_firms"] = engineering_firms
        bridge_info_dict["bridge_location_image"] = AnalysisReportJSONFormatter.get_image_info_dict(bridge_location_base64, self.image_index)
        self.image_index += 1

        return self.__format_data(bridge_info_dict)
    

    def __format_data(self, bridge_info_dict: dict):
        print(bridge_info_dict)
        result_dict = dict()

        result_dict["agency_name"] = bridge_info_dict["agency"].name
        result_dict["bridge_name"] =  bridge_info_dict["bridge"].name
        result_dict["area"] =  bridge_info_dict["bridge"].address_name + bridge_info_dict["bridge"].id_address_name
        result_dict["report_name"] = self.__get_report_name(bridge_info_dict["report_time"],
                                                            bridge_info_dict["bridge"].id_address_name,
                                                            bridge_info_dict["bridge"].name
                                                            )
        result_dict["user_company"] = bridge_info_dict["engineering_firms"].name
        result_dict["now_date"] = self.__date_handler.get_report_month_str(datetime.now())
        result_dict["event_list_date"] = self.__date_handler.get_report_month_str_gregorian(bridge_info_dict["report_time"])
        result_dict["longitude"] = bridge_info_dict["bridge"].longitude
        result_dict["latitude"] = bridge_info_dict["bridge"].latitude
        result_dict["bridge_maintenance_record"] =  "橋長為200 公尺，111年1月26日竣工後通車，近一次工程紀錄為114年1月底的維修紀錄。"
        result_dict["bridge_location_image"] = bridge_info_dict["bridge_location_image"]
        result_dict["sensor_data"] = self.__get_sensor_data(bridge_info_dict["bridge"], bridge_info_dict["sensors"])

        # print("result_dict :", result_dict["sensor_data"])

        return result_dict

    def __load_image_by_path(self, image_path: str):
        """
        Load image from specified path and return base64 encoded string.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_path}' not found.")

        with open(image_path, "rb") as image_file:
            base64_img = self.__img_handler.convert_img_into_base64(image_file)
            return base64_img



    def __get_report_name(self, date: datetime, district: str, strcture_name: str):
        """
        Get title of anaylysis report by date, district and structure name
        """

        report_month_str = self.__date_handler.get_report_month_str(date)

        return report_month_str + '份' + district + strcture_name

    


    def __get_sensor_data(self, bridge: Bridge, sensors: list):
        """
        get all sensor dataset including total count and individual sensor infomation
        """
        sensor_data_dict = dict()


        # Sensor Concept (統計sensor數量)
        sensor_concept_dict = dict()
        sensor_concept_dict["total_count"] = len(sensors)
        
        # 依照 type 統計數量，並直接紀錄在sensor_concept_dict
        for sensor in sensors:
            sensor_type = sensor.sensor_location
            if (sensor_type not in sensor_concept_dict):
                sensor_concept_dict[sensor_type] = 0
            sensor_concept_dict[sensor_type] += 1


        # Sensor List 詳細資料
        sensor_list = list()
        # bridge_photo_name = "Bridge8.png"
        bridge_base64 = bridge.base64
        # bridge_photo_name = bridge.photo_name
        for sensor in sensors:

            sensor_base64 = self.__img_handler.get_image_with_sensor_mark(bridge_base64, sensor.image_x, sensor.image_y)
            # self.__show_image_with_matplotlib(sensor_base64)
            sensor_item = {
                "detailed_location": sensor.detailed_location,
                "sensor_location": sensor.sensor_location,
                "ip": sensor.ip,
                "cable_mass_per_length": sensor.cable_mass_per_length,
                "cable_length": sensor.cable_length,
                "elasticity": sensor.elasticity,
                "inertia": sensor.inertia,
                "mass": sensor.mass,
                "span": sensor.span,
                "nearest_pier_distance": sensor.nearest_pier_distance,
                "health_alert_index": sensor.health_alert_index,
                "health_move_index": sensor.health_move_index,
                "event_alert_index": sensor.event_alert_index,
                "event_move_index": sensor.event_move_index,
                "sensor_location_image": AnalysisReportJSONFormatter.get_image_info_dict(sensor_base64, self.image_index)
            }

            self.image_index += 1  # 圖片index每次遞增
            sensor_list.append(sensor_item)
   

        # 統整兩個字典成一個大字典
        sensor_data_dict["sensor_concept"] = sensor_concept_dict
        sensor_data_dict["sensor_list"] = sensor_list

        return sensor_data_dict
    

    
    def __show_image_with_matplotlib(self, base64_str: str):
        # 1. 解碼 base64 到 bytes
        img_bytes = base64.b64decode(base64_str)
        
        # 2. 將 bytes 放進記憶體緩衝區並交由 PIL 開啟
        img_io = io.BytesIO(img_bytes)
        image = Image.open(img_io)

        # 3. 用 Matplotlib 顯示圖片
        plt.imshow(image)
        plt.axis('off')  # 隱藏座標軸，純粹看圖
        plt.show()