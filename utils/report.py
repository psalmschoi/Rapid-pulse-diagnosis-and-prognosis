import numpy as np

class Report() :
    def __init__(self, title, y_name) :
        self.title = title
        self.y_name = np.array(y_name).reshape(-1)
        self.name = title.ljust(20) + " " + str(self.y_name)
        self.r_values = []
        self.anomal_error_ratio = []
        
    def add_r(self, r_value) :
        self.r_values.append(round(r_value,3))
        
    def add_error(self, error_rate) :
        self.anomal_error_ratio.append(error_rate)
        
    def output(self) :
        return self.name + " : " + str(self.r_values)