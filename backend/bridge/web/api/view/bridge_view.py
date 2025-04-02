from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from rest_framework.parsers import MultiPartParser, FormParser
from web.api.service.bridge_service import BridgeService
from web.api.serializer.bridge_name_serializer import BridgeNameSerializer
from web.api.serializer.upload_bridge_name_serializer import UploadBridgeNameSerializer
from bridge.utils.swagger_decorator import (auto_schema_with_file_and_example,
                                                auto_schema_without_example) # import decorator for SwaggerUI Example


class BridgeView(APIView):
    # permission_classes was class attribute 
    serializer_class = BridgeNameSerializer
    permission_classes = [IsAdminOrSupoerUser]
    parser_classes = (MultiPartParser, FormParser) # let API receive Multipart/form-data from client
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [BridgeGetThrottle]
    bridge_s = BridgeService()

    @auto_schema_without_example()
    def get(self, request, id: int):
        """
        Get bridge by id
        """
        bridge_s = BridgeService()
        response = bridge_s.get_bridge(id)

        if (response["success"]):
            return Response(data= response,
                        status= status.HTTP_201_CREATED)
        else:
            return Response(data= response,
                        status= status.HTTP_404_NOT_FOUND)
    
    
    @auto_schema_with_file_and_example(UploadBridgeNameSerializer)
    def put(self, request, id):
        """
        Update bridge
        """
        # # get old data(record) query object
        # result = get_object_or_404(BridgeName, id= id)
        # self.check_object_permissions(request, result) 

        # update new content to old data(record)
        bridge_s = BridgeService()
        response = bridge_s.update_bridge(id, request)
        if (response["success"]):
            return Response(data= response,
                            status= status.HTTP_204_NO_CONTENT)
        elif (response["success"] == False) & (response["message"] == "Error, Bad Request!"):
            return Response(data= response,
                            status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data= response,
                            status= status.HTTP_404_NOT_FOUND)
        

    @auto_schema_without_example()
    def delete(self, request, id):
        """
        Delete bridge
        """
        bridge_s = BridgeService()
        response = bridge_s.delete_bridge(id)

        if (response["success"]):
            return Response(data= response,
                            status= status.HTTP_204_NO_CONTENT)
        else:
            return Response(data= response,
                            status= status.HTTP_404_NOT_FOUND)
