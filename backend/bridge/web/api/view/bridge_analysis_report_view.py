from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.bridge_analysis_report_service import BridgeAnalysisReportService
from web.api.serializer.bridge_analysis_report_serializer import BridgeAnalysisReportSerializer
from bridge.utils.swagger_decorator import auto_schema_with_query_params # import decorator for SwaggerUI Example


class BridgeAnalysisReportView(APIView):
    # permission_classes was class attribute 
    serializer_class = BridgeAnalysisReportSerializer
    permission_classes = [IsAdminOrSupoerUser]
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [BridgeGetThrottle]
    bridge_analysis_report_s = BridgeAnalysisReportService()

    @auto_schema_with_query_params(BridgeAnalysisReportSerializer)
    def get(self, request, bid: int):
        """
        Get bridge by id
        """
        bridge_analysis_report_s = BridgeAnalysisReportService()
        response = bridge_analysis_report_s.get_bridge_report(request, bid)

        if (response["success"]):
            return Response(data= response,
                        status= status.HTTP_201_CREATED)
        else:
            return Response(data= response,
                        status= status.HTTP_404_NOT_FOUND)
    