import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from scipy import stats
from utils.report import Report

def get_result(k, X, Y, anomal, y_name, title) :
    
    X_pca = PCA(n_components = 2).fit_transform(X)
    
    x = X_pca[:,0]
    
    report = Report(title = title, y_name = y_name)
    
    for i in range(2) :
        for j in range(2) :
            y = Y[y_name[i][j]].to_numpy()
            
            anomal_index = [X.index.get_loc(idx) for idx in anomal[y_name[i][j]].index if idx in X.index]
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            x_anomal = x[anomal_index]
            y_anomal = y[anomal_index]

            anomal_error = mean_squared_error(y_anomal, x_anomal*slope + intercept)
            total_error = mean_squared_error(y, x*slope + intercept)
            
            anomal_error_ratio = anomal_error / total_error
            
            
            report.add_r(r_value)
            report.add_error(anomal_error_ratio)

    
    return report