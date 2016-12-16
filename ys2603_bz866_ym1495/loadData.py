'''
Created on Dec 3, 2016

@author: muriel820
'''
import pandas as pd
import numpy as np

class loadData:
    
    '''
    classdocs
    '''
    def __init__(self, basicDataFileName, largeCleanedDataFileName):
        '''
        Constructor
        '''
        self.basicData = pd.read_csv(basicDataFileName)
        self.basicData.set_index('Pokemon No.', inplace=True, drop=False)
        self.largeData = pd.read_csv(largeCleanedDataFileName)
        
        '''a series of all Pokemon names, with pokemonID as index'''
        self.nameList = self.basicData['Name']
        
        '''return a numpy ndarray of cities'''
        self.cityList = self.largeData['city'].unique()
        self.cityList = np.sort(self.cityList)
        
        '''return a numpy ndarray of continents'''
        self.continentList = self.largeData['continent'].unique()
    
    def __repr__(self):
        str = 'Welcome to Pokemon World!'
        return str

    
   
    

    
