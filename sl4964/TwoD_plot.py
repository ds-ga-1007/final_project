'''
This moduel run analyses for any given single midi file and return 6 charts..

@author: Wenjie Sun
'''



import matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict
import warnings
warnings.filterwarnings("ignore")

class plot():

    def __init__(self,clean_df):

        self.clean_df = clean_df
        self.midi_name = list((set(self.clean_df["MidiName"])))[0]
        self.global_channel_list = list()

    def plot1(self):

        # plotting music note/octave range by channel chart
        fig = plt.figure(figsize=(10, 8))
        self.max_list = list()
        self.min_list = list()
        self.instrutment_list = list()
        self.high_note_list = list()
        self.low_note_list = list()
        self.channel_list = list()

        for i in list(set(self.clean_df.Channel)):
            self.dloop = self.clean_df[self.clean_df.Channel == i]
            self.dloop_zero = self.dloop[self.dloop.Note != 0]  # drop out 0 from the data frame
            self.channel_list.append(i)
            self.instrutment_list.append(list(set(self.dloop.Instrument.dropna())))  # dropna from the instrument and append a list
            self.max_list.append(self.dloop.Note.max())
            self.min_list.append(self.dloop_zero.Note.min())
            self.high_note_list.append(self.clean_df.loc[self.dloop.Note.idxmax()].Octave)
            self.low_note_list.append(self.clean_df.loc[self.dloop_zero.Note.idxmin()].Octave)

        plt.plot(self.channel_list, self.max_list, label = "Highest Note Per Channel")
        plt.plot(self.channel_list, self.min_list, label = "Lowest Note Per Channel")
        plt.title("Music Note / Octave Range by Channel")
        plt.xlabel("Channel")
        plt.ylabel("""Note (Octave)""")
        plt.legend(loc="lower right")

        plt.xticks(range(len(self.channel_list) + 1))
        plt.ylim(ymin=0)

        for a, b, c in zip(self.channel_list, self.max_list, self.high_note_list):
            plt.text(a, b + 1, str(c))

        for a, b, c in zip(self.channel_list, self.min_list, self.low_note_list):
            plt.text(a, b - 1, str(c))


        plt.savefig(self.midi_name+" Music Note (Octave Range) by Channel.png")
        plt.show()

    def plot2(self):
        # plotting music velocity range by channel
        fig = plt.figure(figsize=(10, 8))
        self.max_list = list()
        self.min_list = list()
        self.high_note_list = list()
        self.low_note_list = list()
        self.channel_list = list()

        for i in list(set(self.clean_df.Channel)):
            self.dloop = self.clean_df[self.clean_df.Channel == i]
            self.dloop_zero = self.dloop[self.dloop.Velocity != 0]  # drop out 0 from the data frame
            self.channel_list.append(i)

            self.max_list.append(self.dloop.Velocity.max())
            self.min_list.append(self.dloop_zero.Velocity.min())

        plt.plot(self.channel_list, self.max_list, label = "Highest Volume")
        plt.plot(self.channel_list, self.min_list, label = "Lowest Volume")
        plt.title("Volume Range by Channel")
        plt.legend(loc="lower right")
        plt.xlabel("Channel")
        plt.ylabel("Volume")

        plt.xticks(range(len(self.channel_list) + 1))
        plt.ylim(ymin=0)
        plt.savefig(self.midi_name + "Music Volume Range by Channel.png")
        plt.show()

    def plot3(self):
        # plotting time persence by channel


        fig = plt.figure(figsize=(10, 8))

        self.time_dict = dict()
        for i in list(set(self.clean_df.Channel)):
            self.dloop = self.clean_df[self.clean_df.Channel == i]
            self.dloop_zero = self.dloop[self.dloop.Velocity != 0]
            self.time_dict[i] = self.dloop_zero["Real_time"].sum()
        self.time_dict_sorted = sorted(self.time_dict.items(), key=lambda x: x[1], reverse=True)

        self.midi_length = max(list(set(self.clean_df["Length"])))  # supposed to only have 1 length each song. using max to avoid any problem
        self.time_list_sorted = list()
        self.channel_list_sorted = list()
        self.pct_list = list()

        for i in range(len(self.time_dict_sorted)):
            self.channel_list_sorted.append(self.time_dict_sorted[i][0])
            self.time_list_sorted.append(self.time_dict_sorted[i][1])
            self.pct_list.append(self.time_dict_sorted[i][1] / self.midi_length)

        plt.bar(range(len(self.time_list_sorted)), self.time_list_sorted, align="center")

        plt.xticks(range(len(self.time_list_sorted)), self.channel_list_sorted)

        plt.title("Total Time by Channel")
        plt.xlabel("Channel")
        plt.ylabel("Total Time   (Percentage of Total)")


        plt.ylim(ymin=min(self.time_list_sorted) - 20)

        for a, b, c in zip(range(len(self.time_list_sorted)), self.time_list_sorted, self.pct_list):
            plt.text(a - 0.4, b + 1.2, "{0:.0f}%".format(c * 100))

        plt.savefig(self.midi_name + "Total Time by Channel.png")
        plt.show()

        # produce a global list for popluating top channels
        if int(len(self.channel_list_sorted) * 0.2) < 4:

            self.global_channel_list = self.channel_list_sorted[0:4]
        else:
            self.global_channel_list = self.channel_list_sorted[0:int(len(self.channel_list_sorted) * 0.2) + 1]
    def plot4(self):
        # Plotting pie chart for instrutment

        fig = plt.figure(figsize = (10, 8))
        self.clean_df_int = self.clean_df[self.clean_df.Instrument.notnull()]
        self.time_dict = dict()
        for i in list(set(self.clean_df_int.Instrument)):
            self.dloop = self.clean_df_int[self.clean_df_int.Instrument == i]
            self.dloop_zero = self.dloop[self.dloop.Velocity != 0]
            self.time_dict[i] = self.dloop_zero["Real_time"].sum()
        self.time_dict_sorted = sorted(self.time_dict.items(), key=lambda x: x[1],reverse= True)



        self.total_time = sum(list(self.time_dict.values()))

        self.instrument_list = list()
        self.time_list = list()


        for i in range(len((self.time_dict_sorted))):

            self.instrument_list.append(self.time_dict_sorted[i][0])
            self.time_list.append(self.time_dict_sorted[i][1])

        plt.pie(self.time_list, labels=self.instrument_list,
                        autopct='%1.1f%%', startangle=90)
        plt.title("Total Time by Instrument")
        plt.savefig(self.midi_name + "Total Time by Instrument.png")
        plt.show()
    def plot5(self):
        # plotting note wave
        self.dy = pd.DataFrame()
        fig = plt.figure(figsize=(20, 10))

        for i in self.global_channel_list:
            self.dloop = self.clean_df[self.clean_df.Channel == i]
            self.dloop["Time_CumSum"] = self.dloop.Real_time.cumsum()
            self.dy = self.dy.append(self.dloop)
            plt.plot(self.dloop["Time_CumSum"], self.dloop["Note"], label="Channel" + str(i))
            plt.legend(loc="lower right")

        plt.title("Note Wave by Top Channels")

        plt.savefig(self.midi_name + "Note Wave by Top Channels.png")
        plt.show()
    def plot6(self):
        # plotting wave of the midi volume
        self.dy = pd.DataFrame()
        fig = plt.figure(figsize=(20, 10))
        for i in self.global_channel_list:
            self.dloop = self.clean_df[self.clean_df.Channel == i]
            self.dloop["Time_CumSum"] = self.dloop.Real_time.cumsum()
            self.dy = self.dy.append(self.dloop)
            plt.plot(self.dloop["Time_CumSum"], self.dloop["Velocity"], label="Channel: " + str(i))
            plt.legend(loc="lower right")

        plt.title("Volume Wave by Top Channels")

        plt.savefig(self.midi_name + "Volume Wave by Top Channels.png")
        plt.show()



