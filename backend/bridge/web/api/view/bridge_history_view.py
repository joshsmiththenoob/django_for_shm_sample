from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from web.api.serializer.bridge_history_serializer import BridgeHistorySerializer
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.bridge_history_service import BridgeHistoryService
from bridge.utils.swagger_decorator import (auto_schema_with_example,
                                                 auto_schema_without_example,
                                                 auto_schema_with_query_params) # import decorator for SwaggerUI Example
from drf_yasg.utils import swagger_auto_schema



class BridgeHistoryView(APIView):

    serializer_class = BridgeHistorySerializer
    permission_classes = [AllowAny]

    @auto_schema_with_query_params(BridgeHistorySerializer)
    def get(self, request, bid: int):
        # 服務層呼叫
        service = BridgeHistoryService()
        response = service.get(request, bid= bid)

        print(response)
        
        if (response["success"]):
            return Response(data= response,
                        status= status.HTTP_201_CREATED)
        elif (response["success"] == False) and (response["status"] == 400):
            return Response(data= response,
                        status= status.HTTP_400_BAD_REQUEST)

        else:
            return Response(data= response,
                        status= status.HTTP_500_INTERNAL_SERVER_ERROR)
                            

