'''
This module processes raw video data for further analysis.
'''
from apidata import *
from math import nan

import numpy as np
import pandas as p
import re
import calendar

class video():
    '''
    Given one channel name, start date, end date and API key, the video class obtains 
    the number, durations and publish times of videos that were published by the channel in the date range.
    '''
    def __init__(self, channel_name, start_date, end_date, API_key):
        '''
        The constructor defines instance variables channel_name, and apidata.
        '''
        self.channel_name = channel_name
        self.apidata = apidata(channel_name, start_date, end_date, API_key)

    def video_number(self):
        '''
        The function returns the number of videos.
        '''
        return len(self.apidata.video_ids())
    
    def video_durations(self):
        '''
        The function returns a dataframe of video durations.
        '''
        video_durations = []
        # Add each video duration to the list, and then display the list of all video durations.
        for video_id in self.apidata.video_ids():
            try:
                video_duration_text = self.apidata.video_detail(video_id)['contentDetails']['duration']
                # Transform the duration string (such as "PT10M59S" for 10 minutes and 59 seconds) into seconds (such as 659)
                video_duration_number = re.findall('\d+', video_duration_text)   # Reference: http://stackoverflow.com/questions/28467446/problems-with-using-re-findall-in-python
                video_duration = sum(int(x) * 60 ** i for i,x in enumerate(reversed(video_duration_number)))   # Reference: http://stackoverflow.com/questions/6402812/how-to-convert-an-hmmss-time-string-to-seconds-in-python
                video_durations.append(video_duration)
            except (KeyError, HttpError):
                video_durations.append(int('NaN'))
        video_durations = p.DataFrame({self.channel_name: video_durations})
        return video_durations
    
    def video_published(self):
        '''
        The function returns a dataframe of video published times, namely day of a week and hour of a day.
        '''
        video_published = []
        # Add each video published time to the list, and then display the list of all video published times.
        for video_id in self.apidata.video_ids():
            try:
                video_published_text = self.apidata.video_detail(video_id)['snippet']['publishedAt']
                # Transform the publishedAt string (such as "2014-01-29T17:53:13.000Z") into weekday and hour (such as "Wednesday" and 15)
                video_published_number = [int(number) for number in re.findall('\d+', video_published_text)]
                video_published_weekday = datetime(video_published_number[0], video_published_number[1], video_published_number[2]).date().weekday()
                video_published_weekday = calendar.day_name[video_published_weekday]   # Reference: https://docs.python.org/3/library/datetime.html
                video_published_hour = video_published_number[3]
                video_published.append([video_published_weekday, video_published_hour])
            except (KeyError, HttpError):
                video_published.append([int('NaN'), int('NaN')])   # Not tested yet
        video_published = p.DataFrame(video_published, columns = ['weekday', 'hour'])
        return video_published

class merge():
    '''
    Given a list of channel names, start date, end date and API key, the merge class obtains the dictionary of video numbers,
    and the dataframes of video durations and publish times by different channels in the date range.
    '''
    def __init__(self, channel_list, start_date, end_date, API_key):
        '''
        The constructor defines instance variables channel_list, start_date, end_date and API_key
        and set the initial values of number, duration, weekday, and hour.
        '''
        self.channel_list = channel_list
        self.start_date = start_date
        self.end_date = end_date
        self.API_key = API_key
        
        self.number = {}
        self.duration = p.DataFrame()
        self.weekday = p.DataFrame()
        self.hour = p.DataFrame()

    def merge_number(self):
        '''
        The function returns a dictionary in which indexes are channel names and values are video numbers.
        '''
        for channel_name in self.channel_list:
            new_video = video(channel_name, self.start_date, self.end_date, self.API_key)
            self.number[channel_name] = new_video.video_number()
        return self.number 
        
    def merge_duration(self):
        '''
        The function returns a dataframe in which columns are channel names and values are video durations.
        '''
        for channel_name in self.channel_list:
            new_video = video(channel_name, self.start_date, self.end_date, self.API_key)
            self.duration = self.duration.join(new_video.video_durations(), how = 'outer')    
        return self.duration
    
    def merge_weekday(self):
        '''
        The function returns a dataframe in which columns are channel names and values are video published weekdays.
        '''
        for channel_name in self.channel_list:
            new_video = video(channel_name, self.start_date, self.end_date, self.API_key)
            new_video_weekday = new_video.video_published()['weekday'].to_frame().rename(columns = {'weekday': channel_name})   # Reference: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.to_frame.html
            self.weekday = self.weekday.join(new_video_weekday, how = 'outer')    
        return self.weekday
            
    def merge_hour(self):
        '''
        The function returns a dataframe in which columns are channel names and values are video published hours.
        '''
        for channel_name in self.channel_list:
            new_video = video(channel_name, self.start_date, self.end_date, self.API_key)
            new_video_hour = new_video.video_published()['hour'].to_frame().rename(columns = {'hour': channel_name})
            self.hour = self.hour.join(new_video_hour, how = 'outer')   
        return self.hour
      
    