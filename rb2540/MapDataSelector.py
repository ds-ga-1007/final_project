import pandas as pd

class MapDataSelector(object) :
    '''For a given year and list of event types, gives access to longitude and latitude data for events'''
    def __init__(self,file) :
        '''Loads the events, and excludes storms beginning off map, or in untracked states'''
        excludedStates = ['VIRGIN ISLANDS','PUERTO RICO','GUAM','ALASKA','HAWAII']
        lowerLimit = -400
        upperLimit = -60
        file = r'./FilteredData/filteredData.csv'
        df = pd.read_csv(file)
        df = df[(df['BEGIN_LON']>-400) & (df['BEGIN_LON']<-60) & (df['STATE'].isin(excludedStates)==False)]
        self.frame = df
    
    def getYearData(self,year,eventList) :
        '''Returns a tuple of a longitude dataframe and a latitude dataframe for the given year and event list'''
        df = self.frame
        year = df[(df['BEGIN_YEAR']==year) & (df['EVENT_TYPE'].isin(eventList))]
        return (year['BEGIN_LON'],year['BEGIN_LAT'])
        
