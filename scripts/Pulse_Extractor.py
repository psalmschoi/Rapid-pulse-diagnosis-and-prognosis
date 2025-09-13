import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from core.Data import *


M = []
D = []
H = []

TOTAL = [M, D, H]

for i in range(1,5) :
    for j in range(1, 82) :
        temp = Data(i,j)
        if temp.next == 'M' :
            M.append(temp)
        elif temp.next == 'D' :
            D.append(temp)
        else :
            H.append(temp)

#time_ini = int(input("Enter initial time (sec) to extract: "))
#time_fin = int(input("Enter final time (sec) to extract: "))

time_ini = 4
time_fin = 1200

Diff = np.arange(time_ini, time_fin+1, 2)
    
    
        
seek_point = list(np.arange(0,17,1))

index_name = ["C-rate", "Next", "Path", "Number", "Time"]
column_index = seek_point
index_tuples = []
data_values = []

for c_rate_index in range(2) :
    c_rate = "0.5C" if c_rate_index else "0.1C"
    
    for idx, sub in enumerate(TOTAL) :
        for data in tqdm(sub, desc = f"Extracting {c_rate} ({idx+1}/{len(TOTAL)})") :
            data.get_Peak(D = Diff)
            data.get_Retention()
            
            for time_index, time in enumerate(Diff) :
                index_tuple = (c_rate, data.next, data.path, data.num, time)
                index_tuples.append(index_tuple)
                
                data_value = [data.Result[c_rate_index][time_index][soc_index] for soc_index in seek_point] + [data.SOH, data.next_SOH, data.next_Ratio, data.cyc_Ratio]
                data_values.append(data_value)
                
row_index = pd.MultiIndex.from_tuples(tuples = index_tuples, names = index_name)

DATA = pd.DataFrame(data = data_values, index = row_index, columns = column_index + ['SOH', 'Next_SOH', 'Ratio_SOH', 'Ratio_CYC'])

if time_ini != 4 or time_fin != 1200:
    DATA.to_csv(f"data/output/pulse/SOC_Point_Data({time_ini}-{time_fin}).csv")
else:
    DATA.to_csv(f"data/output/pulse/SOC_Point_Data.csv")

