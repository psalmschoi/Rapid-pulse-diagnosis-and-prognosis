import os
import numpy as np
import pandas as pd
import core.Process as F
import matplotlib.pyplot as plt
from core.Data import *
from utils.convert import *
from tqdm import tqdm

start_path = os.getcwd()

soc = [np.linspace(40,80,17) for i in range(2)]

Diff = np.arange(4,1201,2)
select = np.array(range(len(Diff)))
    
        
seek_point = list(np.arange(0,17,1))

index_name = ["C-rate", "Path", "Number", "Time"]
column_index = seek_point
index_tuples = []
data_values = []


for cell in tqdm(range(1,82), desc="Extracting Cell") :
    path = os.path.join("data/input/relaxation data", get_path(cell), "RAW CSV")
    os.chdir(path)
    
    file, = os.listdir()
    
    Result = F.Pulse_Data(file, soc, D = Diff)
    
    os.chdir(start_path)
    
    prev_data = Data(get_path(cell)[:-1], cell)
    prev_data.get_Retention()
    
    for c_rate_index in range(2) :
        c_rate = "0.5C" if c_rate_index else "0.1C"
            
        for time_index in range(len(select)) :
            index_tuple = (c_rate, get_path(cell), cell, Diff[select[time_index]])
            index_tuples.append(index_tuple)
            
            data_value = [Result[c_rate_index][time_index][soc_index] for soc_index in seek_point] + [prev_data.cyc_next]
            data_values.append(data_value)
    
    
    
row_index = pd.MultiIndex.from_tuples(tuples = index_tuples, names = index_name)    
    
DATA = pd.DataFrame(data = data_values, index = row_index, columns = column_index + ['SOH'])

DATA.to_csv("data/output/pulse/Final_Point_Data.csv")





    
    