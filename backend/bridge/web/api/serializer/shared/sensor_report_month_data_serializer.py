from rest_framework import serializers
from web.api.serializer.shared.feature_serializer import FeatureReportSerializer, FeatureSerializer
from bridge.utils.camel_case_serializer_mixin import CamelCaseSerializerMixin


class SensorReportMonthDataSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    detailed_location = serializers.CharField(max_length= 20)
    sensor_location = serializers.CharField(max_length= 20)
    seismic = FeatureSerializer()
    centroid_frequency = FeatureReportSerializer()
    damping_ratio = FeatureReportSerializer()
    health = FeatureReportSerializer()
    sensor_feature = FeatureReportSerializer()
