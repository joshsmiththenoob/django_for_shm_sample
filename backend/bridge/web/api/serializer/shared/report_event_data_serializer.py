from rest_framework import serializers
from bridge.utils.camel_case_serializer_mixin import CamelCaseSerializerMixin
from web.api.serializer.shared.image_serializer import ImageSerializer

class seismicSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    f_min = serializers.FloatField(allow_null=True)
    f_max = serializers.FloatField(allow_null=True)
    feature_ratio = serializers.FloatField(allow_null=True)
    chart = ImageSerializer(allow_null=True)

class centroid_frequencySerializer(CamelCaseSerializerMixin, serializers.Serializer):
    Q3 = serializers.FloatField(allow_null=True)
    Q1 = serializers.FloatField(allow_null=True)
    feature_ratio = serializers.FloatField(allow_null=True)
    alert_message = serializers.CharField(allow_null=True)
    result_message = serializers.CharField(allow_null=True)
    chart = ImageSerializer(allow_null=True)

class ReportEventDataSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    detailed_location = serializers.CharField(required= False)
    sensor_location = serializers.CharField(required= False)
    seismic = seismicSerializer(required= False, allow_null=True)
    centroid_frequency = centroid_frequencySerializer(required= False,allow_null=True)


class EarthquakeTableSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    earthquake_id = serializers.CharField(allow_null=True)
    start_time = serializers.CharField(allow_null=True)
    end_time = serializers.CharField(allow_null=True)

class TyphoonTableSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    cht_name = serializers.CharField(allow_null=True)
    start_time = serializers.CharField(allow_null=True)
    end_time = serializers.CharField(allow_null=True)
