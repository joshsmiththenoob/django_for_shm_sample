from rest_framework import serializers

class EarthquakeListSerializer(serializers.Serializer):
    # earthquake_event
    bid = serializers.IntegerField()
    sensor = serializers.IntegerField()
    event_id = serializers.IntegerField()

    # earthquake
    origintime = serializers.DateTimeField( allow_null= True)
    endtime = serializers.DateTimeField( allow_null= True)
    epicenterlocation = serializers.CharField(max_length=50, allow_null= True)
    longitude = serializers.FloatField(allow_null= True)
    latitude = serializers.FloatField(allow_null= True)
    magnitudevalue = serializers.FloatField(allow_null= True)
    depthvalue = serializers.FloatField(allow_null= True)
    before = serializers.FloatField(allow_null= True)
    after = serializers.FloatField(allow_null= True)
    freqeuncy_variance_ratio = serializers.FloatField(allow_null= True)
    max_during =  serializers.FloatField(required= False, allow_null= True)

    # final_seismic_resistance
    post_event_health = serializers.FloatField(allow_null= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["id"] = representation.pop("event_id")
        representation["originTime"] = representation.pop("origintime")
        representation["endTime"] = representation.pop("endtime")
        representation["epiCenterLocation"] = representation.pop("epicenterlocation")
        representation["magnitudeValue"] = representation.pop("magnitudevalue")
        representation["postEventHealth"] = representation.pop("post_event_health")
        representation["frequencyVarianceRatio"] = representation.pop("freqeuncy_variance_ratio")
        representation["maxDuring"] = representation.pop("max_during")
        
        return representation