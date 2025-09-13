import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.convert import *
from matplotlib.colors import LinearSegmentedColormap


Retention_Data = pd.read_csv("data/input/retention/Retention.csv", header = 1, index_col = 0).T


Next = ["M", "D", "H"]
color_dict = {"M" : ['skyblue', 'blue'], 
              "D" : ['lemonchiffon', 'orange'], 
              "H" : ['lightcoral', 'red'],
              "E" : ['blue', 'purple', 'lightcoral']}

next_dict = {"M" : 0, "D" : 1, "H" : 2}

N = 27


fig = plt.figure(1, figsize = (12,8))
ax = fig.add_subplot()

for depth in range(5) :
    Next_counts = np.zeros(3)
    
    for cell in range(1,82) :
        path = get_path(cell)
        
        Next_counts[next_dict[path[depth]]] += 1
        
        retention = Retention_Data.loc[path, 100*depth+1 : 100*(depth+1)]
        
        cmap = LinearSegmentedColormap.from_list(None, color_dict[path[depth]], N = N)
        ax.plot(retention.index, retention, color = cmap(0.5))
        
ax.set_xlabel("Cycle")
ax.set_ylabel("Capacity (Ah)")

ax.set_xlim([0,500])

plt.show()


fig = plt.figure(2, figsize = (12,8))
ax = fig.add_subplot()

cmap = LinearSegmentedColormap.from_list(None, color_dict["E"], N = 81)

for cell in range(1,82) :
    path = get_path(cell)
    
    retention = Retention_Data.loc[path]
    
    ax.plot(retention.index, retention, color = cmap(cell / 81))
        
ax.set_xlabel("Cycle")
ax.set_ylabel("Capacity (Ah)")

ax.set_xlim([0,500])

plt.show()

fig = plt.figure(3, figsize = (12,8))
ax = fig.add_subplot()

Retention_Data_sorted = Retention_Data.sort_values(by = 500, ascending = True)

cmap = LinearSegmentedColormap.from_list(None, color_dict["E"], N = 81)

for cell in range(81) :
    retention = Retention_Data_sorted.iloc[cell]
    
    ax.plot(retention.index, retention, color = cmap(cell / 81))
    

ax.set_xlabel("Cycle")
ax.set_ylabel("Capacity (Ah)")

ax.set_xlim([0,500])

plt.show()

Retention_Data_sorted.to_csv("data/output/retention/Retention_Data_Sorted.csv")
