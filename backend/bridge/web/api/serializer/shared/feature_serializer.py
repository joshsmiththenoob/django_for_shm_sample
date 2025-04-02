from rest_framework import serializers
from web.api.serializer.shared.image_serializer import ImageSerializer
from bridge.utils.camel_case_serializer_mixin import CamelCaseSerializerMixin


class FeatureSerializer(serializers.Serializer):
    Q2 = serializers.FloatField()
    Q4 = serializers.FloatField()
    Q0 = serializers.FloatField()
    chart = ImageSerializer()


class FeatureReportSerializer(CamelCaseSerializerMixin, FeatureSerializer):
    variation =  serializers.CharField()
    alert_message = serializers.CharField(required=False)
    result_message = serializers.CharField(required=False)
    slope = serializers.FloatField(required=False)
    latest_value = serializers.FloatField(required=False)
    time_to_alert_index = serializers.FloatField(required=False)
    time_to_move_index = serializers.FloatField(required=False)