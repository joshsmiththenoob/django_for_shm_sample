import os
from web.models import Bridge
from django.db.models import Max
from django.conf import settings
from rest_framework import status
from web.models import AuthAgencyUsers, AuthAgencyBridges
from rest_framework.request import Request
from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.bridge_name_serializer import BridgeNameSerializer
from web.api.serializer.upload_bridge_name_serializer import UploadBridgeNameSerializer
from web.api.handler.image_handler import ImageHandler
import requests



"""
The rule of Reponse Body structure:
{
    "success"(boolean): if client get response successful or not
    "message"(string):  message detail
    "data"(any): return data
}

"""


class BridgeListService:
    serializer_class = BridgeNameSerializer
    CWA_API_URL = os.getenv("CWA_API_URL")
    CWA_API_KEY = os.getenv("CWA_API_KEY")

    def __init__(self):
        self.__img_handler = ImageHandler()

    def get_serializer_class(self, request):
        """
        return Serializer based on request METHOD
        """
        if request.method == "POST":
            return UploadBridgeNameSerializer
        return self.serializer_class

    def get_bridge_list(self, request: Request):
        """
        Get list of bridge
        """
        user = request.user
        
        if (user.is_superuser):
            # Admin sees all non-deleted bridges
            bridge_objects = Bridge.objects.filter(deleted=0)
        else:
            # Regular users see bridges related through AuthAgencyBridges
            bridge_ids = AuthAgencyBridges.objects.filter(
                agency__authagencyusers__user=user,
                bridge__deleted=0
            ).values_list('bridge_id', flat=True).distinct()
            bridge_objects = Bridge.objects.filter(id__in=bridge_ids)

        # set argument:many to True for getting multiple results from ORM objects
        serializer = self.get_serializer_class(request)(instance= bridge_objects, many= True) 
        # QuerySet.values() returns a type like list but still a QuerySet object
        # Need to change data type from QuerySet objects to list, and get involved by dict we created

        # form json
        json = ResponseFormatter.format_get_response(serializer.data)

        return json
    def create_new_bridge(self, request: Request):
        """
        Create a new bridge by uploading File/Photo
        """
        # Check if it get the file or not
        pic_file = request.FILES.get("photo")
        if not pic_file:
            return ResponseFormatter.format_400_response("No photo provided")

        # setting default value
        request.data["deleted"] = 0
        request.data["type"] = "Bridge"

        # optional: quite not sure if base64 is needed or not
        request.data["base64"] = self.__img_handler.convert_img_into_base64(pic_file)
        # get id for new bridge
        max_bridge = Bridge.objects.latest('id')
        extension = os.path.splitext(pic_file.name)[1]
        request.data["photo_name"] = f"Bridge{max_bridge.id + 1}" + extension
        
        # get station_id for new bridge
        longitude = request.data["longitude"]
        latitude = request.data["latitude"]
        station_id, ctyName, townName = self.__get_station_id(longitude=longitude, latitude=latitude)
        request.data["station_id"] = station_id
        request.data["address_name"] = ctyName
        request.data["id_address_name"] = townName

        serializer = self.get_serializer_class(request)(data=request.data)


        # form json
        if serializer.is_valid():
            try:
                # save img
                self.__img_handler.save_img(
                    settings.BRIDGE_IMAGE_DIR, pic_file, request.data["photo_name"]
                )


                # filter the new record we need to insert in DB
                validated_data = serializer.validated_data
                validated_data.pop("photo")  # don't want the photo file to insert in DB

                # save & return new object
                new_bridge = serializer.create(validated_data)
                self.__add_relation_between_agency_and_bridge(request, new_bridge)
                json = ResponseFormatter.format_post_response(validated_data)
            except Exception as e:
                print(e)
                json = ResponseFormatter.format_400_response(str(e))
        else:
            print(serializer.errors)
            json = ResponseFormatter.format_400_response(serializer.validated_data)


        return json

    def __add_relation_between_agency_and_bridge(self, request, new_bridge):
        # get group ORM object of request user
        user_id = request.user.id

        # get ORM object which user_id == user_id and search specific attribute agency object first
        agency_results = AuthAgencyUsers.objects.filter(user_id=user_id).select_related(
            "agency"
        )
        a_id = agency_results[0].agency.id

        AuthAgencyBridges.objects.create(agency_id=a_id, bridge_id=new_bridge.id)

    def __get_station_id(self, longitude: float, latitude: float):
        print(0)
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
        print(self.CWA_API_KEY)
        print(self.CWA_API_URL)
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
