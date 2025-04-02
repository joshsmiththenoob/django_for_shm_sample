#     Deal with 2nd Chapter of Analysis Report
import os
import time
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.request import Request
from web.models import Bridge, Sensor, Agency, StructureMinuteHistoryData, WeatherDailyHistoryData, MinuteHistoryData
from web.api.handler.statistic_handler import StatisticHandler
from web.api.handler.date_handler import DateHandler
from web.api.handler.analysis_report.analysis_report_json_formatter import AnalysisReportJSONFormatter
from web.api.handler.analysis_report.second_chapter.second_chapter_base import SecondChapterBase
from django.db.models import Prefetch
from django.contrib.auth.models import User
from web.api.handler.ai_report_handler import AIReportHandler



class SecondChapterHandler(SecondChapterBase): 
    # regards prefix as a class variable so that every object get the same prefix to query
    additional_features = ["time"]
    prefixes = ["max_", "up_", "mid_", "down_", "min_"] 


    def __init__(self, image_index):
        super().__init__()
        self.image_index = image_index
        self.__date_handler = DateHandler()
        # datetime_str = "2025-03-10 14:00:00"
        # self.current_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        # self.current_time = now()

    
    def get_current_image_index(self):
        return self.image_index
    
    def set_current_image_index(self, image_index: int):
        self.image_index = image_index
        
    
    def __get_bridge_informations_for_user(self, user: User, bid: int, date: datetime):

        # Get agency by AuthAgencyUsers
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

        return bridge, sensors, date

    
    def get_last_day_report(self, user: User, bid: int, date: datetime):
        report_type = "last_day"
        bridge, sensors, date = self.__get_bridge_informations_for_user(user, bid, date)

        # Get report
        bridge_report = self.get_bridge_report(bridge, date, report_type)
        sensor_report_list = self.get_sensor_report(bridge, sensors, date, report_type)
        

        # Get last days weather information
        station_id = bridge.station_id
        weather_data = WeatherDailyHistoryData.objects.filter(
                        station_id=station_id.station_id,
                        time__date=date  # 比較日期部分
                    ).first()
        
        # format json result for last date
        last_day_result = dict()
        last_day_result["last_date"] = self.__date_handler.get_report_date_str(date)
        last_day_result["temperature"] = weather_data.mid_temperature
        last_day_result["wind_speed"] = weather_data.mid_wind_speed
        last_day_result["wind_direction"] = weather_data.mid_wind_direction
        last_day_result["bridge_data"] = bridge_report
        last_day_result["sensor_data"] = sensor_report_list


        # Get AI results
        ai_handler = AIReportHandler()
        last_day_result["ai_report_messages"]= ai_handler.get_ai_results(sensor_report_list)
        # print(last_day_result["ai_report_messages"])
        return last_day_result

        # print(last_day_result["ai_report_messages"])


    def get_last_month_report(self, user: User, bid: int, date: datetime):
        report_type = "last_month"
        bridge, sensors, date = self.__get_bridge_informations_for_user(user, bid, date)


        # Get report
        bridge_report = self.get_bridge_report(bridge, date, report_type, with_trend= True)
        sensor_report_list = self.get_sensor_report(bridge, sensors, date, report_type, with_trend= True)

    
        # Get start date and end date timestamp
        start_date = self.__date_handler.get_report_start_time(date, report_type)
        start_date_str = self.__date_handler.get_report_date_str(start_date)
        end_date_str = self.__date_handler.get_report_date_str(date)
        
        # format json result for last date
        last_month_result = dict()
        last_month_result["start_date"] = start_date_str
        last_month_result["end_date"] = end_date_str
        last_month_result["bridge_data"] = bridge_report
        last_month_result["sensor_data"] = sensor_report_list 

        return last_month_result


    def get_last_year_report(self, user: User, bid: int, date: datetime):
        report_type = "last_year"
        bridge, sensors, date = self.__get_bridge_informations_for_user(user, bid, date)


        # Get report
        bridge_report = self.get_bridge_report(bridge, date, report_type, with_trend= True)
        sensor_report_list = self.get_sensor_report(bridge, sensors, date, report_type, with_trend= True)

    
        # Get start date and end date timestamp
        start_date = self.__date_handler.get_report_start_time(date, report_type)
        start_date_str = self.__date_handler.get_report_date_str(start_date)
        end_date_str = self.__date_handler.get_report_date_str(date)
        
        # format json result for last date
        last_year_result = dict()
        last_year_result["start_date"] = start_date_str
        last_year_result["end_date"] = end_date_str
        last_year_result["bridge_data"] = bridge_report
        last_year_result["sensor_data"] = sensor_report_list 

        return last_year_result