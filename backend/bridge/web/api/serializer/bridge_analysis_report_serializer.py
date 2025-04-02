# Only represent chapter serializer which import the common serializers in shared folder

from rest_framework import serializers
from drf_yasg import openapi
from web.api.serializer.shared.image_serializer import ImageSerializer
from web.api.serializer.shared.sensor_report_basic_data_serializer import SensorReportBasicDataSerializer
from web.api.serializer.shared.bridge_report_second_data_serializer import BridgeReportSecondDataSerializer
from web.api.serializer.shared.sensor_report_second_data_serializer import SensorReportSecondDataSerializer
from web.api.serializer.shared.sensor_report_month_data_serializer import SensorReportMonthDataSerializer
from web.api.serializer.shared.bridge_report_month_data_serializer import BridgeReportMonthDataSerializer
from web.api.serializer.shared.report_event_data_serializer import ReportEventDataSerializer, EarthquakeTableSerializer, TyphoonTableSerializer
from bridge.utils.camel_case_serializer_mixin import CamelCaseSerializerMixin


############################   Chapter Data Report###########################################

class ReportBasicDataReportSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    agency_name = serializers.CharField(max_length=20)
    report_name = serializers.CharField(max_length=50)
    user_company = serializers.CharField(max_length=50)
    now_date = serializers.CharField(max_length=20)
    event_list_date = serializers.CharField(max_length=20)
    bridge_name = serializers.CharField(max_length=20)
    area = serializers.CharField(max_length=20)
    bridge_maintenance_record = serializers.CharField(required= False, default= "橋長為200 公尺，111年1月26日竣工後通車，近一次工程紀錄為114年1月底的維修紀錄。") 
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    bridge_location_image = ImageSerializer(allow_null=True)
    sensor_data = SensorReportBasicDataSerializer(allow_null=True)

    

class ReportSecondDataSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    last_date = serializers.CharField(max_length=20)
    temperature = serializers.FloatField()
    wind_speed = serializers.FloatField()
    wind_direction = serializers.IntegerField()
    bridge_data = BridgeReportSecondDataSerializer()
    sensor_data = SensorReportSecondDataSerializer(many= True)




class ReportMonthDataSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    start_date = serializers.CharField(max_length=20)
    end_date = serializers.CharField(max_length=20)
    bridge_data = BridgeReportMonthDataSerializer()
    sensor_data = SensorReportMonthDataSerializer(many= True)


class ReportEarthquakeDataSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    earthquake_table = EarthquakeTableSerializer(many=True, allow_null= True)
    earthquake_id = serializers.IntegerField(allow_null=True)
    earthquake_report = ImageSerializer(required= False, allow_null=True)
    earthquake_rank = serializers.FloatField(allow_null=True)
    bridge_data = ReportEventDataSerializer()
    sensor_data = ReportEventDataSerializer(many=True)


class ReportTyphoonDataSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    typhoon_table = TyphoonTableSerializer(many=True, allow_null= True)
    typhoon_name = serializers.CharField(max_length=20, allow_null=True)
    typhoon_id = serializers.IntegerField(allow_null=True)
    typhoon_report = ImageSerializer(allow_null=True)
    typhoon_rank = serializers.CharField(allow_null=True)
    bridge_data = ReportEventDataSerializer()
    sensor_data = ReportEventDataSerializer(many=True)


class BridgeAnalysisReportSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    report_basic_data = ReportBasicDataReportSerializer()
    report_second_data = ReportSecondDataSerializer()
    report_month_data = ReportMonthDataSerializer()
    report_year_data = ReportMonthDataSerializer()
    report_earthquake_data = ReportEarthquakeDataSerializer(required= False, allow_null=True)
    report_typhoon_data = ReportTyphoonDataSerializer(required= False, allow_null=True)
    conversation = serializers.CharField(required= False, allow_null=True)
    

    class Meta:
        query_params = [
            openapi.Parameter(
                name = "report-month",
                in_ = openapi.IN_QUERY,
                description = "製作分析報告時間點，例如: '2025-02'",
                type = openapi.TYPE_STRING,
                default = "2025-02",
                required= True
            ),
        ]
