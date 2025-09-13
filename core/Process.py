import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.interpolate import CubicSpline


def PseudoVoigt(x, A, u, s, a) :
    sg = s/np.sqrt(2*np.log(2))
    
    Gaussian = np.exp(-np.power((x-u),2)/(2*sg**2))*(A/np.sqrt(2*np.pi))
    Lorentzian = (s/(np.power(x-u, 2) + s**2))*(A/np.pi)
    
    return (1-a)*Gaussian + a*Lorentzian

def colorFader(c1, c2, mix=0) :
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex(((1-mix)**1.5)*c1 + mix*c2)



def Pulse_Data(File_name, SOC, time_step = 2, ns = 2, nd = 17, FR = [600, 1800], R = [600, 1800], D = np.linspace(10,1200,596)) :
    Result = np.zeros((ns, len(D), nd))
    
    raw_data = pd.read_csv(File_name, header = None)
    
    col = ["Time"] + [f"T{i}_{j}%" for i in range(ns) for j in SOC[i]]
    
    raw_data.columns = col
    raw_data = raw_data.set_index('Time')
    
    for i in range(ns) :
        off_set = np.array([int(FR[i]/time_step+1) if j == 0 else int(R[i]/time_step+1) for j in range(nd)])
        stand = off_set + 1
        
        for j in range(len(D)) :
            obs = off_set + int(D[j]/time_step)
            
            test_data = raw_data[["T{}_{}%".format(i, k) for k in SOC[i]]]
            
            stand_data = np.array([test_data.iloc[stand[l],l] for l in range(nd)])
            obs_data = np.array([test_data.iloc[obs[l],l] for l in range(nd)])
            
            Result[i, j] = obs_data - stand_data
            
    return Result
    
    

def SOC_Data(File_SOC, 
             file_size = 81, n_set = 2, n_data = 17, 
             Q_pulse = 0.019344, 
             MODE = True, 
             start = 40, end = 80, interval = 2.5):
    
    if not MODE :
        try :
            if int((end - start)/interval)+1 != n_data :
                raise Exception('interval Error')
        except Exception as e :
            print(e)
        
        soc = np.array([[[j for j in np.linspace(start, end, n_data)] for i in range(n_set)] for file_num in range(file_size)]).round(2)
        
        return soc
    
    try :
        File_name = File_SOC[0]
    except :
        print("INPUT SOC FILE or Check SOC MODE!!")
    
    SOC = pd.read_csv(File_name, header = None)
    
    soc = [[[0 for j in range(n_data)] for i in range(n_set)] for file_num in range(file_size)]
    
    for file_num in range(file_size) :
        for i in range(n_set) :
            soc[file_num][i] = SOC[file_num][i*(n_data+1) + 1 : (i+1)*(n_data+1)+1].to_numpy()
            
            for j in range(1,n_data+1) :
                soc[file_num][i][j] = soc[file_num][i][j-1] + soc[file_num][i][j] - Q_pulse
            
            soc[file_num][i] = soc[file_num][i] / soc[file_num][i][n_data] * 100
            soc[file_num][i] = soc[file_num][i][:-1].round(2)
    
    return soc


def Plot_Data(x, y, ns = 2, xlim = [45,80], ylim = [0.010, 0.05], File_set = ["Error"], Set_name = ["0.1C", "0.5C"], Interpolation = [False, False, False, False, False, False]) :
    fs = len(File_set)
    plot_num = y.shape[2]
    
    fig_set = [[0 for j in range(ns)] for i in range(fs)]
    
    file_num = 0
    
    for File_name in File_set :
        
        for show_data in range(ns) :
            
            fig = plt.figure((file_num)*(ns) + show_data+1)
            ax = fig.add_subplot()
            
            if Interpolation[0] :
                pass
            else :
                for i in range(plot_num) :
                    ax.plot(x[file_num][show_data], y[file_num, show_data,i], color = colorFader('red', 'blue', i/plot_num), linewidth = 0.75)
    
             
            ax.set_xlabel('SOC (%)')
            ax.set_ylabel('dV (V)')
            ax.set_title(File_name + ' / {}'.format(Set_name[show_data]))
            ax.set_ylim(ylim)
            ax.set_xlim(xlim)
            
            fig_set[file_num][show_data] = fig
            
            plt.close()
        
        file_num = file_num + 1
        
    return fig_set
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    