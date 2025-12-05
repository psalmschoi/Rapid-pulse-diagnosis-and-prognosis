import pandas as pd
from sklearn.model_selection import train_test_split


def Get_Data(Data) :
    RPT_MODE = "0.1C"
    SOC_Range = [9,10,11,12]

    Time_Range = range(6, 15, 2)
    SOC_Range = [str(i) for i in SOC_Range]
    

    X = Data.loc[RPT_MODE, "0" : "16"]
    Y = Data.loc[RPT_MODE, ["SOH", "Next_SOH", "Ratio_SOH", "Ratio_CYC"]].groupby(level = ["Next", "Path", "Number"]).mean()
    
    y = pd.Series(Y["Next_SOH"] - Y["SOH"], name = "Delta_SOH")
    
    Y = pd.concat([Y, y], axis = 1)

    X_seek = X.loc[X.index.get_level_values("Time").isin(Time_Range), SOC_Range]


    X_std = X_seek.groupby(level = ["Next", "Path", "Number"]).std()
    
    return X_std, Y



def Even_Split(X, y, test_size, rs) :

    X_M = X.xs(key = 'M', level = 'Next', drop_level = False)
    X_D = X.xs(key = 'D', level = 'Next', drop_level = False)
    X_H = X.xs(key = 'H', level = 'Next', drop_level = False)
    
    XX = {"M" : X_M, "D" : X_D, "H" : X_H}
    
    y_M = y.xs(key = 'M', level = 'Next', drop_level = False)
    y_D = y.xs(key = 'D', level = 'Next', drop_level = False)
    y_H = y.xs(key = 'H', level = 'Next', drop_level = False)
    
    yy = {"M" : y_M, "D" : y_D, "H" : y_H}
    
    
    XXX = {"M" : [], "D" : [], "H" : []}
    
    yyy = {"M" : [], "D" : [], "H" : []}
    
    
    for n in ["M", "D", "H"] :
        for path in range(1,5) :
            X_path = XX[n].loc[XX[n].index.get_level_values(level = 'Path').str.len() == path]
            y_path = yy[n].loc[yy[n].index.get_level_values(level = 'Path').str.len() == path]
            
            XXX[n].append(X_path)
            yyy[n].append(y_path)
            
            
    XX_tn = {"M" : [], "D" : [], "H" : []}
    XX_te = {"M" : [], "D" : [], "H" : []}
    
    yy_tn = {"M" : [], "D" : [], "H" : []}
    yy_te = {"M" : [], "D" : [], "H" : []}
        
    for n in ["M", "D", "H"] :
        for path in range(1,5) :
            X_temp = XXX[n][path-1]
            y_temp = yyy[n][path-1]
            
            X_tn, X_te, y_tn, y_te = train_test_split(X_temp, y_temp, test_size = test_size, random_state = rs)
            
            XX_tn[n].append(X_tn)
            XX_te[n].append(X_te)
            yy_tn[n].append(y_tn)
            yy_te[n].append(y_te)
          
    
            
    for n in ["M", "D", "H"] :
        XX_tn[n] = pd.concat(XX_tn[n])
        XX_te[n] = pd.concat(XX_te[n])
        yy_tn[n] = pd.concat(yy_tn[n])
        yy_te[n] = pd.concat(yy_te[n])
        
        
    X_tn = pd.concat(XX_tn.values())
    X_te = pd.concat(XX_te.values())
    
    y_tn = pd.concat(yy_tn.values())
    y_te = pd.concat(yy_te.values())
    
    return X_tn, X_te, y_tn, y_te