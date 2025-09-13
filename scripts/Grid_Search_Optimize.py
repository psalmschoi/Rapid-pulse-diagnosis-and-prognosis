import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from utils.grid_search import Grid_Search
from tqdm import tqdm


color_dict = {"(M)" : LinearSegmentedColormap.from_list(None, ['skyblue', 'blue'], N = 10)(0.3),
              "(D)" : LinearSegmentedColormap.from_list(None, ['lemonchiffon', 'orange'], N = 10)(0.5),
              "(H)" : LinearSegmentedColormap.from_list(None, ['lightcoral', 'red'], N = 10)(0.3)}

time_lower = [4, 6]
time_upper = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 50, 100, 200, 400, 600, 800, 1000]

for t_low in time_lower:
    for t_up in tqdm(time_upper, desc=f"r value (t_low: {t_low}): "):

        row_index, col_idx, r_value_list, anomal_error_rate_list, report_r_max, report_a_min = Grid_Search("0.1C", t_low, t_up)
        
        col_index = np.array(col_idx).reshape(2,-1)

        fig = plt.figure(1, figsize = (12, 6))
        gs = fig.add_gridspec(1,2)
        ax = [[fig.add_subplot(gs[i,j]) for j in range(2)] for i in range(1)]

        x = range(len(anomal_error_rate_list))


        for n in range(1) :
            for m in range(2) :
                ylim = [100, 0]
                for i in [1,5,6,7] :
                    if n == 0 and m == 0 and i != 1:
                        continue
                    
                    color = "purple"
                    for key, value in color_dict.items() :
                        if key in row_index[i] :
                            color = value
                    
                    y = np.array([anomal_df.loc[row_index[i], col_index[n, m]] for anomal_df in anomal_error_rate_list])
                    
                    ylim_new = [min(0.8, y.min()-0.1), max(1.5, y.max()+0.1)]
                    ylim = [min(ylim[0], ylim_new[0]), max(ylim[1], ylim_new[1])]
                
                    ax[n][m].plot(x, y, label = row_index[i], color = color)

                    ax[n][m].legend(fontsize = 8, loc = "upper left", framealpha = 0.2)
                    ax[n][m].set_xlabel("Start Point")
                    ax[n][m].set_ylabel("Anomaly MSE Rate")
                    ax[n][m].set_title(col_index[n][m])
                    
                ax[n][m].set_ylim(ylim)

        #fig.suptitle("Anomaly Mean Square Error Rate ( " + str(time_lower) + " to " + str(time_upper) + " )", fontsize = 15)
        fig.suptitle("Anomaly Mean Square Error Rate", fontsize = 15)



        fig = plt.figure(2, figsize = (12, 6))
        gs = fig.add_gridspec(1,2)
        ax = [[fig.add_subplot(gs[i,j]) for j in range(2)] for i in range(1)]

        x = range(len(r_value_list))

        save_y_df = {}

        for n in range(1) :
            for m in range(2) :
                ylim = [100, 0]
                for i in [1,5,6,7] :
                    if n == 0 and m == 0 and i != 1:
                        continue
                    
                    color = "purple"
                    for key, value in color_dict.items() :
                        if key in row_index[i] :
                            color = value
                    
                    y = np.array([abs(r_value_df.loc[row_index[i], col_index[n, m]]) for r_value_df in r_value_list])
                    
                    ylim_new = [min(0.5, y.min()-0.1), max(1, min(y.max()+0.1,1))]
                    ylim = [min(ylim[0], ylim_new[0]), max(ylim[1], ylim_new[1])]
                
                    ax[n][m].plot(x, y, label = row_index[i], color = color)

                    ax[n][m].legend(fontsize = 8, loc = "upper left", framealpha = 0.2)
                    ax[n][m].set_xlabel("Start Point")
                    ax[n][m].set_ylabel("| r |")
                    ax[n][m].set_title(col_index[n][m])
                    
                    save_y_df[col_index[n, m] + row_index[i]] = y
                    
                    
                    
                ax[n][m].set_ylim(ylim)

        #fig.suptitle("| r | ( " + str(time_lower) + " to " + str(time_upper) + " )", fontsize = 15)
        fig.suptitle("| r |", fontsize = 15)

        #plt.show()

        Save_DF = pd.DataFrame(save_y_df)
        Save_DF.to_csv(f"data/output/r_value/r_value optimizing t_lower({t_low}) t_upper({t_up}).csv")

