from rest_framework import serializers
from web.models import Bridge
from drf_yasg import openapi


class UploadBridgeNameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(max_length=20, default="Bridge")
    bno = serializers.CharField(max_length=10, required=False)
    name = serializers.CharField(max_length=20, required=False)
    longitude = serializers.FloatField(required=False)
    latitude = serializers.FloatField(required=False)
    address_name = serializers.CharField(max_length=20, required=False)
    id_address_name = serializers.CharField(max_length=20, required=False)
    photo_name = serializers.CharField(max_length=200, required=False, allow_null=True)
    base64 = serializers.CharField(required=False, allow_null=True)
    deleted = serializers.IntegerField(default=0, required=False)
    photo = serializers.FileField(required=False, allow_null=True)
    station_id = serializers.CharField(max_length=50, required=False)

    def create(self, validated_data):
        return Bridge.objects.create(**validated_data)  # unpack validated_data:dict

    def update(self, instance, validated_data: dict):  # validated_data is dict
        """
        instance: the old value of record
        validated_data: the new value of record
        """
        # get value of key and replace it to the existed value
        instance.type = validated_data.get("type", instance.type)
        instance.bno = validated_data.get("bno", instance.bno)
        instance.name = validated_data.get("name", instance.name)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.address_name = validated_data.get("address_name", instance.address_name)
        instance.id_address_name = validated_data.get("id_address_name", instance.id_address_name)
        instance.photo_name = validated_data.get("photo_name", instance.photo_name)
        instance.base64 = validated_data.get("base64", instance.base64)
        instance.deleted = validated_data.get("deleted", instance.deleted)
        instance.station_id = validated_data.get("station_id", instance.station_id)
        instance.save() # update the content of existied data(record) in DB
        print("update completed")
        return instance

    def to_internal_value(self, data):
        """
        Convert input data (e.g, city -> address_name) for internal use from frontend(client)
        But in the future we need to update table column
        """

        # # 將 QueryDict 的列表值轉換為單一值
        # if isinstance(data, QueryDict):
        #     data = {key: value[0] if isinstance(value, list) else value for key, value in data.items()}
        if "city" in data:
            data["address_name"] = data["city"]
        if "district" in data:
            data["id_address_name"] = data["district"]

        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modify key from representation json
        representation["city"] = representation.pop("address_name")
        representation["district"] = representation.pop("id_address_name")
        representation["photoName"] = representation.pop("photo_name")
        representation["stationId"] = representation.pop("station_id")

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

##############################################################################################
class BridgeLocationImageSerializer(serializers.Serializer):
    base64 = serializers.CharField() 
    index = serializers.IntegerField()

class QSerializer(serializers.Serializer):
    Q2 = serializers.ListField(
        child=serializers.FloatField(allow_null=True),  
        allow_empty=True,  
        required= False
    )
    Q4 = serializers.ListField(
        child=serializers.FloatField(allow_null=True),  
        allow_empty=True,
        required= False 
    )
    Q0 = serializers.ListField(
        child=serializers.FloatField(allow_null=True),  
        allow_empty=True, 
        required= False  
    )
    result = serializers.CharField(allow_null= True, required= False)
    chart = BridgeLocationImageSerializer(allow_null= True, required= False) # base64 + index
    alert_massage = serializers.CharField(allow_null= True, required= False)
    result_massage = serializers.CharField(allow_null= True, required= False)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["alertMassage"] = representation.pop("alert_massage")
        representation["resultMassage"] = representation.pop("result_massage")
        
        
        return representation

class BridgeInfoSerializer(serializers.Serializer):
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
    staiton_id = serializers.CharField(max_length=50)
    deleted = serializers.IntegerField(default= 0)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modify key from representation json
        representation["city"] = representation.pop("address_name")
        representation["district"] = representation.pop("id_address_name")
        representation["photoName"] = representation.pop("photo_name")
        representation["staitonId"] = representation.pop("staiton_id")

        return representation

