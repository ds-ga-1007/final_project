'''
Provide a function that allows users to input a file path and output a dataframe.
If users input a second parameter as “1” (optional), then this function will also partition the path for GenreType and ArtistName into the dataframe.
During the process:
1)    The function will map the note_id in midi format to octave
2)    The function will map the program_id in midi format to which instrument and its type in each track (as well as handle the special case for track 10, which is reserved for special instruments)

@author: Wenjie Sun
'''


import mido
import pandas as pd
import numpy as np
from mido import MidiFile
midi_program = pd.read_csv("Midi_Program.csv")
midi_pro_10 = pd.read_csv("midi10.csv",encoding = "ISO-8859-1")
# source: https://en.wikipedia.org/wiki/General_MIDI
midi_note = pd.read_csv("midi_note.csv")
# source: http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm

class midi_to_dataframe():

    def __init__(self,midi_path,path_info=0):
        self.midi_path = midi_path
        self.midi = MidiFile(self.midi_path)
        self.channel_list = list()
        self.note_list = list()
        self.vel_list = list()
        self.time_list = list()
        self.program_list = list()
        self.channel_list_program = list()
        self.path_info = path_info
        self.midi_program = midi_program
        self.midi_pro_10 = midi_pro_10
        self.midi_note = midi_note

        # for loop to run for midi channel(track), note, velocity, time, and program.
        # The dataframe will only take when channel is not null and time is not null (if a row without time and channel, it provides little info).

        for i, track in enumerate(self.midi.tracks):
            for message in track:
                try:
                    self.channel_list.append(message.channel)
                    try:
                        self.time_list.append(message.time)
                        # Midi will only have a program id when the program is changed. So, when it is missing, it means NaN
                        # And NaN will be taken care in the later.
                        try:
                            self.program_list.append(message.program)
                        except:
                            self.program_list.append(np.NaN)
                        # when velocity or note is missing in that row, it basically means this track at this time is silent.
                        try:
                            self.vel_list.append(message.velocity)
                        except:
                            self.vel_list.append(0)
                        try:
                            self.note_list.append(message.note)
                        except:
                            self.note_list.append(0)
                    except:
                        pass
                except:
                    pass

        self.consolidate = pd.DataFrame({
            'Channel': self.channel_list,
            'Note': self.note_list,
            'Velocity': self.vel_list,
            'Time': self.time_list,
            'Program': self.program_list
        })
        # if path_info parameter ==1, it parses the info from the path.
        if self.path_info == 1:

            self.consolidate["MidiName"] = (str(self.midi_path.split("/")[-1]).split('.')[0])
            self.consolidate["Artist"] = (str(self.midi_path.split("/")[-2]))
            self.consolidate["Genre"] = (str(self.midi_path.split("/")[-3]))
        else:
            self.consolidate["MidiName"] = (str(self.midi_path.split("/")[-1]).split('.')[0])
            self.consolidate["Artist"] = ""
            self.consolidate["Genre"] = ""
        # Total midi length
        self.consolidate["Length"] = self.midi.length
        # The ticks per beat for the midi
        self.consolidate["Ticks_per_beat"] = self.midi.ticks_per_beat

        # as mentioned eariler, this block to fill NaN with program id
        for i in self.midi.tracks[0]:
            if i.type == "set_tempo":
                self.consolidate["Tempo"] = i.tempo
        self.consolidate["Program"] = self.consolidate["Program"].fillna(method="ffill")
        # merge the dataframe with midi_program (which provides instrument info)
        self.consolidate_instrument = pd.merge(self.consolidate, self.midi_program, left_on="Program", right_on="ProgramID",
                                          how="left")

        self.consolidate_instrument = self.consolidate_instrument.drop("ProgramID", axis=1)

        # * Special note: Midi reserves channel == 10 for a special set of instrument.
        if 10 in self.consolidate_instrument.Channel:
            x = self.consolidate_instrument[self.consolidate_instrument.Channel != 10]

            y = self.consolidate_instrument[self.consolidate_instrument.Channel == 10]

            new_y = pd.merge(y, self.midi_pro_10, left_on="Program", right_on="ProgramID", how="left")
            new_y = new_y.drop(["Type", "Instrument", "ProgramID"], axis=1)
            new_y = new_y.rename(index=str, columns={"Type_10": "Type", "Instrument_10": "Instrument"})
            self.consolidate_instrument = x.append(new_y, ignore_index=True)
        # Drop Channel 0 since it provides some base information of midi only
        if 0 in self.consolidate_instrument.Channel:
            self.consolidate_instrument = self.consolidate_instrument[self.consolidate_instrument.Channel != 0]
        # Create a new column of real-time. midi used a different way to process the time
        self.consolidate_instrument["Real_time"] = (
        self.consolidate_instrument.Tempo / (10 ** 6 * self.consolidate_instrument.Ticks_per_beat) * self.consolidate_instrument.Time)

        # merge midi note file so that we know what is the octave respectively to the note id
        self.combine_w_note = pd.merge(self.consolidate_instrument, self.midi_note, left_on="Note", right_on="Midi_NoteNum",
                                  how="left")
        self.combine_w_note = self.combine_w_note.drop("Midi_NoteNum", axis=1)
        # re-organize the column.
        # This modeul has been updated 6 times becasue the compliexity of midi file. To ensure other functions can work properly,
        # I reorganize all columns sequence in the same way.
        self.combine_w_note = self.combine_w_note[['Channel', 'Note', 'Time', 'Velocity', 'MidiName', 'Artist', 'Genre',
                                         'Length', 'Ticks_per_beat', 'Tempo', 'Program', 'Type', 'Instrument',
                                         'Real_time', 'Octave']]











    def result(self):
        return self.combine_w_note






