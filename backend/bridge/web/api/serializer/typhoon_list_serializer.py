from rest_framework import serializers

class TyphoonListSerializer(serializers.Serializer):
    # typhoon_event
    bid = serializers.IntegerField()
    sensor = serializers.IntegerField()
    event_id = serializers.IntegerField()

    # typhoon
    cht_name = serializers.CharField(max_length=10, allow_null= True)
    eng_name = serializers.CharField(max_length=50, allow_null= True)
    sea_start_datetime = serializers.DateTimeField( allow_null= True)
    sea_end_datetime = serializers.DateTimeField( allow_null= True)
    max_intensity = serializers.CharField(max_length=3, allow_null= True)
    before = serializers.FloatField(allow_null= True)
    after = serializers.FloatField(allow_null= True)
    freqeuncy_variance_ratio = serializers.FloatField(allow_null= True)


    # final_flood_resistance
    post_event_health = serializers.FloatField(allow_null= True)
   
    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["id"] = representation.pop("event_id")
        representation["chtName"] = representation.pop("cht_name")
        representation["engName"] = representation.pop("eng_name")
        representation["seaStartDatetime"] = representation.pop("sea_start_datetime")
        representation["seaEndDatetime"] = representation.pop("sea_end_datetime")
        representation["maxIntensity"] = representation.pop("max_intensity")
        representation["postEventHealth"] = representation.pop("post_event_health")
        representation["frequencyVarianceRatio"] = representation.pop("freqeuncy_variance_ratio")
        
        return representation
        