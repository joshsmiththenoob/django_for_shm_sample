from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from bridge.utils.swagger_decorator import auto_schema_without_example
from user.api.service.group_urls_service import GroupUrlsService

class GroupUrlsView(APIView):
    permission_classes = [IsAuthenticated]

    @auto_schema_without_example()
    def get(self, request):
        group_urls_s = GroupUrlsService()

        response = group_urls_s.get_path_element_by_group(request)

        if (response["success"]):
            return Response(data= response,
                        status= status.HTTP_201_CREATED)
        elif(response["success"] == False and response["success"] == "Error, Interval Server Error!"):
            return Response(data= response,
                        status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data= response,
                        status= status.HTTP_500_INTERNAL_SERVER_ERROR)