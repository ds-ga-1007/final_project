'''
This module obtains data from YouTube Data API.
'''

from apiclient.discovery import build
from apiclient.errors import HttpError
from Exception import ChannelError
from datetime import datetime

class apidata():
    '''
    Given one channel name, start date, end date and API key, the apidata class obtains 
    the videos that were published by the channel in the date range and their details.
    '''
    def __init__(self, channel_name, start_date, end_date, API_key):
        '''
        The constructor defines instance variables channel_name, start_date, end_date and youtube.
        '''
        self.channel_name = channel_name
        self.start_date = start_date
        self.end_date = end_date
        # The build() function returns an instance of an API service object that can be used to make API calls. 
        self.youtube = build('youtube', 'v3', developerKey = API_key) 
        
    def channel_id(self):
        '''
        The function transforms the channel name into the channel id.
        '''
        try:
            response = self.youtube.channels().list(
                part = 'id',
                forUsername = self.channel_name
            ).execute()   # Reference: https://developers.google.com/youtube/v3/docs/channels/list
            channel_id_list = response.get('items', [])
            channel_id = channel_id_list[0]['id']
            return channel_id
        # If there is no channel id corresponding to the channel name, raise ChannelError.
        except IndexError:
            raise(ChannelError)


    def search_response(self, token):
        '''
        The function searches for all videos published by the channel in the data range.
        '''
        search_response = self.youtube.search().list(
            part = 'id',
            channelId = self.channel_id(), 
            type = 'video',
            publishedAfter = self.start_date.date().strftime('%Y-%m-%d') + 'T00:00:00Z',
            publishedBefore = self.end_date.date().strftime('%Y-%m-%d') + 'T00:00:00Z',
            maxResults = 50,
            pageToken = token
        ).execute()   # Reference: https://developers.google.com/youtube/v3/docs/videos/list
        return search_response
    

    def video_ids(self):
        '''
        The function returns a list of all video ids.
        '''
        video_ids = []
        token = ''
        while True:    
            try:         
                for search_result in self.search_response(token).get('items', []):
                    video_ids.append(search_result['id']['videoId'])
                # Specify the pageToken for next API call.
                token = str(self.search_response(token).get('nextPageToken'))
            # Stop search if there is no nextPageToken, namely all pages have been retrieved.
            except HttpError:
                break       
        return video_ids
    
        # Call the videos.list method to retrieve location details for each video.
    def video_detail(self, video_id):
        '''
        The function returns details of one video, including its duration and published time.
        '''
        try:
            video_response = self.youtube.videos().list( 
                part = 'snippet, contentDetails',
                id = video_id  # for each of the video_ids
            ).execute()   # Reference: https://developers.google.com/youtube/v3/docs/videos/list
            video_detail = video_response.get('items', [])
            return video_detail[0]
        except HttpError:
            return {}

