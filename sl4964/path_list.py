'''
As long as the midi files are stored in a structure like "user_path/Jazz/Louis Amstrong/xyz.mid".
User needs to input user_path piece and the code will piece down the lables.
The function will produce a list of all the midi files in the user_path folder.


@author: Wenjie Sun
'''


import os

class path_list():
    """

    """
    def __init__(self,path):
        """
        The code can also handle if there is any non-midi file also werid mac format
        """
        self.path = path
        self.genre_file = os.listdir(self.path)
        self.genre_list = []
        self.artist_list = []
        self.song_list = []
        self.path_list = []

        for self.genre in self.genre_file:
            self.genre_list.append(self.genre)
            try:
                self.artist_file = os.listdir(self.path + '/' + self.genre)
            except:
                continue
            for self.artist in self.artist_file:
                self.artist_list.append(self.artist)
                try:
                    self.song_file = os.listdir(self.path + '/' + self.genre + '/' + self.artist)
                except:
                    continue
                for self.song in [self.i for self.i in self.song_file if self.i.endswith('.mid')]:
                    self.song_list.append(self.song)
                    self.path_list.append(self.path + '/' + self.genre + '/' + self.artist + '/' + self.song)


    def result(self):
        return (list(set(self.path_list)))