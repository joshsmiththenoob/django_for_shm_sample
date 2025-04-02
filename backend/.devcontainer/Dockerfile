# 使用 Python 3.12 映像
FROM python:3.12-slim

# 設置工作目錄
WORKDIR /app

# 複製需求文件
COPY requirements.txt /app/

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案檔案
COPY . /app/

# 開放 Django 的預設埠
EXPOSE 8000

# 啟動伺服器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
