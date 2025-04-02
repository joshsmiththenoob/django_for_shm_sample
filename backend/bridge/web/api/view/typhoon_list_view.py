from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from web.api.serializer.typhoon_list_serializer import TyphoonListSerializer
from web.api.service.typhoon_list_service import TyphoonListService
from bridge.utils.swagger_decorator import auto_schema_without_example # import decorator for SwaggerUI Example
# Create your views here.



class TyphoonListView(APIView):

    serializer_class = TyphoonListSerializer
    permission_classes = [AllowAny]

    @auto_schema_without_example()
    def get(self, request, bid: int, sid: int):
        try:
            service = TyphoonListService()
            response = service.get_typhoon_list(bid= bid, sid= sid)
            if (response["success"]):
                return Response(data= response, 
                                status= status.HTTP_200_OK)
            else:
                return Response(data= response,
                                status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)  