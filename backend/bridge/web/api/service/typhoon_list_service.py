from web.models import Typhoon, TyphoonEvent, FinalFloodResistance
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from web.api.serializer.typhoon_list_serializer import TyphoonListSerializer
from bridge.utils.response_formatter import ResponseFormatter
from django.db.models import OuterRef, Subquery


class TyphoonListService:
    serializer_class = TyphoonListSerializer

    def get_typhoon_list(self, bid: int, sid: int):
        """
        Query typhoon event-related information for the specified bridge and sensor.
        """

        # 找出特定bid、sensor不重複的event_id
        # .order_by('-event_id') => 降序排列 (DESC)
        event_query = TyphoonEvent.objects.filter(bid=bid, sensor=sid).values('bid', 'sensor', 'event_id').distinct().order_by('-event_id')

        # 進行JOIN操作，查找相關的 Earthquake 和 FinalSeismicResistance 資料
        result = event_query.annotate(
                cht_name=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('cht_name')[:1]),
                eng_name=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('eng_name')[:1]),
                sea_start_datetime=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('sea_start_datetime')[:1]),
                sea_end_datetime=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('sea_end_datetime')[:1]),
                max_intensity=Subquery(Typhoon.objects.filter(id=OuterRef('event_id')).values('max_intensity')[:1]),
                post_event_health=Subquery(FinalFloodResistance.objects.filter(event_id=OuterRef('event_id')).values('post_event_health')[:1]),
                # 新增 time_marker 的 before 和 after 資料
                before=Subquery(TyphoonEvent.objects.filter(event_id=OuterRef('event_id'),time_marker='before').values('up_centroid_frequency')[:1]),
                after=Subquery(TyphoonEvent.objects.filter(event_id=OuterRef('event_id'),time_marker='after').values('up_centroid_frequency')[:1]) 
            ).filter(post_event_health__isnull=False) # 加入篩選條件，排除 post_event_health 為 null 的資料
        

        result_list = list(result)
        for item in result_list:
             # Ensure got both before, after value and caculate frequency_variance_ratio
            before = item.get("before")
            after = item.get("after")
            if (after) and (before):
                item["freqeuncy_variance_ratio"] = int((after / before) * 100) / 100

        serializer = self.serializer_class(result, many= True)    

        if not event_query.exists(): # query結果回傳空值[]，回傳400
            json = ResponseFormatter.format_400_response(serializer.data)
        else:
            json = ResponseFormatter.format_get_response(serializer.data)
            
        return json
