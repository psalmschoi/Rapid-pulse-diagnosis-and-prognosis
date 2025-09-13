import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy import stats
from utils.report import Report
        

def Plot_Result(k, X, Y, anomal, y_name, title, colors = ["lightblue", "red"]) :
    
    n, m = y_name.shape
    

    fig = plt.figure(k, figsize = (10, 10))
    gs = fig.add_gridspec(n,m)
    ax = [[fig.add_subplot(gs[i,j]) for j in range(m)] for i in range(n)]
    
    X_pca = PCA(n_components = 2).fit_transform(X)
    
    x = X_pca[:,0]
    
    report = Report(title = title, y_name = y_name)
    
    
    for i in range(n) :
        for j in range(m) :
            y = Y[y_name[i][j]].to_numpy()
            
            anomal_index = [X.index.get_loc(idx) for idx in anomal[y_name[i][j]].index if idx in X.index]
            
            ax[i][j].scatter([val for idx, val in enumerate(x) if idx not in anomal_index], [val for idx, val in enumerate(y) if idx not in anomal_index], color = colors[0], label = 'Normality')
            ax[i][j].scatter([val for idx, val in enumerate(x) if idx in anomal_index], [val for idx, val in enumerate(y) if idx in anomal_index], color = colors[1], label = 'Anomaly')
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            ax[i][j].plot(x, slope*x+intercept, c = 'black', linewidth = 0.8)
            
            ax[i][j].set_xlabel("PCA 1st axis", fontsize = 12)
            ax[i][j].set_ylabel(y_name[i][j], fontsize = 12)
            
            ax[i][j].set_title(y_name[i][j] + " [r = " + str(round(r_value, 3)) + "]", fontsize = 15)
            #ax[i][j].legend()
            
            report.add_r(r_value)
        
    fig.suptitle(title, fontsize = 20)
    
    return report