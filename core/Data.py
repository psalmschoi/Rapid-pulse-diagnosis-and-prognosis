import numpy as np
import pandas as pd
import os
import core.Process as Process


class Data() :
    def __init__(self, path, ID) :
        if isinstance(ID, str) :
            if len(ID) == 5:
                tail = ID[1:][::-1]
                self.num = 0
                for i in range(len(tail)) :
                    if tail[i] == 'M' :
                        self.num = self.num + 3**i*0
                    elif tail[i] == 'D' :
                        self.num = self.num + 3**i*1
                    else :
                        self.num = self.num + 3**i*2
                self.num = self.num + 1
                self.whole = ID
            else:
                raise ValueError(f"Please input a 5-character ID. Your input: {ID}")
            
        if isinstance(ID, int):
            if ID > 0 and ID <= 81:
                self.num = ID
                n = ID - 1
                self.whole = ''
                for i in range(4) :
                    n, mod = divmod(n, 3)
                    
                    if mod == 0 :
                        self.whole = self.whole + 'M'
                    elif mod == 1 :
                        self.whole = self.whole + 'D'
                    else :
                        self.whole = self.whole + 'H'
                        
                self.whole = (self.whole + 'D')[::-1]
            else:
                raise ValueError(f"Please input an ID between 1 and 81. Your input: {ID}")
        
        if isinstance(path, str) :
            if path == 'F' :
                self.path = path
                self.next = self.whole[0]
            else :
                self.path = path
                self.next = self.whole[len(path)]
        
        if isinstance(path, int) :
            if path == 0 :
                self.path = 'F'
                self.next = self.whole[0]
            else :
                self.path = self.whole[:path]
                self.next = self.whole[path]
                
        
    def get_Peak(self, D = np.arange(10,1201,2)) :
        start_dir = os.getcwd()
        data_dir = os.path.join(start_dir, 'data/input/relaxation data', self.path, "RAW CSV")
        os.chdir(data_dir)
        
        File_set = os.listdir()
        File_set = [file_csv for file_csv in File_set if '.csv' in file_csv]
        File_SOC = [x for x in File_set if 'SOC' in x]
        File_set = [not_SOC for not_SOC in File_set if not_SOC not in File_SOC]
            
        file_size = len(File_set)
            
        soc = Process.SOC_Data(File_SOC, file_size = file_size)
        
        remain = self.whole[len(self.path):][::-1]
        digit = 1
        temp = 0
        for i in remain :
            if i == "D" : temp = temp + 1*digit
            elif i == "H" : temp = temp + 2*digit
            digit = digit*3

        self.SOC = soc[temp]
        
        file_name = self.path + "_" + str(self.num) + ".csv"
        
        self.Result = Process.Pulse_Data(File_name = file_name, SOC = self.SOC, D = D)
        os.chdir(start_dir)
        
        
    def plot_Peak(self) :
        self.get_Peak()
        file_name = self.path + "_" + str(self.num) + ".csv"
        self.Figure = Process.Plot_Data(self.SOC, self.Result, File_set = [file_name])[0]
        
    def get_Retention(self) :
        retention = pd.read_csv("data/input/retention/Retention_RPT.csv", header = 1, index_col = 'CYC')
        self.Retention = retention[self.whole]
        
        cyc_retention = pd.read_csv("data/input/retention/Retention.csv", header = 1, index_col = 0).T
        
        if self.path == 'F' :
            self.now_SOH = 1
            self.next_Ratio = self.Retention.loc[2]/self.Retention.loc[1]
            self.next_SOH = self.next_Ratio
            self.SOH = self.Retention.loc[1]/self.Retention.loc[1]
            self.cyc_Ratio = cyc_retention.loc[self.whole,100]/cyc_retention.loc[self.whole,1]
            self.cyc_now = cyc_retention.loc[self.whole,1]
            self.cyc_next = cyc_retention.loc[self.whole,100]
        else :
            self.next_Ratio = self.Retention.loc[len(self.path)+2]/self.Retention.loc[len(self.path)+1]
            self.next_SOH = self.Retention.loc[len(self.path)+2]/self.Retention.loc[1]
            self.SOH = self.Retention.loc[len(self.path)+1]/self.Retention.loc[1]
            self.cyc_Ratio = cyc_retention.loc[self.whole,100*(len(self.path)+1)]/cyc_retention.loc[self.whole,100*len(self.path)+1]
            self.cyc_now = cyc_retention.loc[self.whole,100*len(self.path)+1]
            self.cyc_next = cyc_retention.loc[self.whole,100*(len(self.path)+1)]
            
        
        

