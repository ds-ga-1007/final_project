'''
Created on Nov 15, 2016
@author: Fanglin Chen
YouTube is a video-sharing platform where members can create channels and upload videos for sharing. 
The program displays both text output and matplotlib popup of video statistics after a user enters a channel name and a date range. 
The video statistics include the number of videos, the mean, standard deviation, minimum and maximum of video durations, 
and the mode of video publish times (i.e. hour of the day and day of the week). 
The program also enables comparing the information across multiple channels. 
Please refer to the user guide for a detailed description.
'''

from video import *
from action import *
from Exception import *

# Prompt user to enter one or multiple channel name(s), start date, end date and API key.
while True:
    try:  
        channel_list = input('Please enter one YouTube channel name, or multiple YouTube channel names separated by commas: \n> ')
        if channel_list == 'quit': 
            break
        channel_list = channel_list.split(',')

        start_date = input('Please enter a start date in the form of YYYY-MM-DD: \n> ')
        if start_date == 'quit': 
            break
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = input('Please enter an end date in the form of YYYY-MM-DD: \n> ')
        if end_date == 'quit':
            break
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        if start_date >= end_date or end_date >= datetime.today() or end_date <= datetime.strptime('1970-01-01', '%Y-%m-%d'):
            raise DateError
        
        API_key = input('Please enter your key for YouTube Data API: \n> ')
        if API_key == 'quit':
            break
        break
    except DateError:
        print('The end date should be later than the start date and reasonable')
    except ValueError:
        print('Invalid date')
    except KeyboardInterrupt:
        print('You have hit the interrupt key')

def output():
    '''
    The function displays the output produced by the program.
    '''
    while True:
        try:
            # Prompt user to enter a desired action.
            variable = input('Please choose one of the following actions: number, duration, or published \n> ')
            if variable == 'quit': 
                break
            # If the user chooses "number", display the number of videos.
            elif variable == 'number':
                result = merge(channel_list, start_date, end_date, API_key)
                print(result.merge_number())
            # If the user chooses "duration", display the summary statistics and plot the histograms of video durations.
            elif variable == 'duration':
                result = action(channel_list, start_date, end_date, API_key)  
                print(result.duration_stats())
                result.duration_hist()
            # If the user chooses "published", display the summary statistics and plot the barplots of video published times.
            elif variable == 'published':
                result = action(channel_list, start_date, end_date, API_key)  
                print(p.concat([result.weekday_mode(), result.hour_mode()], ignore_index = True))
                result.published_bar()
            else:
                raise ActionError # Need to specify  
            break  
        # In the case of ActionError or KeyboardInterrupt, prompt user to enter a desired action again.
        except ActionError:
            print('Invalid action: please choose from number, duration, and published') 
        except KeyboardInterrupt:
            print('You have hit the interrupt key')
        # In the case of ChannelError or HttpError, end the program.
        except ChannelError:
            print('Invalid channel name(s)')
            break
        

if __name__ == '__main__':
    output()