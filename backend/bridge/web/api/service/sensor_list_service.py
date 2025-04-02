from web.models import Sensor
from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.sensor_name_serializer import SensorNameSerializer
from django.db.models import Max

"""
The rule of Reponse Body structure:
{
    "success"(boolean): if client get response successful or not
    "message"(string):  message detail
    "data"(any): return data
}

"""

class SensorListService:
    serializer_class = SensorNameSerializer

    def create_new_sensor(self, request, bid: int):
        """
        Create a new sensor
        """

        request.data["bid"] = bid
        max_sensor = Sensor.objects.filter(bid=bid).aggregate(Max('sensor'))
        
        if (max_sensor["sensor__max"]): # 若橋梁有感測器，以最新的感測器編號 + 1
            request.data["sensor"] = max_sensor["sensor__max"] + 1
        else: # 若橋梁無感測器，則感測器編號為 1
            request.data["sensor"] = 1

        serializer = self.serializer_class(data= request.data)
        request_data = request.data.copy()
        # form json
        if serializer.is_valid():
            # save & return new object
            new_sensor = serializer.create(serializer.validated_data)
            json = ResponseFormatter.format_post_response(request_data)
        else:
            json = ResponseFormatter.format(False, "Error, Bad Request!", serializer.errors)

        return json