import os
import time
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.request import Request
from web.models import (Bridge, 
                        Sensor, 
                        Agency, 
                        StructureMinuteHistoryData, 
                        StructureHourlyHistoryData,
                        StructureDailyHistoryData,
                        WeatherDailyHistoryData, 
                        MinuteHistoryData,
                        DailyHistoryData,
                        QuartileData,
                        )
from web.api.handler.statistic_handler import StatisticHandler
from web.api.handler.date_handler import DateHandler
from web.api.handler.analysis_report.analysis_report_json_formatter import AnalysisReportJSONFormatter
from django.db.models import Prefetch
from django.contrib.auth.models import User


class AnalysisReportRepository:
    def __init__(self, end_date: datetime, report_type: str):
        self.__date_handler = DateHandler()
        self.end_date = end_date
        self.report_type = report_type
        self.__initalize_tables()
    
    def set_report_type(self, report_type: str):
        self.report_type = report_type
        self.__initalize_tables()
    def get_bridge_query_result(self, bridge: Bridge, features_dict: dict):
        """
        Get the last day's statistics report for a specific bridge   
        """

        # Query specific table with filtered features of sensors grouped by location
        query_results = self.bridge_model.objects.filter(
                    bid= bridge.id,
                    time__gte= self.start_date,
                    time__lt = self.end_date
        ).values(*features_dict["filtered_features"])

        return query_results

        
    def get_sensor_query_result(self, bridge: Bridge, sensor_id : str, features_dict: dict):
        """
        Get the last day's statistics report for a specific bridge and its own sensors.        
        """

        # Query specific table with filtered features of sensors grouped by location
        query_results = self.sensor_model.objects.filter(
                    bid= bridge.id,
                    sensor= sensor_id,
                    time__gte= self.start_date,
                    time__lt = self.end_date
        ).values(*features_dict["filtered_features"])
                
        return query_results

    def __initalize_tables(self):
        """
        Initialize repository settings based on the report type.
            1. start_date: The beginning of the report period.
            2. bridge_model: The Django ORM model used for querying bridge-related data.
            3. sensor_model: The Django ORM model used for querying sensor-related data.
            based on report type
        """

        self.start_date = self.__date_handler.get_report_start_time(self.end_date, self.report_type)

        if (self.report_type == "last_day"):
            self.bridge_model = StructureMinuteHistoryData
            self.sensor_model = MinuteHistoryData
        elif (self.report_type == "last_month"):
            self.bridge_model = StructureHourlyHistoryData
            self.sensor_model = QuartileData
        elif (self.report_type == "last_year"):
            self.bridge_model = StructureDailyHistoryData
            self.sensor_model = DailyHistoryData
        else:
            raise ValueError(f"Wrong report_type: {self.report_type}, Please Check it!!")