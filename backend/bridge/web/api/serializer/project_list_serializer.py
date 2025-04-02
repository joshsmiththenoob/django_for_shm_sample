from rest_framework import serializers

class LatestTyphoonConceptSerializer(serializers.Serializer):
    # ty_event_id = serializers.IntegerField(allow_null= True)
    ty_before_after = serializers.FloatField(allow_null= True)
    ty_max_during = serializers.FloatField(allow_null= True)


    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        # representation["id"] = representation.pop("ty_event_id")
        representation["beforeAfter"] = representation.pop("ty_before_after")
        representation["maxDuring"] = representation.pop("ty_max_during")

        return representation



class LatestEarthquakeConceptSerializer(serializers.Serializer):
    # eq_event_id = serializers.IntegerField(allow_null= True)
    eq_before_after = serializers.FloatField(allow_null= True)
    eq_max_during = serializers.FloatField(allow_null= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        # representation["id"] = representation.pop("eq_event_id")
        representation["beforeAfter"] = representation.pop("eq_before_after")
        representation["maxDuring"] = representation.pop("eq_max_during")

        return representation

    
class LatestWeatherDataSerializer(serializers.Serializer):
    precipitation = serializers.FloatField(allow_null= True)
    temperature = serializers.FloatField(allow_null= True)
    wind_speed = serializers.FloatField(allow_null= True)
    wind_direction = serializers.FloatField(allow_null= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["windSpeed"] = representation.pop("wind_speed")
        representation["windDirection"] = representation.pop("wind_direction")

        return representation


class StationSerializer(serializers.Serializer):
    name =  serializers.CharField(max_length=20, allow_null= True)
    detail = LatestWeatherDataSerializer(allow_null= True)


class AnomalySernsorsSerializer(serializers.Serializer):
    connection_errors = serializers.ListField(
        child=serializers.IntegerField(allow_null=True), allow_null= True
    )
    health_errors = serializers.ListField(
        child=serializers.IntegerField(allow_null=True), allow_null= True
    )
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

                                                                                                                                                                                                                                                                                                                                                   
class AnomalySensorListSerializer(serializers.Serializer):
    counts = serializers.IntegerField(allow_null= True)
    detail = AnomalySernsorsSerializer(allow_null= True)


class TrendSerializer(serializers.Serializer):
    last_year = serializers.FloatField(allow_null= True)
    last_month = serializers.FloatField(allow_null= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["lastYear"] = representation.pop("last_year")
        representation["lastMonth"] = representation.pop("last_month")

        return representation

class ProjectListSerializer(serializers.Serializer):
    bid = serializers.IntegerField()
    name = serializers.CharField(max_length=20)
    type = serializers.CharField(max_length=20)
    station = StationSerializer()
    anomaly_sensor_list = AnomalySensorListSerializer(allow_null= True)
    latest_health = serializers.FloatField(allow_null= True)
    slope = TrendSerializer()
    earthquake = LatestEarthquakeConceptSerializer(allow_null= True)
    typhoon = LatestTyphoonConceptSerializer(allow_null = True)
    