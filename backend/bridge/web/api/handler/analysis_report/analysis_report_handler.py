#   Deal with Analysis Report
from web.api.handler.analysis_report.first_chapter.first_chapter_handler import FirstChapterHandler
from web.api.handler.analysis_report.second_chapter.second_chapter_handler import SecondChapterHandler
from web.api.handler.analysis_report.third_chapter.earthquake_report_handler import EarthquakeReportHandler
from web.api.handler.analysis_report.third_chapter.typhoon_report_handler import TyphoonReportHandler
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import time


class AnalysisReportHandler:

    def __init__(self):
        self.image_index = 1 # Initalize index of image to record on analysis report
    
    def get_report(self, user: User, bid: int, date: datetime):
        report = dict()

        self.__first_chap_handler = FirstChapterHandler(self.image_index)
        report["report_basic_data"] = self.__first_chap_handler.get_report(user, bid, date)
        self.image_index = self.__first_chap_handler.get_current_image_index()
        print(self.image_index)

        self.__second_chap_handler = SecondChapterHandler(self.image_index)
        report["report_second_data"] =  self.__second_chap_handler.get_last_day_report(user, bid, date)
        self.image_index = self.__second_chap_handler.get_current_image_index()
        print("repot_basic_data Finished")

        self.__second_chap_handler.set_current_image_index(self.image_index)
        report["report_month_data"] =  self.__second_chap_handler.get_last_month_report(user, bid, date)
        self.image_index = self.__second_chap_handler.get_current_image_index()
        print("repot_month_data Finished")

        self.__second_chap_handler.set_current_image_index(self.image_index)
        report["report_year_data"] =  self.__second_chap_handler.get_last_year_report(user, bid, date)
        self.image_index = self.__second_chap_handler.get_current_image_index()
        print("repot_year_data Finished")

        self.__earthquake_report_handler = EarthquakeReportHandler(self.image_index)
        report["report_earthquake_data"] =  self.__earthquake_report_handler.get_report(user, bid, date)
        self.image_index = self.__earthquake_report_handler.get_current_image_index()
        print("report_earthquake_data Finished")

        self.__typhoon_report_handler = TyphoonReportHandler(self.image_index)
        report["report_typhoon_data"] =  self.__typhoon_report_handler.get_report(user, bid, date)
        self.image_index = self.__typhoon_report_handler.get_current_image_index() 
        print("report_typhoon_data Finished")

        #Create last chapter dictionary so that AI message in report_second_data could migrate into it
        report["conversation"] = report["report_second_data"].pop("ai_report_messages")

        
        return report
    