class SensorCoordinateIndexSerializer(serializers.Serializer):
    image_x =  serializers.FloatField(allow_null= True)
    image_y =  serializers.FloatField(allow_null= True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modify key from representation json
        representation["x"] = representation.pop("image_x")
        representation["y"] = representation.pop("image_y")

        return representation

class SensorLocationImageSerializer(serializers.Serializer):
    bridge_image = serializers.CharField() # bridge_info 內已經包含圖片?
    sensor_coordinate_index = SensorCoordinateIndexSerializer()

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["bridgeImage"] = representation.pop("bridge_image")
        representation["sensorCoordinateIndex"] = representation.pop("sensor_coordinate_index")
        
        return representation

class SensorDataSerializer(serializers.Serializer):
    sensor = serializers.IntegerField(allow_null= True, required= False)
    detailed_location = serializers.CharField(max_length=20, allow_null= True, required= False)
    sensor_location = serializers.CharField(max_length=20, allow_null= True, required= False)
    cable_mass_per_length = serializers.FloatField(allow_null= True, required= False)
    cable_length = serializers.FloatField(allow_null= True, required= False)
    elasticity = serializers.FloatField(allow_null= True, required= False)
    inertia = serializers.FloatField(allow_null= True, required= False)
    mass = serializers.FloatField(allow_null= True, required= False)
    # 跨距
    # 最近橋柱距離
    health_alert_index = serializers.IntegerField(allow_null= True, required= False)
    health_move_index = serializers.IntegerField(allow_null= True, required= False)
    event_alert_index = serializers.IntegerField(allow_null= True, required= False)
    event_move_index = serializers.IntegerField(allow_null= True, required= False)
    sensor_location_image = SensorLocationImageSerializer(many=True, required= False)

    seismic = QSerializer(many= True, required= False)
    centroid_frequency = QSerializer(many= True, required= False)
    damping_ratio = QSerializer(many= True, required= False)
    cable_force = QSerializer(many= True, required= False)
    effective_length = QSerializer(many= True, required= False)
    load_carry_capacity =QSerializer(many= True, required= False)
    health = QSerializer(many= True, required= False)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["detailedLocation"] = representation.pop("detailed_location")
        representation["sensorLocation"] = representation.pop("sensor_location")
        representation["cableMassPerLength"] = representation.pop("cable_mass_per_length")
        representation["cableLength"] = representation.pop("cable_length")
        representation["healthAlertIndex"] = representation.pop("health_alert_index")
        representation["healthMoveIndex"] = representation.pop("health_move_index")
        representation["eventAlertIndex"] = representation.pop("event_alert_index")
        representation["eventMoveIndex"] = representation.pop("event_move_index")
        representation["sensorLocationImage"] = representation.pop("sensor_location_image")
        representation["centroidFrequency"] = representation.pop("centroid_frequency")
        representation["dampingRatio"] = representation.pop("damping_ratio")
        representation["cableForce"] = representation.pop("cable_force")
        representation["effectiveLength"] = representation.pop("effective_length")
        representation["loadCarryCapacity"] = representation.pop("load_carry_capacity")
        
        return representation

class BridgeDataSerializer(serializers.Serializer):
    seismic = QSerializer(many= True, required= True)
    centroid_frequency = QSerializer(many= True, required= True)
    damping_ratio = QSerializer(many= True, required= True)
    health = QSerializer(many= True, required= True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["centroidFrequency"] = representation.pop("centroid_frequency")
        representation["dampingRatio"] = representation.pop("damping_ratio")
        
        return representation

################################# Report ###################################
class ReportBasicDataSerializer(serializers.Serializer):
    agency_name = serializers.CharField(max_length=20)
    report_name = serializers.CharField(max_length=50)
    user_company = serializers.CharField(max_length=50)
    now_date = serializers.DateTimeField() 
    bridge_name = serializers.CharField(max_length=20)
    bridge_info = BridgeInfoSerializer(allow_null=True) 
    longitude = serializers.FloatField() # bridge_info 內有包含經位度資訊，是要放在外層還是bridge_info內?
    latitude = serializers.FloatField() # bridge_info 內有包含經位度資訊，是要放在外層還是bridge_info內?
    bridge_location_image = BridgeLocationImageSerializer()
    sensor_data = SensorDataSerializer(many=True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["agencyName"] = representation.pop("agency_name")
        representation["reportName"] = representation.pop("report_name")
        representation["userCompany"] = representation.pop("user_company")
        representation["nowDate"] = representation.pop("now_date")
        representation["bridgeName"] = representation.pop("bridge_name")
        representation["bridgeInfo"] = representation.pop("bridge_info")
        representation["bridgeLocationImage"] = representation.pop("bridge_location_image")
        representation["sensorData"] = representation.pop("sensor_data")
        
        return representation

class ReportSecondDataSerializer(serializers.Serializer):
    last_date = serializers.DateTimeField()
    tempature = serializers.FloatField()
    wind_speed = serializers.FloatField()
    wind_direction = serializers.FloatField()
    bridge_data = BridgeDataSerializer()
    sensor_data = SensorDataSerializer(many=True)

    def to_representation(self, instance):
        """ 
        Modify representation from parent's class.to_representation() method
        to get custom JSON file
        """
        representation = super().to_representation(instance) 
        
        # modify key from representation json
        representation["lastDate"] = representation.pop("last_date")
        representation["windSpeed"] = representation.pop("wind_speed")
        representation["windDirection"] = representation.pop("wind_direction")
        representation["bridgeData"] = representation.pop("bridge_data")
        representation["sensorData"] = representation.pop("sensor_data")
        
        return representation