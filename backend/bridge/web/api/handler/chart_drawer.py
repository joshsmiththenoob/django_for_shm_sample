import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from datetime import datetime, timedelta
import time
from web.api.handler.image_handler import ImageHandler
import pandas as pd



class ChartDrawer:
    def __init__(self):
        self.__image_handler = ImageHandler()

    def get_statistic_line_chart_base64(self, time: list, up_dataset: list, mid_dataset: list, down_dataset: list, title: str, fit_curve: list= None):
        """
        Draw Q1, Q2, Q3 of specific feature as title
        """
        plt.figure(figsize=(10, 4))

        # 調整圖的背景與風格
        ax = plt.gca()
        ax.set_facecolor('#000000')  # 深灰色背景
        # 淺色虛線網格
        ax.grid(color='white', linestyle='--', linewidth=0.6, alpha=0.7)

        # plt.plot(time, up_dataset, label='Q1', color='#00BFFF', linewidth=0.5)    # 淺藍色
        plt.plot(time, mid_dataset, label='Q2', color='#FF4B4B', linewidth=0.8)  # 亮紅
        # plt.plot(time, down_dataset, label='Q3', color='#7CFC00', linewidth=0.5)  # 淺綠色
        if (fit_curve is not None):
            plt.plot(time, fit_curve, label='Trend', color='yellow', linewidth=1.5, linestyle= "--")  # 亮紅

        
        # # 改為散點圖
        # plt.scatter(time, up_dataset, label='Q1', color='#00BFFF', s= 5)     # 淺藍點
        # plt.scatter(time, mid_dataset, label='Q2', color='#FF4B4B', s= 5)   # 亮紅點
        # plt.scatter(time, down_dataset, label='Q3', color='#7CFC00', s= 5) # 淺綠點

        plt.xlabel('Time')
        plt.ylabel(title)
        plt.title(f'{title.capitalize()} Line Chart')
        plt.legend()
        

        # 圖例
        legend = plt.legend()
        for text in legend.get_texts():
            text.set_color("white")

        # 軸刻度顏色
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')


        # 邊框顏色
        for spine in ax.spines.values():
            spine.set_edgecolor('white')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()

        return self.__image_handler.convert_img_into_base64(buffer)
    

    def get_event_table_image_base64(self, event_dataset: list, title: str = None):
        """
        Draw table of event and return base64 encode

        args:
            1. headers: list
            2. rows: list of record : [111025, 康瑞颱風]
            3. title: title
        """
        headers = []
        rows = []

        if title == "earthquake":
            headers = ["earthquake id ", "start time", "end time"]
            for e in event_dataset:
                # start_time = e.origintime
                # end_time = e.origintime + timedelta(minutes=2)
                start_time = e['start_time']
                end_time = e['end_time']
                rows.append([e['event_id'], start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S")])

        elif title == "typhoon":
            headers = ["typhoon name", "start time", "end time"]
            for t in event_dataset:
                rows.append([
                    t['cht_name'],
                    t['start_time'].strftime("%Y-%m-%d %H:%M:%S") if t['start_time'] else "N/A",
                    t['end_time'].strftime("%Y-%m-%d %H:%M:%S") if t['end_time'] else "N/A"
                ])
        else:
            headers = ["無法識別的類型"]
            rows = [["請傳入正確的 title 參數，例如 'earthquake' 或 'typhoon'"]]



        plt.figure(figsize=(len(headers) * 1.2, len(rows) * 0.5 + 1))
        ax = plt.gca()
        ax.axis('off')  # 不要顯示坐標軸

        # 設定標題
        plt.title(title, fontsize=14)

        # 建立表格
        table = ax.table(
            cellText=rows,
            colLabels=headers,
            cellLoc='center',
            loc='center'
        )
        table.scale(1, 1.5)  # 可根據需要調整寬高

        # 存圖轉 base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
        plt.close()
        buffer.seek(0)

        return self.__image_handler.convert_img_into_base64(buffer)
    
