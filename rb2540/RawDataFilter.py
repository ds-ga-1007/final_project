import pandas as pd
class RawDataFilter(object) :
    ''' Class used to load raw weather data, and then clean and prune it
    for efficient loading and access'''
    def __init__(self) :
        '''Initializes required fields and events'''
        self.relevantFields = ['BEGIN_YEARMONTH','BEGIN_DAY','STATE','BEGIN_LAT','BEGIN_LON','EVENT_TYPE','MAGNITUDE','INJURIES_DIRECT','INJURIES_INDIRECT','DEATHS_DIRECT','DEATHS_INDIRECT']
        self.relevantEvents = ['Hail','Thunderstorm Wind','Tornado']
    
    def loadData(self, files) :
        '''Loads data from given list of files, concatenates it, and then
        extras required events and fields.  Also cleans NaNs and adds
        BEGIN_YEAR and BEGIN_MONTH fields'''
        frame = pd.DataFrame()
        frameList = []
        for f in files :
            df = pd.read_csv(f,index_col=None, header=0)
            frameList.append(df)
        frame = pd.concat(frameList)
        frame = frame[self.relevantFields]
        frame = frame[frame['EVENT_TYPE'].isin(self.relevantEvents)]
        frame.dropna()
        frame['BEGIN_YEAR'] = frame['BEGIN_YEARMONTH']//100
        frame['BEGIN_MONTH'] = frame['BEGIN_YEARMONTH']%100
        del frame['BEGIN_YEARMONTH']
        self.dataFrame = frame
        
    def writeFilteredData(self, file) :
        '''Writes cleaned and filtered data to a given csv file'''
        self.dataFrame.to_csv(file)
