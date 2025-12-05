import pandas as pd
import numpy as np
import utils.find_anomal as FA
from utils.get_report import get_report


def Grid_Search(RPT_MODE, time_lower, time_upper, SOC_size = 4, X = None, Y = None):
    if X is None or Y is None:
        X = FA.X
        Y = FA.Y_tot

    r_list = []
    a_list = []

    SOC_Range = range(SOC_size + 1)
    report = get_report(X, Y, RPT_MODE, time_lower, time_upper, SOC_Range)

    row_idx = []
    r_data = []
    a_data = []
    for r in report :
        row_idx.append(r.title)
        r_data.append(r.r_values)
        a_data.append(r.anomal_error_ratio)
        col_idx = r.y_name
        
    report_r_max = pd.DataFrame(r_data, index = row_idx, columns = col_idx)
    report_a_min = pd.DataFrame(a_data, index = row_idx, columns = col_idx)

    r_list.append(report_r_max)
    a_list.append(report_a_min)

    max_index_r = report_r_max.copy()
    max_index_r.loc[:,:] = 0

    min_index_a = report_a_min.copy()
    min_index_a.loc[:,:] = 0


    for i in range(1,18-SOC_size) :
        SOC_Range = [j for j in range(i,i+SOC_size)]

        report = get_report(X, Y, RPT_MODE, time_lower, time_upper, SOC_Range)
        
        row_idx = []
        r_data = []
        a_data = []
        for r in report :
            row_idx.append(r.title)
            r_data.append(r.r_values)
            a_data.append(r.anomal_error_ratio)
            col_idx = r.y_name
            
        report_r_new = pd.DataFrame(r_data, index = row_idx, columns = col_idx)
        report_a_new = pd.DataFrame(a_data, index = row_idx, columns = col_idx)
        
        r_list.append(report_r_new)
        a_list.append(report_a_new)
        
        report_r_max = report_r_new.combine(report_r_max, np.minimum)
        report_a_min = report_a_new.combine(report_a_min, np.minimum)
        
        max_index_r[report_r_new == report_r_max] = i
        min_index_a[report_a_new == report_a_min] = i

    return row_idx, col_idx, r_list, a_list, report_r_max, report_a_min
   
    
if __name__ == "__main__":
    RPT_MODE = "0.1C"

    time_lower = 4
    time_upper = 36

    row_idx, col_idx, r_list, a_list, report_r_max, report_a_min = Grid_Search(RPT_MODE, time_lower, time_upper, SOC_size=4)

    print("--- Time Range ---")
    print(str(time_lower) + ' to ' + str(time_upper))
    print("------------------\n")

    print(report_r_max)


    
