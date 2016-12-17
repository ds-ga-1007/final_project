'''
This class merges multiple midi files into one dataframe.

@author: Wenjie Sun
'''


from path_list import *
from midi_to_dataframe import *

class process_master():

    def __init__(self,pathlist,min_channel_number):
        self.pathlist = pathlist
        self.min_channel_number = min_channel_number
        self.master = pd.DataFrame()
        self.allpath = path_list(self.pathlist).result()
        self.song_seq_num = 0
        for self.i in range(len(self.allpath)):
            try:
                # adding song_seq to the master_database
                self.mididf = midi_to_dataframe(self.allpath[self.i],1).result()
                if len(list(set(self.mididf["Channel"]))) > self.min_channel_number:
                    self.mididf["Song_Seq"] = self.song_seq_num
                    self.song_seq_num += 1
                    self.master = self.master.append(self.mididf)
            except:
                continue

    def result(self):
        return self.master