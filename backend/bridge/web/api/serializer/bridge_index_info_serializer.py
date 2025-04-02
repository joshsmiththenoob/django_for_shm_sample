from rest_framework import serializers

class TyphoonConceptSerializer(serializers.Serializer):
    ty_event_id = serializers.IntegerField(allow_null= True)
    ty_cht_name = serializers.CharField(max_length=10, allow_null= True)
    ty_eng_name = serializers.CharField(max_length=10, allow_null= True)
    ty_sea_start_datetime = serializers.DateTimeField(allow_null= True)
    ty_sea_end_datetime = serializers.DateTimeField(allow_null= True)
    ty_max_intensity = serializers.CharField(max_length=3, allow_null= True)
    ty_post_event_health = serializers.FloatField(allow_null= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["id"] = representation.pop("ty_event_id")
        representation["chtName"] = representation.pop("ty_cht_name")
        representation["engName"] = representation.pop("ty_eng_name")
        representation["seaStartDatetime"] = representation.pop("ty_sea_start_datetime")
        representation["seaEndDatetime"] = representation.pop("ty_sea_end_datetime")
        representation["maxIntensity"] = representation.pop("ty_max_intensity")
        representation["postEventHealth"] = representation.pop("ty_post_event_health")

        return representation



class EarthquakeConceptSerializer(serializers.Serializer):
    eq_event_id = serializers.IntegerField(allow_null= True)
    eq_origintime = serializers.DateTimeField( allow_null= True)
    eq_endtime = serializers.DateTimeField(allow_null= True)
    eq_magnitudevalue = serializers.FloatField(allow_null= True)
    eq_longitude = serializers.FloatField(allow_null= True)
    eq_latitude = serializers.FloatField(allow_null= True)
    eq_post_event_health = serializers.FloatField(allow_null= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["id"] = representation.pop("eq_event_id")
        representation["originTime"] = representation.pop("eq_origintime")
        representation["endTime"] = representation.pop("eq_endtime")
        representation["magnitudeValue"] = representation.pop("eq_magnitudevalue")
        representation["longitude"] = representation.pop("eq_longitude")
        representation["latitude"] = representation.pop("eq_latitude")
        representation["postEventHealth"] = representation.pop("eq_post_event_health")

        return representation

class SensorImageCoordinateSerializer(serializers.Serializer):
    x =  serializers.FloatField(allow_null= True)
    y =  serializers.FloatField(allow_null= True)

class SensorConceptSerializer(serializers.Serializer):
    sensor = serializers.IntegerField(allow_null= True)
    latest_time = serializers.DateTimeField(allow_null= True)
    latest_health = serializers.FloatField(allow_null= True)
    type = serializers.CharField(max_length=20, allow_null= True)
    ip = serializers.IntegerField(allow_null= True)
    sensor_location = serializers.CharField(max_length=20, allow_null= True)
    detailed_location = serializers.CharField(max_length=20, allow_null= True)
    cable_mass_per_length = serializers.FloatField(allow_null= True)
    cable_length = serializers.FloatField(allow_null= True)
    elasticity = serializers.FloatField(allow_null= True)
    inertia = serializers.FloatField(allow_null= True)
    mass = serializers.FloatField(allow_null= True)
    health_alert_index = serializers.IntegerField(allow_null= True)
    health_move_index = serializers.IntegerField(allow_null= True)
    event_alert_index = serializers.IntegerField(allow_null= True)
    event_move_index = serializers.IntegerField(allow_null= True)
    bridge_alert_index = serializers.FloatField(allow_null= True)
    bridge_move_index = serializers.FloatField(allow_null= True)
    image_coordinate = SensorImageCoordinateSerializer(allow_null= True)
    status = serializers.IntegerField(allow_null= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["id"] = representation.pop("sensor")
        representation["latestTime"] = representation.pop("latest_time")
        representation["latestHealth"] = representation.pop("latest_health")
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


class BridgeConceptSerializer(serializers.Serializer):
    bid = serializers.IntegerField()
    bridge_name = serializers.CharField(max_length=20)
    address_name = serializers.CharField(max_length=20)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    id_address_name = serializers.CharField(max_length=20)
    photo_name = serializers.CharField(max_length=200)
    latest_health = serializers.FloatField(allow_null= True)
    base64 = serializers.CharField()
     
    def to_representation(self, instance):
            """ 
            Modify representation from parent's class.to_representation() method
            to get custom JSON file
            """
            representation = super().to_representation(instance) 
            
            # modify key from representation json
            representation["id"] = representation.pop("bid")
            representation["name"] = representation.pop("bridge_name")
            representation["city"] = representation.pop("address_name")
            representation["district"] = representation.pop("id_address_name")
            representation["photoName"] = representation.pop("photo_name")
            representation["latestHealth"] = representation.pop("latest_health")
            
            return representation
    

class WeatherConceptSerializer(serializers.Serializer):
    # station_id = serializers.CharField(max_length=20, allow_null= True)
    # station_name = serializers.CharField(max_length=20, allow_null= True)
    latest_weather_time = serializers.DateTimeField(allow_null= True)
    latest_precipitation = serializers.FloatField()
    latest_temperature = serializers.FloatField()
    latest_wind_speed = serializers.FloatField()
    latest_wind_direction = serializers.IntegerField()

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["latestWeatherTime"] = representation.pop("latest_weather_time")
        representation["latestPrecipitation"] = representation.pop("latest_precipitation")
        representation["latestTemperature"] = representation.pop("latest_temperature")
        representation["latestWindSpeed"] = representation.pop("latest_wind_speed")
        representation["latestWindDirection"] = representation.pop("latest_wind_direction")
        
        return representation

class BridgeIndexInfoSerializer(serializers.Serializer):
    bridge = BridgeConceptSerializer(allow_null= True)
    weather = WeatherConceptSerializer(allow_null= True)
    sensor_list = SensorConceptSerializer(many= True, allow_null= True)
    earthquake = EarthquakeConceptSerializer(allow_null= True)
    typhoon = TyphoonConceptSerializer(allow_null= True)

    def to_representation(self, instance):
            """ 
            Modify representation from parent's class.to_representation() method
            to get custom JSON file
            """
            representation = super().to_representation(instance) 
            
            # modify key from representation json
            representation["sensorList"] = representation.pop("sensor_list")
            
            return representation