import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from core.Data import *


Retention_Data = pd.read_csv("data/input/retention/Retention.csv", header = 1, index_col = 0).T


path = input("Enter path or number of the cell : ")

if path.isdigit() :
    n = int(path) - 1
    whole = ''
    for i in range(4) :
        n, mod = divmod(n, 3)
        
        if mod == 0 :
            whole = whole + 'M'
        elif mod == 1 :
            whole = whole + 'D'
        else :
            whole = whole + 'H'
            
    path = (whole + 'D')[::-1]

fig, ax = plt.subplots()

Retention_Data.loc[path].plot(ax=ax)

plt.show()
    


