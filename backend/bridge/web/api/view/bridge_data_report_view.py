from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.bridge_data_report_service import BridgeDataReportService
from bridge.utils.swagger_decorator import auto_schema_without_example # import decorator for SwaggerUI Example
# Create your views here.



class BridgeDataReportView(APIView):

    permission_classes = [IsAdminOrSupoerUser]

    @auto_schema_without_example()
    def get(self, request, bid: int):
        try:
            # 服務層呼叫
            service = BridgeDataReportService()
            result = service.get(bid= bid)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  