# Image Handler: Duty on Saving, Deleting Image
import os
import base64
import io
from io import BytesIO
import time
from PIL import Image, ImageDraw
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
import matplotlib
from shapely.geometry import Point

matplotlib.rc('font', family='Microsoft JhengHei')


class ImageHandler:
    def __init__(self) -> None:
        pass

    def delete_img(self, image_dir: str, file_name: str):
        """
        delete old img from server' image directory path
        """
        print("執行刪除")
        # delete old img if it's existed
        file_location = os.path.join(image_dir, file_name)
        print(file_location)
        if os.path.exists(file_location):
            os.remove(file_location)
            print("刪除成功")
        

    def check_extension(self, pic_file):
        """
        check if file extension is JPG or not
        """
        if pic_file.content_type != "image/jpeg":
            raise TypeError("Wrong picture type. Please using JPG file instead")


    def save_img(self, image_dir: str, pic_file, pic_name: str = None, size= (760, 235)):
        """
        save img to server's image directory path
        """

        # ensure dir is existed, create if not
        self.__make_dir(image_dir)
        # build file path for saving image
        if (not pic_name):
            file_location = os.path.join(image_dir, pic_file.name)
        else:
            file_location = os.path.join(image_dir, pic_name)
    
        print(file_location)
        # check if same file name exsited or not
        if os.path.exists(file_location):
            raise FileExistsError(f"Image '{pic_file.name}' exsited! Please change file name.")
       
        # open uploaded image and save it to file location
        with Image.open(pic_file.file) as img:
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(file_location)
            print("saving completed")

        ## check if aspect-ratio of picture is correct
        # with Image.open(pic_file.file) as img:
        #     original_width = img.size[0]
        #     original_height = img.size[1]
        #     if (self.__is_aspect_ratio_correct(original_width, original_height)):
        #         img = img.resize(size, Image.Resampling.LANCZOS)
        #         img.save(file_location)
        #         print("saving completed")
        #     else:
        #         raise ValueError("Aspect ratio of photo is not available for website. Please make sure aspect ratio is around 3.23 / 1") 

    def convert_img_into_base64(self, pic_file):
        """
        convert img into base64
        """
        # base64_img = base64.b64encode(pic_file.read()).decode("utf-8")
        pic_file.seek(0)  # 確保從檔案開頭開始讀取
        try:
            base64_img = base64.b64encode(pic_file.read()).decode("utf-8")
            return base64_img
        except Exception as e:
            print("Failed to convert img into base64: ", e)
            raise e

        # return base64_img
    

    def get_file_name(self, pic_file):
        print("取得檔案名稱")
        return pic_file.name
        

    def get_image_with_sensor_mark(self, image_base64: str, x: float, y: float):
        """
        Load image and mark image with x, y ratio (upper-left origin).
        Return image base64 with green dot.
        """
        # Change x%, y% into float(ratio)
        x = x / 100
        y = y / 100

        # 將 base64 字串轉為圖片物件
        image_data = base64.b64decode(image_base64)
        image_stream = io.BytesIO(image_data)
        with Image.open(image_stream) as img:
            draw = ImageDraw.Draw(img)
            width, height = img.size
            print(width, height)
            real_x = x * width
            real_y = y * height
            print(real_x, real_y)
            # time.sleep(5)
            
            radius = 8
            # draw.ellipse(
            #     (real_x - radius, real_y - radius, real_x + radius, real_y + radius),
            #     fill="lime"
            # )

            draw.ellipse(
                    (real_x, real_y, real_x + 2*radius, real_y + 2*radius),
                    fill="red"
                )
            # 轉回 base64
            buffer = io.BytesIO()
            img.save(buffer, format='png')  # 用 JPEG 比較節省空間
            buffer.seek(0)
            return self.convert_img_into_base64(buffer)
        


    def __make_dir(self, path: str):
        """
        make directory if not specific directory in path
        """
        if not os.path.exists(path):
            os.makedirs(path)


    def __is_aspect_ratio_correct(self, original_width: int, original_height: int, aspect_ratio: float= 3.23):
        # Get aspect ratio
        original_aspect_ratio = int((original_width / original_height) * 100) / 100
        print(original_aspect_ratio)

        if (original_aspect_ratio == 3.22):
            original_aspect_ratio = round(original_aspect_ratio + 0.01, ndigits= 2)
        elif(original_aspect_ratio == 3.24):
            original_aspect_ratio = round(original_aspect_ratio - 0.01, ndigits= 2)
        
        if (original_aspect_ratio == aspect_ratio):
            return True
        else:
            return False
        
    def get_image_with_bridge_location(self, longitude: float, latitude: float, title: str=None):
        # 創建地標點
        data = {'name': [title],
                'latitude': [latitude],
                'longitude': [longitude]}

        # 轉換為 GeoDataFrame
        gdf = gpd.GeoDataFrame(data, geometry=[Point(xy) for xy in zip(data['longitude'], data['latitude'])])

        # 設定座標系統 (WGS 84)
        gdf.set_crs(epsg=4326, inplace=True)

        # 轉換為 Web Mercator（EPSG:3857）以搭配 contextily
        gdf = gdf.to_crs(epsg=3857)

        # 設定圖片比例（放大到城市街道層級）
        fig, ax = plt.subplots(figsize=(10, 10))

        # 畫出地標點
        gdf.plot(ax=ax, color='red', markersize=200, alpha=0.8, edgecolor='black')

        # 顯示地標名稱
        # for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['name']):
        #     ax.text(x, y, label, fontsize=12, ha='right', color='black', bbox=dict(facecolor='white', alpha=0.5))

        # 顯示經緯度
        for x, y, lon, lat in zip(gdf.geometry.x, gdf.geometry.y, data['longitude'], data['latitude']):
            ax.text(x-200, y-100, f"({lon:.4f}, {lat:.4f})", fontsize=12, ha='left', va='bottom',
                    color='black', bbox=dict(facecolor='white', alpha=0.7, edgecolor='black'))

        # 設定地圖縮放到座標附近
        ax.set_xlim([gdf.geometry.x[0] - 1000, gdf.geometry.x[0] + 1000])  # 左右各 1000m
        ax.set_ylim([gdf.geometry.y[0] - 1000, gdf.geometry.y[0] + 1000])  # 上下各 1000m

        # 加入高解析度街道底圖
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

        # 移除 X/Y 軸座標數值
        ax.set_xticks([])  # 移除 X 軸刻度
        ax.set_yticks([])  # 移除 Y 軸刻度
        # ax.set_frame_on(False)  # 移除邊框

        # 標題
        # plt.xlabel("Longitude")
        # plt.ylabel("Latitude")
        if title :
            # plt.title(title)
            ax.set_title(title, fontsize=18) 

        # plt.show()

        # 儲存到記憶體
        buffer = BytesIO()
        # plt.savefig(buffer, format="png")
        plt.savefig(buffer, format="jpg")
        buffer.seek(0)
        plt.close()

        return self.convert_img_into_base64(buffer)
