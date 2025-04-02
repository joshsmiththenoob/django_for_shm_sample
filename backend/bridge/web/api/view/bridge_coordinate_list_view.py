from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from web.api.serializer.bridge_name_serializer import BridgeNameSerializer
from web.api.service.bridge_coordinate_list_service import BridgeCoordinateListService
from bridge.utils.swagger_decorator import auto_schema_without_example # import decorator for SwaggerUI Example
# Create your views here.


class BridgeCoordinateListView(APIView):

    serializer_class = BridgeNameSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [BridgeListThrottle]

    @auto_schema_without_example()
    def get(self, request):
        """
        Get list of bridge
        """
        bridge_list_s = BridgeCoordinateListService()
        response = bridge_list_s.get_bridge_coord_list(request)
        return Response(response,
                        status= status.HTTP_200_OK)

        

        