import pandas as pd
disease_list=pd.read_csv('disease_list.csv')
disease_list=[i for i in disease_list.iloc[:,1]]
from exception_class import *
import get_heatmap_matrix as mt
from plot_map import *

class color_class:
    def __init__(self, input_color):
        try:
            self.color=float(input_color)
            if (self.color >1 or self.color<0):
                raise colorrangeException()
        except ValueError:
            raise colortypeException()
            
class year_class:
    def __init__(self, input_year,disease):
        self.disease=disease
        try:
            self.year=int(input_year)
            if detect_year(self.year,self.disease)==False:
                raise yearrangeException()
        except ValueError:
            raise yeartypeException()

class disease_class:
    #here import the list of disease and name it as disease_list
    def __init__(self, disease): 
        self.name=disease
        if self.name not in disease_list:
            raise diseaseExceptioin()
        else:
            self.data= mt.heatmap_disease_matrix(disease)
            self.lower=self.data.index.min()
            self.upper=self.data.index.max()
            
    
    def __repr__(self):
        return 'The year range for this disease is from {} to {}'.format(self.lower,self.upper)
