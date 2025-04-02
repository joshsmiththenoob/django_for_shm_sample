from rest_framework import serializers
from web.api.serializer.shared.feature_serializer import FeatureReportSerializer, FeatureSerializer
from bridge.utils.camel_case_serializer_mixin import CamelCaseSerializerMixin


class BridgeReportMonthDataSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    seismic = FeatureSerializer()
    centroid_frequency = FeatureReportSerializer()
    damping_ratio = FeatureReportSerializer()
    health = FeatureReportSerializer()
    

