'''
This module contain developer defined exceptions.
'''

class ActionError(Exception):
    '''
    Exception raised for errors in the specified action.
    '''
    def __str__(self):
        return 'Invalid action: please choose from number, duration, and published'

class DateError(Exception):
    '''
    Exception raised for errors in the specified date range.
    '''
    def __str__(self):
        return 'The end date should be later than the start date and reasonable'

class ChannelError(Exception):
    '''
    Exception raised for errors in the specified channel.
    '''
    def __str__(self):
        return 'Invalid channel name(s)'
