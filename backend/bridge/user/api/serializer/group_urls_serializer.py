# Serializer
"""
Serializer:
like DTO in SpringBoot, 
in charge of serialize (Object -> Json) de-serialize(Json -> Object) the data between frontend and backend

also check if the data structure is correct or not.

"""

# the Serialize could container anoter serialize like datatype(class)

from rest_framework import serializers
from drf_yasg import openapi

class LinkSerializer(serializers.Serializer):
    title =  serializers.CharField()
    path = serializers.CharField()
    element = serializers.CharField()


class GroupUrlsSerializer(serializers.Serializer):
    group = serializers.CharField()
    base64 = serializers.CharField()
    links = LinkSerializer(many= True, allow_null= True)

