#     Deal with 1st Chapter of Analysis Report
import os
import time
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.request import Request
from web.models import Bridge, Sensor, Agency, StructureMinuteHistoryData, WeatherDailyHistoryData, MinuteHistoryData
from web.api.handler.statistic_handler import StatisticHandler
from web.api.handler.date_handler import DateHandler
from web.api.handler.analysis_report.analysis_report_json_formatter import AnalysisReportJSONFormatter
from web.api.handler.analysis_report.analysis_report_repository import AnalysisReportRepository
from django.db.models import Prefetch
from django.contrib.auth.models import User


class SecondChapterBase:
    # regards prefix as a class variable so that every object get the same prefix to query
    additional_features = ["time"]
    prefixes = ["max_", "up_", "mid_", "down_", "min_"] 


    def __init__(self):
        # datetime_str = "2025-03-10 14:00:00"
        # self.current_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        # self.current_time = now()
        self.statistic_handler = StatisticHandler()


    def get_bridge_report(self, bridge: Bridge, end_date: datetime, report_type: str, with_trend: bool= False):
        """
        Get the last day's statistics report for a specific bridge   
        """

        features_dict = self.get_filtered_fields_and_main_features(is_sensor= False)

        # Query specific table with filtered features of sensors grouped by location
        analysis_report_repo = AnalysisReportRepository(end_date, report_type)
        query_results = analysis_report_repo.get_bridge_query_result(bridge, features_dict)

        if (not query_results):
            report_type = "last_month"
            analysis_report_repo.set_report_type(report_type)
            query_results = analysis_report_repo.get_bridge_query_result(bridge, features_dict)
        
        
        # Get bridge result dict 
        result_dict = self.generate_features_report(list(query_results), features_dict["main_features"], with_trend)
        if (with_trend):
            result_dict = AnalysisReportJSONFormatter.insert_time_to_alert_and_move_index_for_bridge(bridge, result_dict)
                
        
        return result_dict

        
    def get_sensor_report(self, bridge: Bridge, sensors: list, end_date: datetime, report_type: str, with_trend: bool= False):
        """
        Get the last day's statistics report for a specific bridge and its own sensors.        
        """

        # Group sensors by sensor location
        sensors_by_location = dict()
        for sensor in sensors:
            sensors_by_location.setdefault(sensor.sensor_location, []).append(sensor)

        analysis_report_repo = AnalysisReportRepository(end_date, report_type)
        
        # Get sensor result dict list
        sensor_result_list = list()
        for location, sensors in sensors_by_location.items():
            # Get filtered features by every sensor's location
            features_dict = self.get_filtered_fields_and_main_features(is_sensor= True, location= location)

            # For each sensor in speicifc group (lcation)
            for sensor in sensors:
                sensor_id = sensor.sensor
                print("感測器 : ", sensor_id)
                detailed_location = sensor.detailed_location
                # Query specific table with filtered features of sensors grouped by location
                query_results = analysis_report_repo.get_sensor_query_result(bridge, sensor_id, features_dict)

                if (not query_results):
                    report_type = "last_month"
                    analysis_report_repo.set_report_type(report_type)
                    query_results = analysis_report_repo.get_sensor_query_result(bridge, sensor_id, features_dict)
                    if (not query_results):
                        continue

                # print(query_results)

                result_dict = self.generate_features_report(query_results, features_dict["main_features"], with_trend)
                result_dict["detailed_location"] = detailed_location
                result_dict["sensor_location"] = location
                # Get alert, result messages with JSONFormatter
                result_dict = AnalysisReportJSONFormatter.insert_alert_mesage_and_result_message(sensor, result_dict)
                print("異常訊息在此!!!: ", result_dict["health"]["alert_message"])

                if (with_trend):
                    result_dict = AnalysisReportJSONFormatter.insert_time_to_alert_and_move_index_for_sensor(sensor, result_dict)
                
                sensor_result_list.append(result_dict)

                # print(result_dict)

        return sensor_result_list

    
    def generate_features_report(self, query_results: list, features: list, with_trend: bool= False) -> dict:
        """
        Generate features report with 3 conditions:
        1. if column feature of sensor is load_carry_capacity etc.
            -> unify these features with sensor_feature
            -> add trend properties
        2. if column feature is health:
            -> add trend properties
        3. otherwise:
            -> create origin feature reports
        """
        
        result_dict = dict()

        for feature in features:
            if (feature == "load_carry_capacity") or (feature == "cable_force") or (feature == "effective_length"):
                result_dict["sensor_feature"] = self.statistic_handler.get_statistics_feature_report(query_results, feature, self.image_index, with_trend)
            elif (feature == "health"):
                result_dict[feature] = self.statistic_handler.get_statistics_feature_report(query_results, feature, self.image_index, with_trend)
            else:
                result_dict[feature] = self.statistic_handler.get_statistics_feature_report(query_results, feature, self.image_index)
            self.image_index += 1
        return result_dict
    

    def get_filtered_fields_and_main_features(self, is_sensor: bool, location: str= None):
        """
        Get all fields that contain specific prefixes & suffixes.
        Return suffixes list and filtered features list as dictionary.
        """
        suffixes = ["seismic", "centroid_frequency", "damping_ratio", "health"]
        # format features dictionary which contains suffixes and filtered_features in statistic table
        features_dict = dict()
        # Check if it's statistic of sensor, otherwise it's for bridge
        if (is_sensor):
            # add suffix which depends on sensor_location
            if (location == "deck"):
                sensor_feature = "load_carry_capacity"
            elif (location == "cable"):
                sensor_feature = "cable_force"
            elif (location == "pier"):
                sensor_feature = "effective_length"
            else :
                raise ValueError("Invallid sensor type!!")
            features_dict["sensor_feature"] = sensor_feature
            # Insert sensor feature before health
            health_index = suffixes.index("health")
            suffixes.insert(health_index, sensor_feature)


        minute_features = [field.name for field in StructureMinuteHistoryData._meta.get_fields()]
        filtered_features = [feature for feature in minute_features 
                             if any(feature.startswith(prefix) for prefix in self.prefixes) and 
                                any(feature.endswith(suffix) for suffix in suffixes)]
        

        if (self.additional_features):
            filtered_features.extend(self.additional_features)
        
        
        features_dict["main_features"] = suffixes
        features_dict["filtered_features"] = filtered_features

        return features_dict
    
    