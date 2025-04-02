# import os
# from dotenv import load_dotenv
# import cohere
# import sys

# # 設定輸出編碼，避免中文亂碼
# sys.stdout.reconfigure(encoding='utf-8')

# # 載入 .env 檔案
# load_dotenv()
# # 取得 Cohere API Key
# cohere_api_key = "oJWHRW8daqkUb2kZoIOjyknP044lSRYBNrkPWl4e"
# if not cohere_api_key:
#     print("API Key 未設定，請確認 .env 檔案內有 COHERE_API_KEY")
#     sys.exit(1)

# # 初始化 Cohere 客戶端
# co = cohere.Client(cohere_api_key)

# def GET_RESULT(ropes):
#     try:
#         if not ropes:
#             print("鋼索資料不可為空")
#             return

#         # 組合多條鋼索的資訊
#         rope_details = "\n".join(
#             [f"鋼索編號 {r['Rope_No']} 之受力狀態為 {r['Rope_Status']}，四分位數 (S_Q1) 為 {r['Alern_status']}，評估結果為 {r['Evaluate_Result']}。" for r in ropes]
#         )

#         # 優化 Prompt，要求總結多條鋼索的安全評估
#         prompt = f"""
#         **請用中文回答**
#         以下是多條鋼索的受力狀態與安全評估結果：
#         {rope_details}
#         這是一份安全評估報告請根據以上資訊提供一個客觀結論，並指出整體的安全狀況與建議。
#         """

#         # 使用 Cohere API 生成回應
#         response = co.generate(
#             model='command',  # 使用 Command-R 模型增強準確性
#             prompt=prompt,
#             max_tokens=500,
#             temperature=0  # 降低隨機性，提高精確度
#         )

#         summary = response.generations[0].text.strip()
#         print(f"{summary}")
#         return summary

#     except Exception as e:
#         print(f"其他錯誤: {str(e)}")

# # 測試函式呼叫
# ropes_data = [
#     {"Rope_No": "001", "Rope_Status": "未有異常", "Alern_status": "高於告警值(90)", "Evaluate_Result": "良好，建議維持現有監測頻率"},
#     {"Rope_No": "002", "Rope_Status": "未有異常", "Alern_status": "高於告警值(90)", "Evaluate_Result": "良好，建議維持現有監測頻率"},
#     {"Rope_No": "003", "Rope_Status": "些微異常", "Alern_status": "低於告警值(90)", "Evaluate_Result": "需警戒，橋梁狀態需密集關注"},
#     # {"Rope_No": "004", "Rope_Status": "異常", "Alern_status": "低於告警值(90)", "Evaluate_Result": "須採取管制行動，建議請專業技師評估補強之必要"}
    
# ]
# # 
# GET_RESULT(ropes_data)



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

class RopeEvaluationView(View):
    def get(self, request):
        try:
            # 直接從 function 獲取 ropes 資料
            ropes = get_ropes_data()  # 確保這個 function 能返回正確的格式

            if not ropes:
                return JsonResponse({"error": "鋼索資料不可為空"}, status=400)
            
            # 組合多條鋼索的資訊
            rope_details = "\n".join(
                [f"鋼索編號 {r['detailed_location']} 之受力狀態為 {r['status']}，四分位數 (S_Q1) 為 {r['alert_status']}，評估結果為 {r['evaluate_result']}。" for r in ropes]
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
            return JsonResponse({"summary": summary})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)