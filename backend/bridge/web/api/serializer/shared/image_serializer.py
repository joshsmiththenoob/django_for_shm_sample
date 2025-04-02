from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    index = serializers.IntegerField(required= False, allow_null=True)
    base64 = serializers.CharField(required= False, allow_null=True) 


