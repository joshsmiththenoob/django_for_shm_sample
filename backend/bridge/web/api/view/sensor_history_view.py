from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from web.api.serializer.sensor_history_serializer import SensorHistorySerializer
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.sensor_history_service import SensorHistoryService
from bridge.utils.swagger_decorator import (auto_schema_with_example,
                                                 auto_schema_without_example,
                                                 auto_schema_with_query_params) # import decorator for SwaggerUI Example
from drf_yasg.utils import swagger_auto_schema



class SensorHistoryView(APIView):

    serializer_class = SensorHistorySerializer
    permission_classes = [AllowAny]

    @auto_schema_with_query_params(SensorHistorySerializer)
    def get(self, request, bid: int, sid: int):
        # 服務層呼叫
        service = SensorHistoryService()
        response = service.get(request, bid= bid, sid= sid)

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
                            


# class SensorHistoryView(generics.ListAPI):

#     serializer_class = BridgeIndexInfoSerializer
#     permission_classes = [AllowAny]

#     @auto_schema_without_example()
#     def get(self, request, bid: int, sid: int):
#         try:
#             # 服務層呼叫
#             service = SensorHistoryService()
#             result = service.get(bid= bid, sid= sid)
#             return Response(result, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


# class SensorHistoryView(generics.ListAPI):

#     serializer_class = BridgeIndexInfoSerializer
#     permission_classes = [AllowAny]

#     @auto_schema_without_example()
#     def get(self, request, bid: int, sid: int):
#         try:
#             # 服務層呼叫
#             service = SensorHistoryService()
#             result = service.get(bid= bid, sid= sid)
#             return Response(result, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  