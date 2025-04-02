#     Deal with 3st Chapter of Analysis Report
import os
import time
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.request import Request
from web.models import Bridge, Sensor, Agency, StructureMinuteHistoryData, WeatherDailyHistoryData, MinuteHistoryData, StructureEarthquakeEvent, StructureMinuteHistoryData, Earthquake, EarthquakeEvent, StructureTyphoonEvent, Typhoon, TyphoonEvent
from web.api.handler.statistic_handler import StatisticHandler
from web.api.handler.date_handler import DateHandler
from web.api.handler.image_handler import ImageHandler
from web.api.handler.analysis_report.analysis_report_json_formatter import AnalysisReportJSONFormatter
from django.db.models import Prefetch
from django.contrib.auth.models import User   
from web.api.handler.analysis_report.analysis_report_json_formatter import AnalysisReportJSONFormatter
from django.db.models import OuterRef, Subquery
from web.api.handler.chart_drawer import ChartDrawer



class TyphoonReportHandler: 

    def __init__(self, image_index):
        self.image_index = image_index
        self.__date_handler = DateHandler()
        self.__img_handler = ImageHandler()
        self.__chart_drawer = ChartDrawer()

    def get_report(self, user: User, bid: int, date: datetime):
        return  self.__get_latest_events_report (user, bid, date)
    
    def get_current_image_index(self):
        return self.image_index

    def __get_bridge_informations_for_user (self, user: User, bid: int, date: datetime):

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
    
    def __get_latest_events_report (self, user: User, bid: int, date: datetime):

        bridge, sensors, date = self.__get_bridge_informations_for_user(user, bid, date)   
        result_dict, event_query = self.get_event_report(bid, date)

        if bool(event_query) == False:
            
            return None
        
        else:
            event_dict = dict()
            event_dict['year'] = result_dict['year']
            event_dict['month'] = result_dict['month'] 
            event_dict['typhoon_table'] = result_dict['typhoon_table']
            event_dict['typhoon_name'] = result_dict['typhoon_name']
            event_dict['typhoon_id'] = result_dict['typhoon_id']
            event_dict['typhoon_report'] = result_dict['typhoon_report']
            event_dict['typhoon_rank'] = result_dict['typhoon_rank']
            event_dict['bridge_data'] = self.get_bridge_report(bid, event_query, bridge)
            event_dict['sensor_data'] = self.get_sensor_report(bid, event_query, sensors)
            print(event_dict['typhoon_rank'])
            return event_dict

    def get_event_report(self, bid: int, date: datetime):
        event_query = StructureTyphoonEvent.objects.filter(bid=bid, time_marker='during', start_time__month=date.month).order_by('-start_time')

        if bool(event_query) == False:
            event_query = ""
            result_dict = ""

            return result_dict, event_query

        event_list = event_query.annotate(
                cht_name=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('cht_name')[:1]),
                eng_name=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('eng_name')[:1]),  
                max_intensity=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('max_intensity')[:1]),
                warning_count=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('warning_count')[:1]),
                track_base64=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('track_base64')[:1]),
                information_base64=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('information_base64')[:1]),
            )

        base64_chart = event_list.values_list('information_base64', flat=True).first()
        information_img_dict = AnalysisReportJSONFormatter.get_image_info_dict(base64_chart, self.image_index)
        table_list = event_list.values('event_id', 'start_time', 'end_time', 'cht_name', 'eng_name', 'max_intensity', 'warning_count', 'track_base64', 'information_base64')
        table = AnalysisReportJSONFormatter.get_event_table_list(table_list, "typhoon")

        result_dict = dict()
        result_dict['year'] = date.year
        result_dict['month'] = date.month
        result_dict['typhoon_table'] = table
        result_dict['typhoon_name'] = event_list.values_list('cht_name', flat=True).first()
        result_dict['typhoon_id'] = event_list.values_list('event_id', flat=True).first()
        result_dict['typhoon_report'] = information_img_dict
        self.image_index += 1
        result_dict['typhoon_rank'] = event_list.values_list('max_intensity', flat=True).first()

        print(result_dict['typhoon_id'])
        print(result_dict['typhoon_rank'])

        return result_dict, event_query
        
    def get_bridge_report(self, bid: int, event_query, bridge):
        event_latest = event_query.first()
        f_min = event_latest.min_seismic
        f_max = event_latest.max_seismic
        f_ratio = f_max/f_min
        Q3 = event_latest.up_centroid_frequency
        Q1 = event_latest.down_centroid_frequency
        Q_ratio = Q1/Q3

        # 前後五分鐘資料
        event_date_time = datetime.strptime("2025-02-14 05:30:00", "%Y-%m-%d %H:%M:%S")
        # start_time, end_time = self.__date_handler.get_event_time_range(event_latest.start_time)
        start_time, end_time = self.__date_handler.get_event_time_range(event_date_time)
        event_data = StructureMinuteHistoryData.objects.filter(bid=bid, time__range=(start_time, end_time))
        time_data = list(event_data.values_list('time', flat=True))
        mid_seismic_dataset = list(event_data.values_list('mid_seismic', flat=True))
        mid_centroid_frequency_dataset = list(event_data.values_list('mid_centroid_frequency', flat=True))

        event_message = AnalysisReportJSONFormatter.insert_event_alert_mesage_and_result_message(bridge, Q_ratio)

        bridge_dict = dict()
        bridge_dict['seismic'] = {}
        bridge_dict['seismic']['f_min'] = f_min
        bridge_dict['seismic']['f_max'] = f_max
        bridge_dict['seismic']['feature_ratio'] = f_ratio
        bridge_dict['seismic']['chart'] = self.generate_chart_with_base64_and_index(time=time_data, mid_dataset=mid_seismic_dataset, title='seismic')
        bridge_dict['centroid_frequency'] = {}
        bridge_dict['centroid_frequency']['Q3'] = Q3
        bridge_dict['centroid_frequency']['Q1'] = Q1
        bridge_dict['centroid_frequency']['feature_ratio'] = Q_ratio
        bridge_dict['centroid_frequency']['alert_message'] = event_message["alert_message"]
        bridge_dict['centroid_frequency']['result_message'] = event_message["result_message"]
        bridge_dict['centroid_frequency']['chart'] = self.generate_chart_with_base64_and_index(time=time_data, mid_dataset=mid_centroid_frequency_dataset, title='centroid_frequency')

        return bridge_dict

    def get_sensor_report(self, bid: int, event_query, sensors):
        event_latest = event_query.first()
        event_sensors = TyphoonEvent.objects.filter(bid=bid, time_marker='during', event_id=event_latest.event_id)

        # 前後五分鐘資料
        event_date_time = datetime.strptime("2025-02-14 05:30:00", "%Y-%m-%d %H:%M:%S")
        start_time, end_time = self.__date_handler.get_event_time_range(event_date_time)
        # start_time, end_time = self.__date_handler.get_event_time_range(event_latest.start_time)
        event_data = MinuteHistoryData.objects.filter(bid=bid, time__range=(start_time, end_time))
        time_data = list(event_data.values_list('time', flat=True).distinct())

        sensor_list = list()
        count = 0
        for sensor in event_sensors:
            mid_seismic_dataset = list(event_data.filter(sensor=sensor.sensor).values_list('mid_seismic', flat=True))
            mid_centroid_frequency_dataset = list(event_data.filter(sensor=sensor.sensor).values_list('mid_centroid_frequency', flat=True))

            sensor_info = sensors.filter(sensor=sensor.sensor).first()
            event_message = AnalysisReportJSONFormatter.insert_event_alert_mesage_and_result_message(sensor_info, sensor.down_centroid_frequency/sensor.up_centroid_frequency)   

            sensor_dict = {
                "detailed_location": sensor_info.detailed_location,
                "sensor_location": sensor_info.sensor_location,
                'seismic': {
                    'f_min': sensor.min_seismic,
                    'f_max': sensor.max_seismic,
                    'feature_ratio': sensor.max_seismic/sensor.min_seismic,
                    'chart': self.generate_chart_with_base64_and_index(time=time_data, mid_dataset=mid_seismic_dataset, title='seismic'),
                },
                'centroid_frequency': {
                    'Q3': sensor.up_centroid_frequency,
                    'Q1': sensor.down_centroid_frequency,
                    'feature_ratio': sensor.down_centroid_frequency/sensor.up_centroid_frequency,
                    'alert_message': event_message["alert_message"],
                    'result_message': event_message["result_message"],
                    'chart': self.generate_chart_with_base64_and_index(time=time_data, mid_dataset=mid_centroid_frequency_dataset, title='centroid_frequency')
                }
            }

            # sensor_list.append({f'{count}': sensor_dict})
            sensor_list.append(sensor_dict)
            count += 1

        return sensor_list
    
    def generate_chart_with_base64_and_index(self, time: list, mid_dataset: list, title: str):
        up_dataset = []
        down_dataset = []
        base64_chart = self.__chart_drawer.get_statistic_line_chart_base64(time=time, up_dataset=up_dataset, mid_dataset=mid_dataset, down_dataset=down_dataset, title=title)
        chart_dict = AnalysisReportJSONFormatter.get_image_info_dict(base64_chart, self.image_index)
        self.image_index += 1

        return chart_dict
    

