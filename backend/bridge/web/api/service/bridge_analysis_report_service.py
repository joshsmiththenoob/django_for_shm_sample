
import calendar
from web.models import Bridge, Sensor
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework.request import Request
from bridge.utils.response_formatter import ResponseFormatter
from web.api.serializer.bridge_analysis_report_serializer import BridgeAnalysisReportSerializer
from web.api.handler.image_handler import ImageHandler
from web.api.handler.date_handler import DateHandler
from web.api.handler.analysis_report.analysis_report_handler import AnalysisReportHandler
from datetime import datetime, timedelta



class BridgeAnalysisReportService:
    serializer_class = BridgeAnalysisReportSerializer

    def __init__(self):
        self.image_index = 0 # Initalize index of image to record on analysis report
        self.report_handler = AnalysisReportHandler()
    def get_bridge_report(self, request: Request, bid: int):
        # parse query params
        report_month = request.GET.get('report-month')
        
        # get last day of the month
        year, month = map(int, report_month.split('-'))
        last_day = calendar.monthrange(year, month)[1]
        report_date = datetime(year, month, last_day)

        # Get User
        user = request.user

        # try:
        # Get first chapter 

        bridge_info_dict = self.report_handler.get_report(user, bid, report_date)

        # print(bridge_info_dict)

        # serialize data
        serializer = BridgeAnalysisReportSerializer(data= bridge_info_dict)

        if serializer.is_valid():
            json = ResponseFormatter.format_get_response(serializer.data)
        else:
            print(serializer.errors)
            json = ResponseFormatter.format_400_response(serializer.data)

        # except Exception as e:
            # print(e)
            # json = ResponseFormatter.format_500_response()

        return json