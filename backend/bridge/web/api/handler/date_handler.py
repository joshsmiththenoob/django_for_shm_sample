import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class DateHandler():
    def __init__(self) -> None:
        pass


    def get_report_month_str(self, date: datetime):
        year = date.year - 1911
        month = date.month

        return f"{year}年{month:02d}月"
    
    def get_report_month_str_gregorian(self, date: datetime):
        year = date.year
        month = date.month

        return f"{year}年{month:02d}月"


    def get_report_date_str(self, date: datetime):
        report_month_str = self.get_report_month_str(date)
        day = date.day

        return report_month_str + f"{day}日"
        
        
    def get_report_start_time(self, current_time, period_type: str):
        if (period_type == "last_day"):
            return current_time - timedelta(days= 1)
        elif (period_type == "last_month"):
            return current_time - relativedelta(months=1)
        elif (period_type == "last_year"):
            return current_time - relativedelta(years=1)
        
    
    def get_event_time_range(self, current_time: datetime):
        # 計算事件發生前後 5 分鐘
        start_time = current_time - timedelta(minutes=5)
        end_time = current_time + timedelta(minutes=5)

        return start_time, end_time
            
