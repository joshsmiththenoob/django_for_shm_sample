from web.models import Sensor, Bridge, Agency, StructureMinuteHistoryData, WeatherDailyHistoryData, MinuteHistoryData
import time
class AnalysisReportJSONFormatter:
    @staticmethod
    def get_image_info_dict(base64: str, image_index: int):
        image_info_dict = dict()
        image_info_dict["index"] = image_index
        image_info_dict["base64"] = base64
        
        return image_info_dict
    

    @staticmethod
    def insert_alert_mesage_and_result_message(sensor: Sensor, features_report: dict,):
        """
        Get interpretation to check if value of specific features is below or above the move index and alert index
        args:
            sensor: ORM object, to get information of individual sensor
            sensor_feature_name: specfic feature mapped by sensor location
            features_report: the report of sensor which recrod statistic data in prior
        """

        health_q1 = features_report.get("health", {}).get("Q1")
        feature_q1 = features_report.get("sensor_feature", {}).get("Q1")

        # get health alert message
        if (health_q1 > sensor.health_alert_index):
            health_alert_message = str(health_q1) + "高於" + f"告警值({sensor.health_alert_index})"
            health_result_message = "良好，建議維持現有監測頻率"
        elif (health_q1 < sensor.health_alert_index) and (health_q1 > sensor.health_move_index):
            health_alert_message = str(health_q1) + "低於" + f"告警值({sensor.health_alert_index})"
            health_result_message = "需警界，橋梁狀態需密集關注"
        elif (health_q1 < sensor.health_move_index):
            health_alert_message = str(health_q1) + "低於" + f"告警值({sensor.health_alert_index})"
            health_result_message = "須採取管制行動，建議請專業技師評估補強之必要"
        else:
            raise Exception


        # get sensor feature alert message
        if (feature_q1 > sensor.bridge_alert_index):
            sensor_alert_message = str(feature_q1) + "高於"  + f"告警值({sensor.bridge_alert_index})"
            sensor_result_message = "未有異常"
        elif (feature_q1 < sensor.bridge_alert_index) and (feature_q1 > sensor.bridge_move_index):
            sensor_alert_message = str(feature_q1) + "低於"  + f"告警值({sensor.bridge_alert_index})"
            sensor_result_message = "些微異常"
        elif (feature_q1 < sensor.bridge_move_index):
            sensor_alert_message = str(feature_q1) + "低於" + f"告警值({sensor.bridge_alert_index})"
            sensor_result_message = "異常"
        
        

        # insert alert messages into feature_report
        features_report["health"]["alert_message"] = health_alert_message
        features_report["health"]["result_message"] = health_result_message
        features_report["sensor_feature"]["alert_message"] = sensor_alert_message
        features_report["sensor_feature"]["result_message"] = sensor_result_message


        return features_report
    

    @staticmethod
    def insert_event_alert_mesage_and_result_message(object: object,  ratio: float):

        # get health alert message
        if (ratio > object.event_alert_index):
            health_alert_message = str(ratio) + "高於" + f"告警值({object.event_alert_index})"
            health_result_message = "良好，建議維持現有監測頻率"
        elif (ratio < object.event_alert_index) and (ratio > object.event_move_index):
            health_alert_message = str(ratio) + "低於" + f"告警值({object.event_alert_index})"
            health_result_message = "需警界，橋梁狀態需密集關注"
        elif (ratio < object.event_move_index):
            health_alert_message = str(ratio) + "低於" + f"告警值({object.event_alert_index})"
            health_result_message = "須採取管制行動，建議請專業技師評估補強之必要"
        else:
            raise Exception
        
        # insert alert messages into feature_report
        event_message = dict()
        event_message["alert_message"] = health_alert_message
        event_message["result_message"] = health_result_message

        return event_message
    def insert_time_to_alert_and_move_index_for_sensor(sensor: Sensor, features_report: dict):
        """
        Get interpretation to check if value of specific features is below or above the move index and alert index
        args:
            sensor: ORM object, to get information of individual sensor
            sensor_feature_name: specfic feature mapped by sensor location
            features_report: the report of sensor which recrod statistic data in prior
        """
        health_slope = features_report.get("health", {}).get("slope")
        health_latest_value = features_report.get("health", {}).get("latest_value")
        time_to_health_alert_index = (health_latest_value - sensor.health_alert_index) / abs(health_slope) 
        time_to_health_move_index = (health_latest_value - sensor.health_move_index) / abs(health_slope)  

        features_report["health"]["time_to_alert_index"] = int(time_to_health_alert_index) if (time_to_health_alert_index > 0) else 0
        features_report["health"]["time_to_move_index"] = int(time_to_health_move_index) if (time_to_health_move_index > 0) else 0

        feature_slope = features_report.get("sensor_feature", {}).get("slope")
        feature_latest_value = features_report.get("sensor_feature", {}).get("latest_value")
        
        time_to_feature_alert_index = (feature_latest_value - sensor.bridge_alert_index) / abs(feature_slope) 
        time_to_feature_move_index = (feature_latest_value - sensor.bridge_move_index) / abs(feature_slope)  

        features_report["sensor_feature"]["time_to_alert_index"] = int(time_to_feature_alert_index) if (time_to_feature_alert_index > 0) else 0
        features_report["sensor_feature"]["time_to_move_index"] = int(time_to_feature_move_index) if (time_to_feature_move_index > 0) else 0

        return features_report
    

    def insert_time_to_alert_and_move_index_for_bridge(bridge: Bridge, features_report: dict, is_sensor: bool= False):
        """
        Get interpretation to check if value of specific features is below or above the move index and alert index
        args:
            sensor: ORM object, to get information of individual sensor
            sensor_feature_name: specfic feature mapped by sensor location
            features_report: the report of sensor which recrod statistic data in prior
        """
        health_slope = features_report.get("health", {}).get("slope")
        health_latest_value = features_report.get("health", {}).get("latest_value")
        time_to_health_alert_index = (health_latest_value - bridge.health_alert_index) / abs(health_slope) 
        time_to_health_move_index = (health_latest_value - bridge.health_move_index) / abs(health_slope)  

        features_report["health"]["time_to_alert_index"] = int(time_to_health_alert_index) if (time_to_health_alert_index > 0) else 0
        features_report["health"]["time_to_move_index"] = int(time_to_health_move_index) if (time_to_health_move_index > 0) else 0

        return features_report


    def get_event_table_list(event_dataset: list, title: str = None):
        event_table_list = list()
        
        if (title == "earthquake"):
            
            for e in event_dataset:
                event_row_dict = dict()
                # start_time = e.origintime
                # end_time = e.origintime + timedelta(minutes=2)
                start_time = e['start_time']
                end_time = e['end_time']
                event_row_dict["earthquake_id"] = e['event_id']
                event_row_dict["start_time"] = start_time.strftime("%Y-%m-%d %H:%M:%S")
                event_row_dict["end_time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
                event_table_list.append(event_row_dict)


        elif (title == "typhoon"):
            for t in event_dataset:
                event_row_dict = dict()
                # start_time = e.origintime
                # end_time = e.origintime + timedelta(minutes=2)
                start_time = t['start_time']
                end_time = t['end_time']
                event_row_dict["cht_name"] = t['cht_name']
                event_row_dict["start_time"] = start_time.strftime("%Y-%m-%d %H:%M:%S")
                event_row_dict["end_time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
                event_table_list.append(event_row_dict)

        return event_table_list