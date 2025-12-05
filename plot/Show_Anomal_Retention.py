import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from core.Data import *
from matplotlib.colors import LinearSegmentedColormap


Retention_Data = pd.read_csv("data/input/retention/Retention.csv", header = 1, index_col = 0).T


path = input("Enter History path of the cell : ")

path_len = len(path)

Next = ["M", "D", "H"]
color_dict = {"M" : ['lightblue', 'blue', 'darkblue'], 
              "D" : ['lightgreen', 'green', 'darkgreen'], 
              "H" : ['lightcoral', 'red', 'darkred'],
              "E" : ['plum', 'purple', 'indigo']}
next_dict = {"M" : 0, "D" : 1, "H" : 2}


bunch = [path]

for i in range(5 - path_len) :
    temp_bunch = []
    
    for b in bunch :
        for n in Next :
            temp_bunch.append(b + n)
    
    bunch = temp_bunch


fig, ax = plt.subplots()


for b in bunch :
    index = b[path_len+1:][::-1]
    i = 0
    for j in range(len(index)) :
        i = i + 3**j*next_dict[index[j]]
    
    N = len(bunch)/3
    
    cmap = LinearSegmentedColormap.from_list(None, color_dict[b[path_len]], N = N)
    Retention_Data.loc[b].plot(ax=ax, c = cmap(i/N))

#ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize = 8)
 

fig = plt.figure(figsize = (28,7))
gs = fig.add_gridspec(1,9)
ax = [fig.add_subplot(gs[:,3*i:3*i+2]) for i in range(3)]

N = int(len(bunch)/3)

Ratio_set = [Retention_Data.loc[b, (path_len+1)*100]/Retention_Data.loc[b, path_len*100+1] for b in bunch]
Ratio_std = [np.array(Ratio_set[N*i:N*(i+1)]).std(ddof=1) for i in range(3)]
Ratio_mean = [np.array(Ratio_set[N*i:N*(i+1)]).mean() for i in range(3)]

cmap_anomal = LinearSegmentedColormap.from_list(None, color_dict["E"], N = N)

anomal = {"M" : [],
          "D" : [],
          "H" : []}

for idx, b in enumerate(bunch) :
    index = b[path_len+1:][::-1]
    i = 0
    for j in range(len(index)) :
        i = i + 3**j*next_dict[index[j]]
    
    cmap = LinearSegmentedColormap.from_list(None, color_dict[b[path_len]], N = N)
    
    Z = (Ratio_set[idx] - Ratio_mean[next_dict[b[path_len]]])/Ratio_std[next_dict[b[path_len]]]
    
    
    
    if Z >= -1:
        Retention_Data.loc[b, path_len*100+1 : (path_len+1)*100].plot(ax=ax[next_dict[b[path_len]]], legend = b,  c = cmap(i/N))
    
    else :
        anomal[b[path_len]].append((b, round(Z,3)))
        Retention_Data.loc[b, path_len*100+1 : (path_len+1)*100].plot(ax=ax[next_dict[b[path_len]]], legend = b,  c = cmap_anomal(i/N))
    


for a in ax :
    a.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize = 8)
    
for n in Next :
    print("Next :",n)
    if anomal[n]:
        print("Anomal:")
        for path, sig in anomal[n]:
            print(path, f"-> {sig} (sig)")
    print()

plt.show()