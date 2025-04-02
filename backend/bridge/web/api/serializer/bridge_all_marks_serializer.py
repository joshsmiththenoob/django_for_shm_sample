from rest_framework import serializers
from drf_yasg import openapi

class BridgeAllMarksSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only= True)
    type = serializers.CharField(max_length=20)
    bno = serializers.CharField(max_length=10, allow_null=True)
    name = serializers.CharField(max_length=20)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    address_name = serializers.CharField(max_length=20)
    id_address_name = serializers.CharField(max_length=20)
    photo_name = serializers.CharField(max_length=200)
    deleted = serializers.IntegerField()

    class Meta:

        example = {
            "type": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="建物編號，例如：'B001'",
                example= "Bridge",
            ),
            "bno": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="建物類型，例如：'Bridge'",
                example= "B001",
            ),
            "name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="建物名稱，例如：'中山橋'",
                example="中山橋",
            ),
            "longitude": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="建物名稱，例如：'經度ㄝ, 例如: 121.5544'",
                example= 121.5544,
            ),
            "latitude": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="建物類型，例如：'緯度, 例如: 25.033'",
                example= 25.033,
            ),
            "address_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="地址名稱, 例如: '新竹市'",
                example= "新竹市",
            ),
            "id_address_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="地址代碼, 例如: '東區'",
                example= "東區",
            ),
            "photo_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="照片名稱, 例如: 'sample.jpg'",
                example= "sample.jpg",
            ),
            "base64": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Base64 編碼, 例如: 'base64string'",
                example= "base64string",
            )
            
        }