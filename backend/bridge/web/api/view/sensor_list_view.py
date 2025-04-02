from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from web.api.serializer.sensor_name_serializer import SensorNameSerializer
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.sensor_list_service import SensorListService
from bridge.utils.swagger_decorator import (auto_schema_with_example,) # import decorator for SwaggerUI Example
# Create your views here.



class SensorListView(APIView):

    serializer_class = SensorNameSerializer
    permission_classes = [IsAdminOrSupoerUser]

    @auto_schema_with_example(SensorNameSerializer)
    def post(self, request, bid: int):
        """
        Createa a new sensor
        """
        sensor_list_s = SensorListService()
        response = sensor_list_s.create_new_sensor(request, bid)

        if (response["success"]):
            return Response(data= response,
                        status= status.HTTP_201_CREATED)
        else:
            return Response(data= response,
                        status= status.HTTP_400_BAD_REQUEST)

        