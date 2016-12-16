'''
This module is to unittest apidata.py, video.py, and action.py.
'''

import unittest
from apidata import *
from video import *
from action import *
from pandas.util.testing import assert_frame_equal

# Set start date, end date, and API key used in the tests.
start_date = datetime.strptime('2016-02-25', '%Y-%m-%d')
end_date = datetime.strptime('2016-03-12', '%Y-%m-%d')
API_key = 'AIzaSyAMHTQivysLqqSuYWZCzbhsmy_ps2Fjc3I'

class Test_apidata(unittest.TestCase):  
    '''
    The Test_apidata class provides unit tests for the class apidata.
    '''
    def test_apidata(self):
        self.assertEqual(apidata('Google', start_date, end_date, API_key).channel_name, 'Google')
        self.assertEqual(apidata('Google', start_date, end_date, API_key).start_date, datetime.strptime('2016-02-25', '%Y-%m-%d'))
        self.assertEqual(apidata('Google', start_date, end_date, API_key).end_date, datetime.strptime('2016-03-12', '%Y-%m-%d'))
                                       
    def test_channel_id(self):
        self.assertEqual(apidata('Google', start_date, end_date, API_key).channel_id(), 'UCK8sQmJBp8GCxrOtXWBpyEA')
        
    def test_video_ids(self):
        expected = ['EnlsEyN7qmw', 'Hl3aJms0xGQ', 'sWWyT8iQU3M']
        self.assertEqual(apidata('Google', start_date, end_date, API_key).video_ids(), expected)
        
    def test_video_detail(self):
        expected = build('youtube', 'v3', developerKey = API_key).videos().list(  
            part = 'snippet, contentDetails',
            id = 'EnlsEyN7qmw'  
        ).execute().get('items', [])[0]
        self.assertEqual(apidata('Google', start_date, end_date, API_key).video_detail('EnlsEyN7qmw'), expected)
        
class Test_video(unittest.TestCase):
    '''
    The Test_video class provides unit tests for the class video.
    '''
    def test_video(self):
        self.assertEqual(video('Google', start_date, end_date, API_key).channel_name, 'Google')
        
    def test_video_number(self):
        self.assertEqual(video('Google', start_date, end_date, API_key).video_number(), 3)
    
    def test_video_durations(self):
        expected = p.DataFrame({'Google': [63, 48, 1445]})
        assert_frame_equal(video('Google', start_date, end_date, API_key).video_durations(), expected)
        # Reference: http://stackoverflow.com/questions/19928284/pandas-dataframe-values-equality-test
    
    def test_video_published(self):
        expected = p.DataFrame([['Wednesday', 6], ['Tuesday', 0], ['Friday', 17]], columns = ['weekday', 'hour'])
        assert_frame_equal(video('Google', start_date, end_date, API_key).video_published(), expected)
 
class Test_merge(unittest.TestCase):
    '''
    The Test_merge class provides unit tests for the class merge.
    '''  
    def test_merge(self):
        self.assertEqual(merge(['PewDiePie', 'Google'], start_date, end_date, API_key).channel_list, ['PewDiePie', 'Google'])
        self.assertEqual(merge(['PewDiePie', 'Google'], start_date, end_date, API_key).start_date, datetime.strptime('2016-02-25', '%Y-%m-%d'))
        self.assertEqual(merge(['PewDiePie', 'Google'], start_date, end_date, API_key).end_date, datetime.strptime('2016-03-12', '%Y-%m-%d'))
        self.assertEqual(merge(['PewDiePie', 'Google'], start_date, end_date, API_key).API_key, 'AIzaSyAMHTQivysLqqSuYWZCzbhsmy_ps2Fjc3I') 
    
    def test_merge_number(self):
        self.assertEqual(merge(['PewDiePie', 'Google'], start_date, end_date, API_key).merge_number(), {'PewDiePie': 25, 'Google': 3})

class Test_action(unittest.TestCase):
    '''
    The Test_action class provides unit tests for the class action.
    '''  
    def test_duration_stats(self):
        assert_frame_equal(action(['PewDiePie'], start_date, end_date, API_key).duration_stats(), 
            merge(['PewDiePie'], start_date, end_date, API_key).merge_duration().describe().ix[['count','mean','std','min','max']].round(2))
     
    def test_weekday_mode(self):
        expected = p.DataFrame({'PewDiePie': ['Wednesday']})
        assert_frame_equal(action(['PewDiePie'], start_date, end_date, API_key).weekday_mode(), expected)
    
    def test_hour_mode(self): 
        expected = p.DataFrame({'PewDiePie': [16, 18]})
        assert_frame_equal(action(['PewDiePie'], start_date, end_date, API_key).hour_mode(), expected)

        
if __name__ == '__main__':
    unittest.main()
    