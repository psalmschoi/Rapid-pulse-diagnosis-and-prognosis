import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utils.find_anomal as FA
from utils.get_result import get_result
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from scipy import stats


def get_report(X, Y, RPT_MODE = "0.1C", time_lower = 4, time_upper = 30, SOC_Range = [8, 9, 10, 11]) :

    SOC_Range = [str(i) for i in SOC_Range]
    Report = []
    
    X_seek = X.loc[X.index.get_level_values('Time').isin(range(time_lower, time_upper+1, 2)), SOC_Range]
    
    X_seek_mean = X_seek.groupby(level = ['Path', 'Next', 'Number']).mean()
    X_seek_std = X_seek.groupby(level = ['Path', 'Next', 'Number']).std()
    
    
    
    ### PLOT PART ###
    
    y_name = np.array([["SOH", "Next_SOH"], ["Ratio_SOH","Ratio_CYC"]])
    anomal = {"SOH" : FA.Anomal_NOW, "Next_SOH" : FA.Anomal_NEXT, "Ratio_SOH" : FA.Anomal_SOH, "Ratio_CYC" : FA.Anomal_CYC}
    
    
    ### MEAN for Whole Data ###
    
    title = "< " + RPT_MODE + " " + "MEAN" + " >"
    Report.append(get_result(k = 1, X = X_seek_mean, Y = Y, y_name = y_name, anomal = anomal, title = title))
    
    
    
    
    ### STD for Whole Data ###
    
    title = "< " + RPT_MODE + " " + "STD" + " >"
    Report.append(get_result(k = 2, X = X_seek_std, Y = Y, y_name = y_name, anomal = anomal, title = title))
    
    
    ### MEAN for Subdata ###
    
    X_sub_mean = {}
    for i , p in enumerate(["M", "D", "H"]) :
        X_sub_mean[p] = X_seek_mean.xs(key = p, level = "Next")
        Y_sub = Y.xs(key = p, level = "Next")
        anomal_sub = {key : value.xs(key = p, level = "Next") for key, value in anomal.items()}
        
        title = "< " + RPT_MODE + " (" + p + ") " + "MEAN" + " >"
        Report.append(get_result(k = i+3, X = X_sub_mean[p], Y = Y_sub, y_name = y_name, anomal = anomal_sub, title = title))
    
    
    
    ### STD for Subdata ###
    
    X_sub_std = {}
    for i , p in enumerate(["M", "D", "H"]) :
        X_sub_std[p] = X_seek_std.xs(key = p, level = "Next")
        Y_sub = Y.xs(key = p, level = "Next")
        anomal_sub = {key : value.xs(key = p, level = "Next") for key, value in anomal.items()}
        
        title = "< " + RPT_MODE + " (" + p + ") " + "STD" + " >"
        Report.append(get_result(k = i+6, X = X_sub_std[p], Y = Y_sub, y_name = y_name, anomal = anomal_sub, title = title))
        
    
    ### REPORT ###

    
    return Report
    
    
    
    
    
    
    
    
    
    
    
