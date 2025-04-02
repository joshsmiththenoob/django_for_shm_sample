from rest_framework import serializers
from web.models import Bridge
from drf_yasg import openapi
from django.http import QueryDict
from rest_framework.utils.serializer_helpers import ReturnDict

class BridgeNameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only= True)
    type = serializers.CharField(max_length=20)
    bno = serializers.CharField(max_length=10, allow_null=True)
    name = serializers.CharField(max_length=20)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    address_name = serializers.CharField(max_length=20)
    id_address_name = serializers.CharField(max_length=20)
    photo_name = serializers.CharField(max_length=200)
    base64 = serializers.CharField()
    deleted = serializers.IntegerField(default= 0)



    def create(self, validated_data):
        return Bridge.objects.create(**validated_data) # unpack validated_data:dict 


    def update(self, instance, validated_data: dict): # validated_data is dict
        """
        instance: the old value of record
        validated_data: the new value of record
        """
        # get value of key and replace it to the existed value
        instance.type = validated_data.get("type", instance.type)
        instance.bno = validated_data.get("bno", instance.bno)
        instance.name = validated_data.get("name", instance.name)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.latitude = validated_data.get("latitude", instance.longitude)
        instance.address_name = validated_data.get("address_name", instance.address_name)
        instance.id_address_name = validated_data.get("id_address_name", instance.id_address_name)
        instance.photo_name = validated_data.get("photo_name", instance.photo_name)
        instance.base64 = validated_data.get("base64", instance.base64)
        instance.deleted = validated_data.get("deleted", instance.deleted)
        instance.save() # update the content of existied data(record) in DB
        print("update completed")
        return instance
    

    def to_internal_value(self, data):
        """
        Convert input data (e.g, city -> address_name) for internal use from frontend(client)
        But in the future we need to update table column
        """
        if isinstance(data, QueryDict):
            data = data.copy()
        else:
            # 如果包含文件字段，使用 ReturnDict 處理
            data = ReturnDict(data, serializer=self)
            
        if ("city" in data):
            data["address_name"] = data["city"] 
        if ("district" in data):
            data["id_address_name"] = data["district"]

        return super().to_internal_value(data)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modify key from representation json
        representation["city"] = representation.pop("address_name")
        representation["district"] = representation.pop("id_address_name")

        return representation

    class Meta:
        # example = {
        #     "type": "Bridge",
        #     "bno": "B001",
        #     "name": "中山橋",
        #     "longitude": 121.5544,
        #     "latitude": 25.033,
        #     "address_name": "新竹市",
        #     "id_address_name": "東區",
        #     "photo_name": "sample.jpg",
        #     "base64": "base64string",
        #     "aid": 123,
        #     "deleted": 0,
        # }

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
            "city": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="地址名稱, 例如: '新竹市'",
                example= "新竹市",
            ),
            "district": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="地址代碼, 例如: '東區'",
                example= "東區",
            ),
            # "photo_name": openapi.Schema(
            #     type=openapi.TYPE_STRING,
            #     description="照片名稱, 例如: 'sample.jpg'",
            #     example= "sample.jpg",
            # ),
            # "base64": openapi.Schema(
            #     type=openapi.TYPE_STRING,
            #     description="Base64 編碼, 例如: 'base64string'",
            #     example= "base64string",
            # )
            
        }