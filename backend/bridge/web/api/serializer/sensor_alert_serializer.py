from rest_framework import serializers

class SensorImageCoordinateSerializer(serializers.Serializer):
    x =  serializers.FloatField(allow_null= True)
    y =  serializers.FloatField(allow_null= True)


class ConnectionErrorsSensorSerializer(serializers.Serializer):
    bid = serializers.IntegerField()
    sensor = serializers.IntegerField()
    detailed_location = serializers.CharField(max_length=20, allow_null=True)
    image_coordinate = SensorImageCoordinateSerializer(allow_null= True)
    current_status = serializers.IntegerField(allow_null= True)


    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["id"] = representation.pop("sensor")
        representation["detailedLocation"] = representation.pop("detailed_location")
        representation["imageCoordinate"] = representation.pop("image_coordinate")
        representation["status"] = representation.pop("current_status")
        return representation

class HealthErrorsSensorSerializer(serializers.Serializer):
    bid = serializers.IntegerField()
    sensor = serializers.IntegerField()
    mid_health = serializers.FloatField()
    type = serializers.CharField(max_length=20, allow_null=True)
    ip = serializers.IntegerField(allow_null=True)
    sensor_location = serializers.CharField(max_length=20, allow_null=True)
    detailed_location = serializers.CharField(max_length=20, allow_null=True)
    cable_mass_per_length = serializers.FloatField(allow_null=True)
    cable_length = serializers.FloatField(allow_null=True)
    elasticity = serializers.FloatField(allow_null=True)
    inertia = serializers.FloatField(allow_null=True)
    mass = serializers.FloatField(allow_null=True)
    health_alert_index = serializers.IntegerField(allow_null=True)
    health_move_index = serializers.IntegerField(allow_null=True)
    event_alert_index = serializers.IntegerField(allow_null=True)
    event_move_index = serializers.IntegerField(allow_null=True)
    bridge_alert_index = serializers.FloatField(allow_null=True)
    bridge_move_index = serializers.FloatField(allow_null=True)
    image_coordinate = SensorImageCoordinateSerializer(allow_null= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["id"] = representation.pop("sensor")
        representation["latestHealth"] = representation.pop("mid_health")
        representation["sensorLocation"] = representation.pop("sensor_location")
        representation["detailedLocation"] = representation.pop("detailed_location")
        representation["cableMassPerLength"] = representation.pop("cable_mass_per_length")
        representation["cableLength"] = representation.pop("cable_length")
        representation["healthAlertIndex"] = representation.pop("health_alert_index")
        representation["healthMoveIndex"] = representation.pop("health_move_index")
        representation["eventAlertIndex"] = representation.pop("event_alert_index")
        representation["eventMoveIndex"] = representation.pop("event_move_index")
        representation["bridgeAlertIndex"] = representation.pop("bridge_alert_index")
        representation["bridgeMoveIndex"] = representation.pop("bridge_move_index")
        representation["imageCoordinate"] = representation.pop("image_coordinate")
        
        return representation

class ConnectionErrorsSerializer(serializers.Serializer):
    sensor_list = serializers.ListField(
        child = ConnectionErrorsSensorSerializer(allow_null=True),
        required= True
    )
    sensor_count = serializers.IntegerField(allow_null=True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["sensorList"] = representation.pop("sensor_list")
        representation["sensorCount"] = representation.pop("sensor_count")
        
        return representation
    
class HealthErrorsSerializer(serializers.Serializer):
    sensor_list = serializers.ListField(
        child = HealthErrorsSensorSerializer(allow_null=True),
        required= True
    )
    sensor_count = serializers.IntegerField(allow_null=True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["sensorList"] = representation.pop("sensor_list")
        representation["sensorCount"] = representation.pop("sensor_count")
        
        return representation

class SensorAlertSerializer(serializers.Serializer):
    connection_errors = ConnectionErrorsSerializer(allow_null=True)
    health_errors = HealthErrorsSerializer(allow_null=True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["connectionErrors"] = representation.pop("connection_errors")
        representation["healthErrors"] = representation.pop("health_errors")
        
        return representation