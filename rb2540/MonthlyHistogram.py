import pandas as pd
from collections import Counter

class MonthlyHistogram(object) :
    '''Counts the number of events in a given month given a fixed year and a list of event types'''
    def __init__(self,file) :
        '''Loads filtered data from the given file'''
        self.frame = pd.read_csv(file)
        
    def getYearCounts(self,year,eventList) :
        '''Produces a list of counts for the given year and list of event types'''
        df = self.frame
        yeardf = df[(df['BEGIN_YEAR']==year) & (df['EVENT_TYPE'].isin(eventList))]      
        counts = Counter(yeardf['BEGIN_MONTH'])
        return [counts[i] for i in range(1,13)]

    
