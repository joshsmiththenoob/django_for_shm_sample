# from . import views
from django.urls import path
from .view.bridge_list_view import BridgeListView
from .view.bridge_view import BridgeView
from .view.bridge_coordinate_list_view import BridgeCoordinateListView
from .view.bridge_index_info_view import BridgeIndexInfoView
from .view.bridge_all_marks_view import BridgeAllMarksView
from .view.sensor_history_view import SensorHistoryView
from .view.earthquake_list_view import EarthquakeListView
from .view.typhoon_list_view import TyphoonListView
from .view.sensor_list_view import SensorListView
from .view.sensor_view import SensorView
from .view.sensor_data_report_view import SensorDataReportView
from .view.sensor_alert_view import SensorAlertView
from .view.project_list_view import ProjectListView
from .view.bridge_data_report_view import BridgeDataReportView
from .view.bridge_history_view import BridgeHistoryView
from .view.bridge_analysis_report_view import BridgeAnalysisReportView
from .view.bridge_earthquake_list_view import BridgeEarthquakeListView

urlpatterns = [
    path("bridges/", BridgeListView.as_view(), name = "bridge-list"),
    path("bridges/<int:id>/", BridgeView.as_view(), name= "bridge-detail"), # only receive integer value of path variable id
    path("bridges/coordinates/", BridgeCoordinateListView.as_view(), name= "bridge-coordinate-list"), # only receive integer value of path variable id
    path("bridges/information/<int:id>/", BridgeIndexInfoView.as_view(), name = "bridge-infomation"),
    # path('agency/', views.UserReview.as_view(), name='sbridge-detail-by-name'),
    path("marks/", BridgeAllMarksView.as_view(), name = "bridge-list"),
    path("bridges/<int:bid>/sensors/<int:sid>/history-trend/", SensorHistoryView.as_view(), name = "bridge-list"),
    path("bridges/<int:bid>/sensors/<int:sid>/earthquake-history/", EarthquakeListView.as_view(), name = "earthquake-list"),
    path("bridges/<int:bid>/sensors/<int:sid>/typhoon-history/", TyphoonListView.as_view(), name = "typhoon-list"),
    path("bridges/<int:bid>/sensors/", SensorListView.as_view(), name = "sensor-list"),
    path("bridges/<int:bid>/sensors/<int:sid>/", SensorView.as_view(), name = "sensor-detail"),
    path("bridges/<int:bid>/sensors/<int:sid>/data-report/", SensorDataReportView.as_view(), name = "data-report"),
    path("bridges/sensors/alert/", SensorAlertView.as_view(), name = "sensor-alert"),
    path("projects/", ProjectListView.as_view(), name = "project-list"),
    path("bridges/<int:bid>/data-report/", BridgeDataReportView.as_view(), name = "bridge-data-report"),
    path("bridges/<int:bid>/history-trend/", BridgeHistoryView.as_view(), name = "bridge-history_Trend"),
    path("bridges/<int:bid>/analysis-report/", BridgeAnalysisReportView.as_view(), name = "report-creation"),
    path("bridges/<int:bid>/earthquake-history/", BridgeEarthquakeListView.as_view(), name = "bridge-earthquake-list"),
    
] 
