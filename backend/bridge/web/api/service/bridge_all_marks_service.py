from web.models import AuthAgencyUsers, AuthAgencyBridges
from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.bridge_all_marks_serializer import BridgeAllMarksSerializer

"""
The rule of Reponse Body structure:
{
    "success"(boolean): if client get response successful or not
    "message"(string):  message detail
    "data"(any): return data
}

"""

class BridgeAllMarksService:
    serializer_class = BridgeAllMarksSerializer
    def __init__(self):
        pass
    def get_bridge_list(self, request):
        """
        Get list of bridge
        """
        # get group ORM object of request user        
        user_id = request.user.id

        # get ORM object which user_id == user_id and search specific attribute agency object first
        agency_results = AuthAgencyUsers.objects.filter(user_id= user_id).select_related('agency')
        a_id = agency_results[0].agency.id

        # get ORM object of query result
        results = AuthAgencyBridges.objects.filter(agency_id= a_id).select_related("bridge")

        # Extract the bridge objects from results
        bridge_objects = [result.bridge for result in results if result.bridge.deleted == 0] # bridge.deleted == 1 為刪除橋梁，故不顯示

        # set argument:many to True for getting multiple results from ORM objects
        serializer = self.serializer_class(instance= bridge_objects, many= True) 
        # QuerySet.values() returns a type like list but still a QuerySet object
        # Need to change data type from QuerySet objects to list, and get involved by dict we created

        # form json
        json = ResponseFormatter.format_get_response(serializer.data)

        return json

    def __add_relation_between_agency_and_bridge(self, request, new_bridge):
        # get group ORM object of request user        
        user_id = request.user.id

        # get ORM object which user_id == user_id and search specific attribute agency object first
        agency_results = AuthAgencyUsers.objects.filter(user_id= user_id).select_related('agency')
        a_id = agency_results[0].agency.id

        AuthAgencyBridges.objects.create(agency_id= a_id, bridge_id= new_bridge.id)