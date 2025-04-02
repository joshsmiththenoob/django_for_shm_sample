from rest_framework import serializers
from web.api.serializer.earthquake_list_serializer import EarthquakeListSerializer

class BridgeEarthquakeListSerializer(EarthquakeListSerializer):
    # earthquake_event
    bid = serializers.IntegerField()
    sensor = serializers.IntegerField(required= False)
    event_id = serializers.IntegerField()