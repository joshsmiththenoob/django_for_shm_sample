from rest_framework import serializers
from drf_yasg import openapi

class BridgeCoordinateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only= True)
    type = serializers.CharField(max_length=20)
    bno = serializers.CharField(max_length=10, allow_null=True)
    name = serializers.CharField(max_length=20)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    address_name = serializers.CharField(max_length=20)
    id_address_name = serializers.CharField(max_length=20)
    photo_name = serializers.CharField(max_length=20)


    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["city"] = representation.pop("address_name")
        representation["distrct"] = representation.pop("id_address_name")
        representation["photoName"] = representation.pop("photo_name")

        return representation