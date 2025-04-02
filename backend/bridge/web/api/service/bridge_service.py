from web.models import Bridge, Sensor
from django.conf import settings
from django.shortcuts import get_object_or_404
from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.bridge_name_serializer import BridgeNameSerializer
from web.api.serializer.upload_bridge_name_serializer import UploadBridgeNameSerializer
from web.api.handler.image_handler import ImageHandler
import requests
import os

class BridgeService:
    serializer_class = BridgeNameSerializer
    CWA_API_URL = os.getenv("CWA_API_URL")
    CWA_API_KEY = os.getenv("CWA_API_KEY")

    def __init__(self):
        self.__img_handler = ImageHandler()


    def get_serializer_class(self, request):
        """
        return Serializer based on request METHOD
        """
        if (request.method == "POST"):
            return UploadBridgeNameSerializer
        return self.serializer_class
    
    def get_bridge(self, id: int):
        # form json
        json = dict()

        try:
            result = get_object_or_404(Bridge, id= id, deleted= 0)
            serializer = self.serializer_class(instance= result)
            json["success"] = True
            json["message"] = "Get data successfully"
            json["data"] = serializer.data

        except Exception as e:
            json["success"] = False
            json["message"] = str(e)
            json["data"] = None
        

        return json
    
    def update_bridge(self, id: int, request):
        """
        Update a existed bridge by uploading File/Photo
        """
        data = request.data.copy()
        try:
            if (request.FILES.get("photo")):
                pic_file = request.FILES.get("photo")
                data["base64"] = self.__img_handler.convert_img_into_base64(pic_file)
                data["photo_name"] = self.__img_handler.get_file_name(pic_file)

            # get Automatic Weather Station Id and Bridge's ctyName、townName
            longitude = data["longitude"]
            latitude = data["latitude"]
            station_id, ctyName, townName = self.__get_station_id(longitude=longitude, latitude=latitude)
            data["station_id"] = station_id
            data["city"] = ctyName
            data["district"] = townName

            result = get_object_or_404(Bridge, id= id)
            # update new content to old data(record)
            upload_serializer_class = UploadBridgeNameSerializer
            upload_serializer = upload_serializer_class(instance=result, data=data, partial=True)

            if upload_serializer.is_valid():
                # update image
                if ("photo_name" in upload_serializer.validated_data):
                    self.__img_handler.delete_img(settings.BRIDGE_IMAGE_DIR, result.photo_name)
                    self.__img_handler.save_img(settings.BRIDGE_IMAGE_DIR, pic_file)
                # save image
                upload_serializer.save()
                json = ResponseFormatter.format_put_response()
            else:
                json = ResponseFormatter.format_400_response(upload_serializer.errors)

        except Exception as e:
            print(e)


        return json
    
    def delete_bridge(self, id: int):
        """
        Delete a existed bridge
        """
        bridge_info = get_object_or_404(Bridge, id=id)
        bridge_info.deleted = 1
        bridge_info.save()

        # delete sensors inside the bridge
        sensor_info_list = Sensor.objects.filter(bid=id) # select all sensors inside the bridge
        if sensor_info_list.exists():
            sensor_info_list.update(deleted=1)

        return ResponseFormatter.format_delete_response()

    def __get_station_id(self, longitude: float, latitude: float):
        query = f"""query aqi {{
                        aqi(longitude: {longitude}, latitude: {latitude}) {{

                            station {{
                                stationId,
                                locationName,
                                latitude,
                                longitude,
                            
                            }},
                            town {{
                                ctyCode,
                                ctyName,
                                townCode,
                                townName,
                                villageCode,
                                villageName
                                #forecast72hr, forecastWeekday...
                            }}
                        }}
                    }}"""
        data = {"query": query}
        headers = {
            "Authorization": self.CWA_API_KEY,  # API 金鑰
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        try:
            # Get response
            response = requests.post(
                self.CWA_API_URL, json=data, headers=headers, timeout=10
            )
            response.raise_for_status()  # raise error if HTTP error
            json = response.json()
            station_id = json["data"]["aqi"][0]["station"]["stationId"]
            ctyName = json["data"]["aqi"][0]["town"]["ctyName"]
            townName = json["data"]["aqi"][0]["town"]["townName"]
            return station_id, ctyName, townName

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}