from rest_framework import serializers
from web.models import Sensor
from drf_yasg import openapi

class SensorNameSerializer(serializers.Serializer):

    
    bid = serializers.IntegerField()
    sensor = serializers.IntegerField()
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
    image_x = serializers.FloatField(allow_null=True)
    image_y = serializers.FloatField(allow_null=True)
    current_status = serializers.ImageField(default=2)
    deleted = serializers.IntegerField(default=0) 

    def create(self, validated_data):
        new_sensor = Sensor.objects.create(**validated_data) # unpack validated_data:dict 

        return new_sensor


    def update(self, instance, validated_data: dict): # validated_data is dict
        """
        instance: the old value of record
        validated_data: the new value of record
        """
        # get value of key and replace it to the existed value
        instance.bid = validated_data.get("bid", instance.bid)
        instance.sensor = validated_data.get("sensor", instance.sensor)
        instance.type = validated_data.get("type", instance.type)
        instance.ip = validated_data.get("ip", instance.ip)
        instance.sensor_location = validated_data.get("sensor_location", instance.sensor_location)
        instance.detailed_location = validated_data.get("detailed_location", instance.detailed_location)
        instance.cable_mass_per_length = validated_data.get("cable_mass_per_length", instance.cable_mass_per_length)
        instance.cable_length = validated_data.get("cable_length", instance.cable_length)
        instance.elasticity = validated_data.get("elasticity", instance.elasticity)
        instance.inertia = validated_data.get("inertia", instance.inertia)
        instance.mass = validated_data.get("mass", instance.mass)
        instance.health_alert_index = validated_data.get("health_alert_index", instance.health_alert_index)
        instance.health_move_index = validated_data.get("health_move_index", instance.health_move_index)
        instance.event_alert_index = validated_data.get("event_alert_index", instance.event_alert_index)
        instance.event_move_index = validated_data.get("event_move_index", instance.event_move_index)
        instance.bridge_alert_index = validated_data.get("bridge_alert_index", instance.bridge_alert_index)
        instance.bridge_move_index = validated_data.get("bridge_move_index", instance.bridge_move_index)
        instance.image_x = validated_data.get("image_x", instance.image_x)
        instance.image_y = validated_data.get("image_y", instance.image_y)
        instance.deleted = validated_data.get("deleted", instance.deleted) # Modify for use with delete method
        instance.save() # update the content of existied data(record) in DB

        return instance


    def to_internal_value(self, data):
        """
        Convert input data (e.g, city -> address_nam) for internal use.
        """
        data["sensor_location"] = data.pop("sensorLocation", None)
        data["detailed_location"] = data.pop("detailedLocation", None)
        data["cable_mass_per_length"] = data.pop("cableMassPerLength", None)
        data["cable_length"] = data.pop("cableLength", None)
        data["health_alert_index"] = data.pop("healthAlertIndex", None)
        data["health_move_index"] = data.pop("healthMoveIndex", None)
        data["event_alert_index"] = data.pop("eventAlertIndex", None)
        data["event_move_index"] = data.pop("eventMoveIndex", None)
        data["bridge_alert_index"] = data.pop("bridgeAlertIndex", None)
        data["bridge_move_index"] = data.pop("bridgeMoveIndex", None)
        image_coordinate = data.pop("imageCoordinate", {})
        data["image_x"] = image_coordinate.get("x")
        data["image_y"] = image_coordinate.get("y")
        
        return super().to_internal_value(data)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modify key from representation json
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
        # 包裝 imageCoordinate
        representation["imageCoordinate"] = {
            "x": representation.pop("image_x"),
            "y": representation.pop("image_y")
        }

        return super().to_representation(instance)
    
    class Meta:

        example = {

            "type": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="感測器類型",
                example="accelerometer",
            ),
            "ip": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="感測器ip",
                example= 43,
            ),
            "sensorLocation": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="構建樣態",
                example= "cable",
            ),
            "detailedLocation": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="安裝位置",
                example= "L-77",
            ),
            "cableMassPerLength": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="鋼索線性密度",
                example= 1.66,
            ),
            "cableLength": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="鋼索長度",
                example= 22.66,
            ),
            "elasticity": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="楊氏模數",
                example= 2.4,
            ),
            "inertia": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="斷面慣性距",
                example= 1.1,
            ),
            "mass": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="質量",
                example= 30.5,
            ),
            "healthAlertIndex": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="安全評估係數警戒值",
                example= 90,
            ),
            "healthMoveIndex": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="安全評估係數行動值",
                example= 85,
            ),
            "eventAlertIndex": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="",
                example= 1,
            ),
            "eventMoveIndex": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="",
                example= 1,
            ),
            "bridgeAlertIndex": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="橋梁警戒值",
                example= 30,
            ),
            "bridgeMoveIndex": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="橋梁行動值",
                example= 40,
            ),
            "imageCoordinate": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="感測器座標",
                properties={
                    "x": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        description="感測器點位X",
                        example=12.3,
                    ),
                    "y": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        description="感測器點位Y",
                        example=4.56,
                    ),
                }
            )
        }