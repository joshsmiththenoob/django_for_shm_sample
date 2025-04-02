from web.models import Earthquake, EarthquakeEvent, FinalSeismicResistance
from web.api.serializer.earthquake_list_serializer import EarthquakeListSerializer
from bridge.utils.response_formatter import ResponseFormatter
from django.db.models import OuterRef, Subquery
from datetime import timedelta


class EarthquakeListService:
    serializer_class = EarthquakeListSerializer

    def get_earthquake_list(self, bid: int, sid: int):
        """
        Query earthquake event-related information for the specified bridge and sensor.
        """

        # 找出特定bid、sensor不重複的event_id
        # .order_by('-event_id') => 降序排列 (DESC)
        event_query = EarthquakeEvent.objects.filter(bid=bid, sensor=sid).values('bid', 'sensor', 'event_id').distinct().order_by('-event_id')

        # 進行JOIN操作，查找相關的 Earthquake 和 FinalSeismicResistance 資料
        result = event_query.annotate(
                origintime=Subquery(Earthquake.objects.filter(earthquakeno=OuterRef('event_id')).values('origintime')[:1]),
                epicenterlocation=Subquery(Earthquake.objects.filter(earthquakeno=OuterRef('event_id')).values('epicenterlocation')[:1]),
                longitude=Subquery(Earthquake.objects.filter(earthquakeno=OuterRef('event_id')).values('longitude')[:1]),
                latitude=Subquery(Earthquake.objects.filter(earthquakeno=OuterRef('event_id')).values('latitude')[:1]),
                magnitudevalue=Subquery(Earthquake.objects.filter(earthquakeno=OuterRef('event_id')).values('magnitudevalue')[:1]),
                depthvalue=Subquery(Earthquake.objects.filter(earthquakeno=OuterRef('event_id')).values('depthvalue')[:1]),
                post_event_health=Subquery(FinalSeismicResistance.objects.filter(event_id=OuterRef('event_id')).values('post_event_health')[:1]),
                # 新增 time_marker 的 before 和 after 資料
                before=Subquery(EarthquakeEvent.objects.filter(event_id=OuterRef('event_id'),time_marker='before').values('up_centroid_frequency')[:1]),
                after=Subquery(EarthquakeEvent.objects.filter(event_id=OuterRef('event_id'),time_marker='after').values('up_centroid_frequency')[:1])
            ).filter(post_event_health__isnull=False) # 加入篩選條件，排除 post_event_health 為 null 的資料


        
        # 將 QuerySet 轉換成 list，並新增 endtime 欄位
        result_list = list(result)
        for item in result_list:
            origintime = item.get('origintime')
            if origintime:  # 確保 'origintime' 存在
                endtime = origintime + timedelta(minutes=2)
                # 將 endtime 加入
                item['endtime'] = endtime.strftime("%Y-%m-%d %H:%M:%S")
            
            # Ensure got both before, after value and caculate frequency_variance_ratio
            before = item.get("before")
            after = item.get("after")
            if (after) and (before):
                item["freqeuncy_variance_ratio"] = int((after / before) * 100) / 100

        serializer = self.serializer_class(result_list, many= True)    

        if not event_query.exists(): # query結果回傳空值[]，回傳400
            json = ResponseFormatter.format_400_response(serializer.data)
        else:
            json = ResponseFormatter.format_get_response(serializer.data)

        return json
