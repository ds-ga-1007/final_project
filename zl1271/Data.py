'''
Created on Dec 10, 2016

@author: felix
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

class Data:
    '''
    Creates a class based on data file location
    Only include the data that will be used later 
    
    '''

    def set_value (self, variable, origial_values, set_as = None):
        # set the entered values as missing, or change into different values
        # variable should be a str that is a header
        # missing_values should be a list of values, determined by the documentation of the data source
        # set_as by default is None, i.e., set it to missing data
        for value in origial_values:
            li = list(self.data.loc[:,variable] == value)
            self.data.loc[li,variable] = set_as
    
    def recode_values(self):
        # record missing values and recode values for regression
        # conrinc is income, 0 is IAP: inapplicable; 999999 is NA: not asked; 999998 is DK: don't know
        self.set_value('conrinc',[0,999999,999998])
        # age: 89 or older is 89, no missing
        # sex: no missing, but need to change to 0 1 coding, i.e., 2 is female, change to 0
        self.set_value('sex',[2],set_as = 0)
        # race: 0 is IAP
        self.set_value('race',[0])
        # educ: 97 is IAP; 99 is NA; 98 is DK
        self.set_value('educ',[97,98,99])
    
    def split_income(self):
        # The conrinc variable does not appear to have a linear relation with the predictors
        # because the variable is calculated based on ordinal data, and the interval was different
        # after 100000
        self.data.loc[:,'high_inc'] = pd.Series(np.zeros(len(self.data)), index=self.data.index)
        li = list(self.data.loc[:,'conrinc'] >= 100000)
        self.data.loc[li,'high_inc'] = 1
    
    def set_categorical(self):
        self.set_value('sex',[0],set_as = 'female')
        self.set_value('sex',[1],set_as = 'male')
        self.set_value('race', [1], 'white')
        self.set_value('race', [2], 'black')
        self.set_value('race', [3], 'other')

    def __init__(self, file_location = './Data/GSS2014.csv'):
        self.data = pd.read_csv(file_location)[['conrinc','educ','age','sex','race']]
        self.recode_values()
        self.split_income()
        self.set_categorical()
        self.data_clean = self.data.dropna()
        
    def rename_columns(self):
        self.data.rename(columns={'conrinc': 'income'}, inplace=True)
        




