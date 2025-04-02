from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from web.api.serializer.bridge_index_info_serializer import BridgeIndexInfoSerializer
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.bridge_index_info_service import BridgeIndexInfoService
from bridge.utils.swagger_decorator import auto_schema_without_example # import decorator for SwaggerUI Example
# Create your views here.



class BridgeIndexInfoView(APIView):

    serializer_class = BridgeIndexInfoSerializer
    permission_classes = [IsAdminOrSupoerUser]

    @auto_schema_without_example()
    def get(self, request, id):
        # try:
        service = BridgeIndexInfoService()
        result = service.get(bid= id)
        return Response(result, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     

        