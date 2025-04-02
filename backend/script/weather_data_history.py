from dotenv import load_dotenv
from script.api_client.cwa_api_client import CWAAPIClient


if __name__ == "__main__":
    start_time = "2024-08-01 00:00:00"
    end_time = "2025-02-17 23:59:59" 
    
    client = CWAAPIClient()
    station_id_list = ["C0C620", "C0C720", "C0D660"]

    # Duration between starttime and endtime should less than 31 days.
    month_range_list = client.split_time_by_month(start_time, end_time)

    for month in month_range_list:
        start_date = month.get('month_start')
        end_date = month.get('month_end')
        # print(month)

        for station_id in station_id_list:
            # get weather station data
            response = client.get_batch_history_weather_data(start_date, end_date, station_id)
            print(response)



