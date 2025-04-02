from rest_framework import serializers
from drf_yasg import openapi

from rest_framework import serializers


class QSerializer(serializers.Serializer):
    title = serializers.CharField()
    Q1 = serializers.ListField(
        child=serializers.FloatField(allow_null=True),  
        allow_empty=True  
    )
    Q2 = serializers.ListField(
        child=serializers.FloatField(allow_null=True),  
        allow_empty=True  
    )
    Q3 = serializers.ListField(
        child=serializers.FloatField(allow_null=True),  
        allow_empty=True  
    )
    fit_curve = serializers.ListField(
        child=serializers.FloatField(allow_null=True),  
        allow_empty=True  
    )
    latest_data = serializers.FloatField(allow_null=True)
    slope = serializers.FloatField(allow_null=True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["latestData"] = representation.pop("latest_data")
        representation["fitCurve"] = representation.pop("fit_curve")
        
        return representation

class SensorHistorySerializer(serializers.Serializer):
    time = serializers.ListField(
        child = serializers.DateTimeField(),
        required= True
    )
    result = QSerializer(many= True, required= True)

    weather_result = QSerializer(many= True, required= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["weatherResult"] = representation.pop("weather_result")
        
        return representation


    class Meta:
        query_params = [
            openapi.Parameter(
                name = "start",
                in_ = openapi.IN_QUERY,
                description = "開始時間，例如: '2024-10-25T12:00:00'",
                type = openapi.TYPE_STRING,
                default = "2024-12-24T00:00:00",
                required= True
            ),
            openapi.Parameter(
                name = "end",
                in_ = openapi.IN_QUERY,
                description = "結束時間，例如: '2024-10-25T24:00:00'，如有開始時間，該值需要大於開始時間",
                type = openapi.TYPE_STRING,
                    default = "2025-01-07T00:00:00",
                required= True
            )
        ]