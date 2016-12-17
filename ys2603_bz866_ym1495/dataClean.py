'''
Created on Dec 3, 2016

@author: muriel820
'''
import pandas as pd
import numpy as np
import datetime as dt

class dataClean():
    '''
    classdocs
    '''


    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.data_origin = pd.read_csv(fileName, header = 0)
        ''''Convert string index to int type'''
        n = np.arange(self.data_origin.shape[0])    #numpy: np.arnage()
        self.data_origin.index = n  #pandas: dataFrame.index
        
    def formatTimetoString(self, colName):
        '''redo time format data to string type'''
        data_time = self.data_origin[colName]
        data_time_x = []
        data_time_format = []
        for i in range(len(data_time)):
            data_time_x.append(dt.datetime.strptime(data_time[i], '%Y-%m-%dT%H:%M:%S'))
        for i in range(len(data_time)):
            data_time_format.append(data_time_x[i].strftime('%Y/%m/%d/%H/%M/%S'))
        self.data_origin[colName] = data_time_format
        
    def dropUnecessaryCols(self, colName):
        self.data_origin = self.data_origin.drop(colName, axis = 1) #pandas: dataFrame.drop
        return self.data_origin
    
    def convertStringtoInt(self, colName):
        '''Convert String type numbers to Int type numbers'''
        pd.to_numeric(self.data_origin[colName])    #pandas:  pd.to_numeric()
        return self.data_origin
    
    def convertBooleantoInt(self):
        '''Convert Boolean elements to Int'''
        Event_to_int = {True:1, False:0}
        for col_name in self.data_origin.columns:
            if self.data_origin.ix[0, col_name] == True or self.data_origin.ix[0, col_name] == False:
                self.data_origin[col_name] = self.data_origin[col_name].map(Event_to_int)
        return self.data_origin
    
    def writetoFile(self, newfilename):
        self.data_origin.to_csv('newfilename')
        file.close()