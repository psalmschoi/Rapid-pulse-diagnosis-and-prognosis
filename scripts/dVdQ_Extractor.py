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


index_name = ["Next", "Path", "Number"]
column_index = ["Stage2"]
index_tuples = []
data_values = []

    
for idx, sub in enumerate(TOTAL) :
    for data in tqdm(sub, desc = f"Extracting ({idx+1}/{len(TOTAL)})") :
        data.get_dVdQ()
        data.get_Retention()
        
        index_tuple = (data.next, data.path, data.num)
        index_tuples.append(index_tuple)
        
        
        data_value = [value for key, value in data.dVdQ.items()] + [data.SOH, data.next_SOH, data.next_Ratio, data.cyc_Ratio]
        data_values.append(data_value)
                
row_index = pd.MultiIndex.from_tuples(tuples = index_tuples, names = index_name)

DATA = pd.DataFrame(data = data_values, index = row_index, columns = column_index + ['SOH', 'Next_SOH', 'Ratio_SOH', 'Ratio_CYC'])

DATA.to_csv(f"data/output/discharge/Discharge_dVdQ_Data.csv")


        