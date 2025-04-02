from dotenv import load_dotenv
from script.api_client.cwa_api_client import CWAAPIClient
import os


if __name__ == "__main__":
    url = os.getenv("CWA_API_STATION_INFO_URL")
    client = CWAAPIClient(url)
    client.update_station_info(120.995, 24.7851)
