'''
This module displays the summary statistics and plots of video durations and publish times.
'''

from video import *

import matplotlib.pyplot as plt
 
class action():
    '''
    Given a list of channel names, start date, end date and API key, the action class obtains
    the count, mean, standard deviation, minimum and maximum of video durations, the mode of video publish times,
    and shows the histograms of video durations as well as the barplots of video publish times.
    '''
    def __init__(self, channel_list, start_date, end_date, API_key):
        '''
        The constructor defines instance variables merge, duration, weekday, and hour.
        '''
        self.merge = merge(channel_list, start_date, end_date, API_key)
        self.duration = self.merge.merge_duration()
        self.weekday = self.merge.merge_weekday()
        self.hour = self.merge.merge_hour()
        
    def duration_stats(self):
        '''
        The function returns the summary statistics of video durations by each channel in the channel list.
        '''
        return self.duration.describe().ix[['count','mean','std','min','max']].round(2)   # Reference: http://www.marsja.se/pandas-python-descriptive-statistics/

    def duration_hist(self):
        '''
        The function returns the histograms of video durations by each channel in the channel list.
        '''
        self.duration.hist(bins = 10, sharex=False, sharey=True)   # Reference: http://matplotlib.org/1.4.2/api/pyplot_api.html
        plt.show()

    def weekday_mode(self):
        '''
        The function returns the mode of video published weekdays by each channel in the channel list.
        '''
        return self.weekday.mode(axis=0)
    
    def hour_mode(self):
        '''
        The function returns the mode of video published hours by each channel in the channel list.
        '''
        return self.hour.mode(axis=0)

    def published_bar(self): 
        '''
        The function returns the barplots of video published weekdays and hours by each channel in the channel list.
        ''' 
        fig, axes = plt.subplots(1, 2, figsize = (15, 10))
        weekday_count = self.weekday.apply(p.value_counts).ix[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]   # Reference: http://stackoverflow.com/questions/22391433/count-the-frequency-that-a-value-occurs-in-a-dataframe-column
        weekday_count.plot(
            kind = 'bar', 
            ax = axes[0],  
            align = 'center',
            title = 'Distribution of Video Published Weekday'
        )
        hour_count = self.hour.apply(p.value_counts).sort_index()
        hour_count.plot(
            kind = 'bar', 
            ax = axes[1], 
            rot = 0,
            align = 'center',
            title = 'Distribution of Video Published Hour'
        )
        plt.show()
