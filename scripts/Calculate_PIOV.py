import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utils.find_anomal as FA
import utils.plot_report as pplot
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats


### SETTING ###

RPT_MODE = "0.1C"

time_lower = 6
time_upper = 14


SOC_Range = [9, 10, 11, 12]

###############
SOC_Range = [str(i) for i in SOC_Range]
Report = []

color_dict = {"M" : LinearSegmentedColormap.from_list(None, ['skyblue', 'blue'], N = 10)(0.3),
              "D" : LinearSegmentedColormap.from_list(None, ['lemonchiffon', 'orange'], N = 10)(0.5),
              "H" : LinearSegmentedColormap.from_list(None, ['lightcoral', 'red'], N = 10)(0.3)}

X = FA.X
Y = FA.Y_tot

X_seek = X.loc[X.index.get_level_values('Time').isin(range(time_lower, time_upper+1, 2)), SOC_Range]

X_seek_mean = X_seek.groupby(level = ['Path', 'Next', 'Number']).mean()
X_seek_std = X_seek.groupby(level = ['Path', 'Next', 'Number']).std()



### PLOT PART ###

y_name = np.array([["Next_SOH"]])
anomal = {"SOH" : FA.Anomal_NOW, "Next_SOH" : FA.Anomal_NEXT, "Ratio_SOH" : FA.Anomal_SOH, "Ratio_CYC" : FA.Anomal_CYC, "Delta_SOH" : FA.Anomal_DELTA}


### MEAN for Whole Data ###

title = "< " + RPT_MODE + " " + "MEAN" + " >"
Report.append(pplot.Plot_Result(k = 1, X = X_seek_mean, Y = Y, y_name = y_name, anomal = anomal, title = title))




### STD for Whole Data ###

title = "< " + RPT_MODE + " " + "STD" + " >"
Report.append(pplot.Plot_Result(k = 2, X = X_seek_std, Y = Y, y_name = y_name, anomal = anomal, title = title))


### MEAN for Subdata ###

X_sub_mean = {}
for i , p in enumerate(["M", "D", "H"]) :
    X_sub_mean[p] = X_seek_mean.xs(key = p, level = "Next")
    Y_sub = Y.xs(key = p, level = "Next")
    anomal_sub = {key : value.xs(key = p, level = "Next") for key, value in anomal.items()}
    
    title = "< " + RPT_MODE + " (" + p + ") " + "MEAN" + " >"
    Report.append(pplot.Plot_Result(k = i+3, X = X_sub_mean[p], Y = Y_sub, y_name = y_name, anomal = anomal_sub, title = title, colors = [color_dict[p], color_dict[p]]))



### STD for Subdata ###
Save_DF = pd.DataFrame()

X_sub_std = {}
Y_sub = {}
for i , p in enumerate(["M", "D", "H"]) :
    X_sub_std[p] = X_seek_std.xs(key = p, level = "Next")
    Y_sub[p] = Y.xs(key = p, level = "Next")
    anomal_sub = {key : value.xs(key = p, level = "Next") for key, value in anomal.items()}
    
    title = "< " + RPT_MODE + " (" + p + ") " + "STD" + " >"
    Report.append(pplot.Plot_Result(k = i+6, X = X_sub_std[p], Y = Y_sub[p], y_name = y_name, anomal = anomal_sub, title = title, colors = [color_dict[p], color_dict[p]]))


plt.show()

### REPORT ###

for report in Report :
    print(report.output())
    

for p in ["M", "D", "H"] :
    X_pca = PCA(n_components = 2).fit_transform(X_sub_std[p])
    
    X_pca_series = pd.Series(X_pca[:,0], index = X_sub_std[p].index, name = "PCA")
    
    XY_sub_std = pd.concat([X_sub_std[p], X_pca_series, Y_sub[p]], axis = 1)
    XY_sub_std.to_csv("data/output/PIOV/PIOV_STD_" + p +'.csv')
    













