from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from web.api.service.bridge_earthquake_list_service import BridgeEarthquakeListService
from bridge.utils.swagger_decorator import auto_schema_without_example # import decorator for SwaggerUI Example
# Create your views here.

class BridgeEarthquakeListView(APIView):

    permission_classes = [AllowAny]

    @auto_schema_without_example()
    def get(self, request, bid: int):
        try:
            service = BridgeEarthquakeListService()
            response = service.get_earthquake_list(bid= bid)
            if (response["success"]):
                return Response(data= response, 
                                status= status.HTTP_200_OK)
            else:
                return Response(data= response,
                                status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)  