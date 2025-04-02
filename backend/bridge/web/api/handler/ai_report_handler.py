

import os
from dotenv import load_dotenv
import cohere
from django.http import JsonResponse
from django.views import View

# 載入 .env 檔案
load_dotenv()

# 取得 Cohere API Key
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("API Key 未設定，請確認 .env 檔案內有 COHERE_API_KEY")

# 初始化 Cohere 客戶端
co = cohere.Client(cohere_api_key)

class AIReportHandler(View):
    
    def get_ai_results(self, sensor_results: list):
        try:
            # 直接從 function 獲取 ropes 資料
            ropes = self.__parse_sensor_message(sensor_results)  # 確保這個 function 能返回正確的格式

            if not ropes:
                return "鋼索資料不可為空"  # 如果沒有資料，直接返回錯誤信息作為字符串
            
            # 組合多條鋼索的資訊
            rope_details = "\n".join(
                [f"鋼索編號 {r['Rope_No']} 之受力狀態為 {r['Rope_Status']}，四分位數 (S_Q1) 為 {r['Alern_status']}，評估結果為 {r['Evaluate_Result']}。" for r in ropes]
            )

            # 優化 Prompt
            prompt = f"""
            **請用中文回答**
            以下是多條鋼索的受力狀態與安全評估結果：
            {rope_details}
            
            請根據以上資訊提供一個結論，指出整體的安全狀況與建議。
            """

            # 使用 Cohere API 生成回應
            response = co.generate(
                model='command',
                prompt=prompt,
                max_tokens=500,
                temperature=0
            )

            summary = response.generations[0].text.strip()
            summary = summary.replace("\n", "")
            return summary  # 直接返回生成的摘要文字

        except Exception as e:
            print(f"Error: {e}")  # 或 logging.error(e)
            return ""  # 其他錯誤直接返回
        
        

    def __parse_sensor_message(self, sensor_results: list):
        """
        Reformat the sensor list to ropes information
        """
        ropes = []
        for sensor in sensor_results:
            rope = {
                "Rope_No": sensor.get("detailed_location", ""),  
                "Rope_Status": sensor.get("sensor_feature", {}).get("result_message", ""),  
                "Alern_status": sensor.get("health", {}).get("alert_message", ""),  
                "Evaluate_Result": sensor.get("health", {}).get("result_message", "")  
            }
            ropes.append(rope)
        return ropes