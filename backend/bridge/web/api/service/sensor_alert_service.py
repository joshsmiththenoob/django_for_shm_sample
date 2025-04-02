from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.sensor_alert_serializer import SensorAlertSerializer
from web.models import Sensor, MinuteHistoryData, Bridge, AuthAgencyBridges
from datetime import datetime, timedelta
from django.db.models import OuterRef, Subquery, Q


"""
The rule of Reponse Body structure:
{
    "success"(boolean): if client get response successful or not
    "message"(string):  message detail
    "data"(any): return data
}

"""

class SensorAlertService:
    serializer_class = SensorAlertSerializer
    def __init__(self):
        datetime_str = "2025-03-10 14:00:00"
        self.current_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        # self.current_time = now()
    def get(self, request):
        # form json     
        user = request.user

        if (user.is_superuser):
            # 超級使用者可看到所有未刪除的 bridge
            bridge_objects = Bridge.objects.filter(deleted=0)
            bridge_ids = bridge_objects.values_list('id', flat=True)
        else:
            # 一般使用者透過 AuthAgencyBridges 查詢所屬 bridge
            bridge_ids = AuthAgencyBridges.objects.filter(
                agency__authagencyusers__user=user,
                bridge__deleted=0
                ).values_list('bridge_id', flat=True).distinct()
            
        try:
            sensor_connection_errors = self.__get_sensor_connection_errors(bridge_ids)
            sensor_health_errors = self.__get_sensor_health_errors(bridge_ids)

            data = dict()
            data["connection_errors"] = sensor_connection_errors
            data["health_errors"] = sensor_health_errors

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

    def __get_end_time(self, current_time):
        return current_time - timedelta(minutes=2)
    
    def __get_sensor_connection_errors(self, bridge_ids):
        """
        Retrieves a list of sensors that are currently in an error state (current_status=2) 
        and have not been deleted (deleted=0).

        """
        sensor_list = list(Sensor.objects.filter(~Q(current_status=0), deleted=0, bid__in=bridge_ids).values("bid", "sensor", "detailed_location", "image_x", "image_y", "current_status"))

        data = {
            'sensor_list': self.__format_image_corrdinate(sensor_list),
            'sensor_count': len(sensor_list)
        }
        
        return data

    def __get_sensor_health_errors(self, bridge_ids, health_threshold: int=80):
        """
        Retrieves sensor health data where mid_health exceeds the given threshold.

        """
        two_minutes_ago = self.__get_end_time(self.current_time)

        sensor_filtered = Sensor.objects.filter(current_status=0, deleted=0, bid__in=bridge_ids)

        sensor_features = [
            'bid', 'sensor', 'mid_health', 'type', 'ip', 'sensor_location', 'detailed_location', 
            'cable_mass_per_length', 'cable_length', 'elasticity',
            'inertia', 'mass', 'health_alert_index', 'health_move_index',
            'event_alert_index', 'event_move_index', 'bridge_alert_index',
            'bridge_move_index', 'image_x', 'image_y'
            ]

        annotations = {'mid_health': Subquery(MinuteHistoryData.objects.filter(mid_health__lt=health_threshold, time__gt=two_minutes_ago, time__lt=self.current_time, bid=OuterRef('bid'), sensor=OuterRef('sensor')).values('mid_health')[:1])}
        
        sensor_list = list(sensor_filtered.annotate(**annotations).filter(~Q(mid_health=0)).values(*sensor_features))
        data = {
            'sensor_list': self.__format_image_corrdinate(sensor_list),
            'sensor_count': len(sensor_list)
        }

        return data
    
    def __format_image_corrdinate(self, sensor_list: list):
        """
        format "image_coordinate": { "x": 47, "y": 36 }
        """
        for sensor in sensor_list:
            sensor["image_coordinate"] = {
                "x": sensor.pop("image_x", None), 
                "y": sensor.pop("image_y", None)  
            }

        return sensor_list