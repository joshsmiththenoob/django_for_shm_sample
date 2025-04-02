from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from web.api.serializer.sensor_name_serializer import SensorNameSerializer
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.sensor_service import SensorService
from bridge.utils.swagger_decorator import (auto_schema_with_example,) # import decorator for SwaggerUI Example
# Create your views here.



class SensorView(APIView):

    serializer_class = SensorNameSerializer
    permission_classes = [IsAdminOrSupoerUser]
    
    @auto_schema_with_example(SensorNameSerializer)
    def put(self, request, bid: int, sid: int):
        """
        Update sensor
        """

        sensor_list_s = SensorService()
        response = sensor_list_s.update_sensor(request, bid, sid)

        if (response["success"]):
            return Response(data= response,
                            status= status.HTTP_204_NO_CONTENT)
        elif (response["success"] == False) & (response["message"] == "Error, Ba dRequest!"):
            return Response(data= response,
                            status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data= response,
                            status= status.HTTP_404_NOT_FOUND)

    def delete(self, request, bid: int, sid: int):
        """
        Delete sensor
        """

        sensor_list_s = SensorService()
        response = sensor_list_s.delete_sensor(bid, sid)

        if (response["success"]):
            return Response(data= response,
                        status= status.HTTP_204_NO_CONTENT)
        else:
            return Response(data= response,
                            status= status.HTTP_404_NOT_FOUND)