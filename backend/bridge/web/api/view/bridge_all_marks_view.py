
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from web.api.service.bridge_all_marks_service import BridgeAllMarksService
from user.api.permission.is_admin_or_super_user import IsAdminOrSupoerUser
from web.api.service.bridge_all_marks_service import BridgeAllMarksService
from bridge.utils.swagger_decorator import auto_schema_without_example # import decorator for SwaggerUI Example
# Create your views here.



class BridgeAllMarksView(APIView):

    serializer_class = BridgeAllMarksService
    permission_classes = [IsAdminOrSupoerUser]
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [BridgeListThrottle]

    @auto_schema_without_example()
    def get(self, request):
        """
        Get list of bridge
        """
        bridge_list_s = BridgeAllMarksService()
        response = bridge_list_s.get_bridge_list(request)
        return Response(response,
                        status= status.HTTP_200_OK)

                            
        

        