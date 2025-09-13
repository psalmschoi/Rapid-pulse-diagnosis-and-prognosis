import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import core.Data as Cell
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from scipy import stats



###################################

RPT_MODE = "0.1C"

###################################


Data = pd.read_csv("data/output/pulse/SOC_Point_Data.csv", index_col = (0,1,2,3,4))
X = Data.reorder_levels(order = (0,2,1,3,4)).sort_index().loc[(RPT_MODE), "0":"16"]
Y = Data.reorder_levels(order = (0,4,2,1,3)).sort_index().loc[(RPT_MODE, 4), ("Ratio_SOH", "Ratio_CYC")]
Y_tot = Data.reorder_levels(order = (0,4,2,1,3)).sort_index().loc[(RPT_MODE, 4), ("SOH","Next_SOH","Ratio_SOH", "Ratio_CYC")]

SOH_Delta = Y_tot["Next_SOH"] - Y_tot["SOH"]
SOH_Delta.name = "Delta_SOH"

Y_tot = pd.concat([Y_tot, SOH_Delta], axis = 1)

PN_group = Y_tot.groupby(level = ['Path','Next'])

PN_mean = PN_group.mean()
PN_std = PN_group.std()

Z = (Y_tot - PN_mean)/PN_std


Y_tot = pd.concat([Y_tot, Z.rename(columns = {"SOH" : 'Anomal_NOW', 'Next_SOH' : 'Anomal_NEXT', 'Ratio_SOH' : 'Anomal_SOH', 'Ratio_CYC' : 'Anomal_CYC', 'Delta_SOH' : 'Anomal_Delta'})], axis = 1)

Y_Cell_ordered = Y_tot.reorder_levels(order = (2,0,1)).sort_index()


### Correlation ###

Cell_Anomal = {"Anomal_NOW" : np.zeros((81, 3)),
               "Anomal_NEXT" : np.zeros((81,3)),
               "Anomal_SOH" : np.zeros((81,3)),
               "Anomal_CYC" : np.zeros((81,3)),
               "Anomal_Delta" : np.zeros((81,3))}


### Indexing ###

Anomal_NOW = Z[Z["SOH"] < -1]
Anomal_NEXT = Z[Z["Next_SOH"] < -1]
Anomal_SOH = Z[Z["Ratio_SOH"] < -1]
Anomal_CYC = Z[Z["Ratio_CYC"] < -1]
Anomal_DELTA = Z[Z["Delta_SOH"] < -1]

Anomal_Cell_SOH = Anomal_SOH.index.get_level_values('Number').value_counts()
Anomal_Cell_CYC = Anomal_CYC.index.get_level_values('Number').value_counts()


Anomal_Cell = pd.concat([Anomal_Cell_SOH, Anomal_Cell_CYC], axis = 1)
Anomal_Cell.columns = ['SOH', 'CYC']


Semi_anomal_SOH = Z[(Z["Ratio_SOH"] > -1) & (Z["Ratio_SOH"] < -0.5)]
Semi_anomal_Cell_SOH = Semi_anomal_SOH.index.get_level_values('Number').value_counts()



if __name__ == "__main__":
    Corr_Cell = {}
    for key, value in Cell_Anomal.items() :
        for i in range(1,82) :
            value[i-1,:] = Y_Cell_ordered.loc[i, key].head(3)

        Cell_First = np.zeros((81,1))
        for i in range(1,82,1) :
            cell_data = Cell.Data("F", i)
            cell_data.get_Retention()
            
            if key == "Anomal_NEXT" :
                Cell_First[i-1] = cell_data.next_SOH
            elif key == "Anomal_SOH" :
                Cell_First[i-1] = cell_data.next_Ratio
            elif key == "Anomal_CYC" :
                Cell_First[i-1] = cell_data.cyc_Ratio
            elif key == "Anomal_Delta" :
                Cell_First[i-1] = cell_data.next_SOH - cell_data.SOH
        
        if key != "Anomal_NOW" :
            Cell_First = (Cell_First - Cell_First.mean())/Cell_First.std()
            value = np.concatenate([Cell_First, value], axis = 1)
        Corr_Cell[key] = np.corrcoef(value, rowvar = False)

    print(Y_tot)
    print(Corr_Cell)
    print(Anomal_Cell)


