from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from web.api.serializer.bridge_name_serializer import BridgeNameSerializer
from web.api.serializer.upload_bridge_name_serializer import UploadBridgeNameSerializer
from web.api.permission.admin_or_read_only import AdminOrReadyOnly
from web.api.permission.bridge_user_or_read_only import BridgeUserOrReadOnly
from web.api.throttling import BridgeListThrottle, BridgeGetThrottle
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.bridge_list_service import BridgeListService
from bridge.utils.swagger_decorator import (auto_schema_with_file_and_example,
                                                 auto_schema_without_example,
                                                 auto_schema_with_example) # import decorator for SwaggerUI Example
# Create your views here.



class BridgeListView(APIView):

    serializer_class = BridgeNameSerializer
    permission_classes = [IsAdminOrSupoerUser]
    parser_classes = (MultiPartParser, FormParser) # let API receive Multipart/form-data from client
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [BridgeListThrottle]

    @auto_schema_without_example()
    def get(self, request):
        """
        Get list of bridge
        """
        bridge_list_s = BridgeListService()
        response = bridge_list_s.get_bridge_list(request)
        return Response(response,
                        status= status.HTTP_200_OK)

    @auto_schema_with_file_and_example(UploadBridgeNameSerializer)
    def post(self, request):
        """
        Createa a new bridge
        """
        bridge_list_s = BridgeListService()
        response = bridge_list_s.create_new_bridge(request)

        if (response["success"]):
            return Response(data= response,
                        status= status.HTTP_201_CREATED)
        else:
            return Response(data= response,
                        status= status.HTTP_400_BAD_REQUEST)
                            
        

        