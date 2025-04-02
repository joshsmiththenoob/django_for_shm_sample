from web.models import Sensor
from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.sensor_name_serializer import SensorNameSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

"""
The rule of Reponse Body structure:
{
    "success"(boolean): if client get response successful or not
    "message"(string):  message detail
    "data"(any): return data
}

"""

class SensorService:
    serializer_class = SensorNameSerializer

    def update_sensor(self, request, bid: int, sid: int):
        """
        Update sensor
        """
        # form json
        json = dict()

        try: 
            request.data["bid"] = bid
            request.data["sensor"] = sid

            result = get_object_or_404(Sensor, bid= bid, sensor= sid)
            # update new content to old data(record)
            serializer = self.serializer_class(instance= result, data= request.data)

            if serializer.is_valid():
                serializer.save()
                
                # 確認資料庫是否已更新
                updated_sensor = Sensor.objects.get(bid=bid, sensor=sid)
                print(updated_sensor)

                json["success"] = True
                json["message"] = "Update data successfully"
                json["data"] = serializer.validated_data
            else:
                json["success"] = False
                json["message"] = "Error, Bad Request!"
                json["data"] = serializer.errors

        except Exception as e:
            json["success"] = False
            json["message"] = str(e)
            json["data"] = None
        

        return json
    
    def delete_sensor(self, bid: int, sid: int):
        """
        Delete sensor
        """
        
        json = dict()

        try: 
            # 找到特定的 Sensor
            sensor = get_object_or_404(Sensor, bid=bid, sensor=sid)

            # 更改 'deleted' 欄位為 1 # add deleted tag
            sensor.deleted = 1
            sensor.save()
		        
            json["success"] = True
            json["message"] = "Sensor deleted successfully"
            json["data"] = None

        except Exception as e:
            json["success"] = False
            json["message"] = str(e)
            json["data"] = None
    
        return json