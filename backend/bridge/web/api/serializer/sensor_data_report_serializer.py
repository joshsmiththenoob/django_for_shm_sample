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
    latest_data = serializers.FloatField(allow_null=True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["latestData"] = representation.pop("latest_data")
        
        return representation

class TimeSegmentSensorDataSerializer(serializers.Serializer):
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



class SensorDataReportSerializer(serializers.Serializer):
    hours = TimeSegmentSensorDataSerializer(allow_null=True)
    minutes = TimeSegmentSensorDataSerializer(allow_null=True)