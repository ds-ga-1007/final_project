import pandas as pd
import numpy as np

class YearlyEventAggregator(object) :
    '''Aggregates "Injuries", "Deaths", and "Number of Events" by year'''
    def __init__(self,file) :
        '''Loads filtered data and sets up year grouping'''
        df = pd.read_csv(file)
        df = df.groupby(df['BEGIN_YEAR'])
        self.frame = df
        self.mapping = {'Injuries':['INJURIES_DIRECT','INJURIES_INDIRECT'],'Deaths':['DEATHS_DIRECT','DEATHS_INDIRECT'],'Number of Events':['Special']}
        
    def getKeys(self) :
        '''The keys used to access the various aggregate data'''
        return list(self.mapping.keys())
        
    def getAggregate(self,key) :
        '''Produces an dataframe of aggregated data'''
        if key == 'Number of Events' :
            counts = self.frame['EVENT_TYPE'].count()
        else :
            cols = self.mapping[key]
            counts = self.frame[cols[0]].sum() + self.frame[cols[1]].sum()
        return counts
