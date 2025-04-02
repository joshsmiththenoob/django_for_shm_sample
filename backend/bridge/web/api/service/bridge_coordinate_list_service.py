from web.models import Bridge, AuthAgencyUsers, AuthAgencyBridges
from web.api.serializer.bridge_coordinate_serializer import BridgeCoordinateSerializer
from bridge.utils.response_formatter import ResponseFormatter

class BridgeCoordinateListService:
    serializer_class = BridgeCoordinateSerializer
    def get_bridge_coord_list(self, request):
        # # Get AuthAgencyBridgesORM Object about Bridge managed by AuthAgencyBridgesManger (check models.py for details)
        # agency_bridge_qs = AuthAgencyBridges.objects.for_user(request.user)
        # # get ORM object of query result
        # bridge_ids = agency_bridge_qs.values_list('bridge_id', flat=True)
        user = request.user
        
        if (user.is_superuser):
            # Admin sees all non-deleted bridges
            bridge_objects = Bridge.objects.filter(deleted=0)
        else:
            # Regular users see bridges related through AuthAgencyBridges
            bridge_ids = AuthAgencyBridges.objects.filter(
                agency__authagencyusers__user=user,
                bridge__deleted=0
            ).values_list('bridge_id', flat=True).distinct()
            bridge_objects = Bridge.objects.filter(id__in=bridge_ids)


        try:
            result = bridge_objects.values("id", "type", "bno", "name", "longitude", "latitude", "address_name", "id_address_name", "photo_name")
            serializer = self.serializer_class(instance= result, many= True)
            json = ResponseFormatter.format_get_response(serializer.data)
            
        except Exception as e:
            print(e)
            json = ResponseFormatter.format_500_response()

        return json