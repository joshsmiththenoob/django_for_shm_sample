import numpy as np
from web.api.handler.chart_drawer import ChartDrawer
from web.api.handler.analysis_report.analysis_report_json_formatter import AnalysisReportJSONFormatter


class StatisticHandler:
    def __init__(self):
        self.__chart_drawer = ChartDrawer()


    def get_statistics_feature_report(self, data: list, feature_name: list, image_index: int, with_trend: bool= False):
        """
        Get statistic value for second chapter report
        """
        print(feature_name)

        mid_feature = f'mid_{feature_name}'
        max_feature = f'max_{feature_name}'
        min_feature = f'min_{feature_name}'
        up_feature = f'up_{feature_name}'
        down_feature = f'down_{feature_name}'


        mid_values = [item[mid_feature] for item in data if item[mid_feature] is not None]
        max_values = [item[max_feature] for item in data if item[max_feature] is not None]
        min_values = [item[min_feature] for item in data if item[min_feature] is not None]
        
        # print("mid_value's len: ", len(mid_values))
        # print("min_values's len: ", len(max_values))
        # print("max_values's len: ", len(min_values))



        time_data = [item['time'] for item in data]
        up_values = [item[up_feature] for item in data]
        down_values = [item[down_feature] for item in data]

        feature_dict = dict()
        feature_dict['Q2'] = round(np.median(mid_values), ndigits= 2) if mid_values else None
        feature_dict['Q4'] = round(np.max(max_values), ndigits= 2) if max_values else None
        feature_dict['Q0'] = round(np.min(min_values), ndigits= 2) if min_values else None
        feature_dict['Q1'] = round(np.percentile(down_values, 25), ndigits= 2) if down_values else None

        
        if (with_trend):
            trend_dict = self.__polyfit(mid_values)
            feature_dict["slope"] = trend_dict["slope"]
            feature_dict["latest_value"] = mid_values[-1]
            fit_curve = trend_dict["fit_curve"]
        else:
            fit_curve = None

        base64_chart = self.__chart_drawer.get_statistic_line_chart_base64(time_data, up_values, mid_values, down_values, feature_name, fit_curve)
        feature_dict['chart'] = AnalysisReportJSONFormatter.get_image_info_dict(base64_chart, image_index)

        if (feature_name != "seismic"):
            feature_dict["variation"] = self.__get_variation_ratio(feature_dict["Q4"], feature_dict["Q0"])
            


        return feature_dict
    

    def __get_variation_ratio(self, max: float, min: float):
        return round((1 - (min / max)) * 100, ndigits= 2)
    

    def __polyfit(self, data: np.array, power: int = 1):
        """
        Curve fitting by power factor
        """
        # get x-axis
        x = np.arange(0, (len(data)))
        param = np.polyfit(x, data, power)

        # get the value of fit curve corresponding to x-axis
        fit_curve = np.polyval(param, x)     
        fit_curve = np.round(fit_curve, 2)

        # get slope when use linear fitting
        slope = round(param[0], ndigits= 6) if power == 1 else None
        

        # format polyfit result
        polyfit_result = dict()
        polyfit_result["fit_curve"] = fit_curve
        polyfit_result["slope"] = slope

        return polyfit_result