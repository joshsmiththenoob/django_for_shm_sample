from rest_framework import serializers
from web.api.serializer.shared.image_serializer import ImageSerializer

class SensorCategorySerializer(serializers.Serializer):
    type =  serializers.CharField(max_length=20, allow_null= True, required= False)
    count = serializers.IntegerField(allow_null= True, required= False)




class SensorConceptSerializer(serializers.Serializer):
    total_count = serializers.IntegerField(allow_null= True, required= False)
    cable = serializers.IntegerField(required= False)
    deck = serializers.IntegerField(required= False)
    pier = serializers.IntegerField(required= False)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["totalCount"] = representation.pop("total_count")
        
        return representation


class SensorSerializer(serializers.Serializer):
    detailed_location = serializers.CharField(max_length=20, allow_null= True, required= False)
    sensor_location = serializers.CharField(max_length=20, allow_null= True, required= False)
    ip = serializers.CharField(max_length=20, allow_null= True, required= False)
    cable_mass_per_length = serializers.FloatField(allow_null= True, required= False)
    cable_length = serializers.FloatField(allow_null= True, required= False)
    elasticity = serializers.FloatField(allow_null= True, required= False)
    inertia = serializers.FloatField(allow_null= True, required= False)
    mass = serializers.FloatField(allow_null= True, required= False)
    span = serializers.FloatField(allow_null= True, help_text="跨距")
    nearest_pier_distance = serializers.FloatField(allow_null= True, help_text="最近橋柱距離")
    health_alert_index = serializers.IntegerField(allow_null= True, required= False)
    health_move_index = serializers.IntegerField(allow_null= True, required= False)
    event_alert_index = serializers.IntegerField(allow_null= True, required= False)
    event_move_index = serializers.IntegerField(allow_null= True, required= False)
    sensor_location_image = ImageSerializer(required= False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modify key from representation json
        representation["sensorLocation"] = representation.pop("sensor_location")
        representation["detailedLocation"] = representation.pop("detailed_location")
        representation["cableMassPerLength"] = representation.pop("cable_mass_per_length")
        representation["cableLength"] = representation.pop("cable_length")
        representation["nearestPierDistance"] = representation.pop("nearest_pier_distance")
        representation["healthAlertIndex"] = representation.pop("health_alert_index")
        representation["healthMoveIndex"] = representation.pop("health_move_index")
        representation["eventAlertIndex"] = representation.pop("event_alert_index")
        representation["eventMoveIndex"] = representation.pop("event_move_index")
        representation["sensorLocationImage"] = representation.pop("sensor_location_image")

        return representation
    
    


class SensorReportBasicDataSerializer(serializers.Serializer):
    sensor_concept = SensorConceptSerializer()
    sensor_list = SensorSerializer(many= True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modify key from representation json
        representation["sensorList"] = representation.pop("sensor_list")
        representation["sensorConcept"] = representation.pop("sensor_concept")

        return representation