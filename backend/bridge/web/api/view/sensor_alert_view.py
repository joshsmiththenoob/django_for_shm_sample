from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from web.api.serializer.sensor_alert_serializer import SensorAlertSerializer
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.sensor_alert_service import SensorAlertService
from bridge.utils.swagger_decorator import auto_schema_without_example # import decorator for SwaggerUI Example
# Create your views here.



class SensorAlertView(APIView):

    serializer_class = SensorAlertSerializer
    permission_classes = [IsAdminOrSupoerUser]

    @auto_schema_without_example()
    def get(self, request):
        try:
            service = SensorAlertService()
            result = service.get(request)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     

        