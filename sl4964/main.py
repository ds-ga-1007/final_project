'''This is the main program. It gives the user two options: choose a song provided in the package, or provide a midi audio 
fileof their choice. Whatever file the user chooses, the program outputs a classification result, tellling the user if the
musical style of the audio file is closer to Jazz or Classical music. the program also visualizes the velocity and musical
notes of the audio file by different channels with both 2d and 3d plots.'''
#Wenjie: namemap is a df with 3 columns: MidiName, Label, and Prediction, which is 1 for Jazz and 0 for Classical. 
#When user puts in a number i, use the number as the index to get the MidiName:
# songname = namemap.loc[i]['MidiName'].  Get the song i's messages from df_toplot: df_toplot[df_toplot['MidiName' == songname]] for plotting.

from sys import stdout, exit
from time import sleep
import pandas as pd
from os import getcwd
from Errors import *
from ThreeD_plot import *
from TwoD_plot import *

instruction = 'This program uses a trained model to judge if a midi audio file has more Jazz influence or Classical influence.\
 We have built in some example audio files in the package, which are pop songs that reputedly have been influenced by either \
Jazz or Classical music. \nYou have the option of either providing your own midi file, or picking one from the built-in package.\
 Whichever midi file you choose, we will visualize that audio file interms of its instruments and velocity, as well as give a binary judgment of whether the song is\
 more Jazzy or Classical in style.\n The program takes up to one minute to load — please wait for the next prompt.\n'
cwd = getcwd()
BAUD = 300 #Change this to 200 before deployment
def baudout(s):
    for c in s:
        sleep(9/ BAUD)  # 8 bits + 1 stop bit @ the given baud rate
        stdout.write(c)
        stdout.flush()#borrowed from adventure game to simulate typing speed for printing instructions, with the aim of improved UX.
#https://github.com/ds-ga-1007/assignment5/blob/master/adventure/adventure.py
baudout(instruction)

from midi_to_dataframe import *
from Classifier import featureExtract, tokenize
from Classify import *
from midi_to_dataframe import *
from process_master import *

package_path = cwd + '/ToClassify'

df_toClassify = process_master(package_path, 2).result()
toClassify = featureExtract(df_toClassify)
prediction = toPredict(toClassify)
toClassify['Prediction'] = prediction #toClassify is a df with each song we provided as a row, some melody and time
#features used for classification, as well as the predicted label.
namemap = toClassify.drop(['Time_sequence', 'Percussion_time', 'Melody'], 1)
df_toplot = df_toClassify.merge(namemap, how = 'left') #This is a comprehensive df with each midi message of each
#provided song as a row, with predicted labels added as a new column. Can be easily used for plotting. Keep in mind
#that 'Prediction' stores the result, with 1 being Jazz and 0 being classical.


def letscontinue():
    baudout('On to the next song: if you want to choose one of the songs provided in the package, type 1.\
If you want to provide your own midi file, type 2. To quit, simply type \'quit\' and enter.')
    option = input()
    return option
    


baudout('Now, if you want to choose one of the songs provided in the package, type 1. \n\
If you want to provide your own midi file, type 2 and enter.')

option = input()
while True:
    if option == '1':
        baudout('Provide a number between 1 to 28 for your lucky pick from our song library. For example, number 8 is a good start.\n')
        input1 = input()
        if input1 == 'quit':
            exit()
        else:
            #try:
            song = int(input1) - 1
            songname = namemap.iloc[song]['MidiName']
            artist = df_toplot[df_toplot['MidiName']==songname]['Artist'].unique()[0]
            if namemap.iloc[song]['Prediction'] == 1:
        
                prediction = 'The song you picked is {} by {}. It is influenced more heavily by Jazz than Classical mucic.\n\n'.\
                format(songname, artist)
                baudout(prediction)
                visual_Vel(df_toplot[df_toplot.MidiName == songname], 1)
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot1()
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot2()
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot3()
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot4()
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot5()
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot6()
                except:
                    pass
                    #Insert plotting function here. Incorporate the prediction  in the plot, using matplotlib.text.Text.
                    #df_to_plot[df_to_plot.MidiName == songname] will give you the dataframe slice for the chosen song.
                option = letscontinue()
                    
            else:
                prediction = 'The song you picked is {} by {}. It is influenced more heavily by Classical than Jazz mucic.\n\n'.\
                format(songname, artist)
                baudout(prediction)
                visual_Vel(df_toplot[df_toplot.MidiName == songname], 0)
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot1() 
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot2() 
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot3() 
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot4() 
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot5() 
                except:
                    pass
                try:
                    plot(df_toplot[df_toplot['MidiName']==songname]).plot6() 
                except:
                    pass
                    #Insert plotting function here. Incorporate the prediction  in the plot, using matplotlib.text.Text.
                option = letscontinue()


            #except:
                #print(InputError('Invalid input. You have to put in a number from 1 through 28 to pick one out of the 28 songs\
#included in the library. Type any number from 1 through 28, and hit enter.\n').message)
            
                
    elif option == '2':
        #We need to deal with the scenario where users put in a type 0 midi file!
        while option == '2':
            baudout('Type in the absolute directory of the midi file that you want us to classify (e.g. /Users/ShashaLin/Desktop/Filename.mid)\n')
            
            directory = input()
            
            
            if directory == 'quit':
                break
            #try:   
            df_user = midi_to_dataframe(directory, 0).result() #This is the df for plotting
            feature_user = featureExtract(df_user)
            if toPredict(feature_user)[0] == 0:
                prediction = 'The song you picked is influenced more heavily by Classical than Jazz mucic.\n\n'#prediction is the classification result for user input midi file. 1 is Jazz
                   #0 is classical.
            if toPredict(feature_user)[0] == 1:
                prediction = 'The song you picked is influenced more heavily by Jazz than Classical mucic.\n\n'#
                       
            baudout(prediction)
            visual_Vel(df_user, toPredict(feature_user)[0])
            try:
                plot(df_user).plot1()
            except:
                pass
            try:
                plot(df_user).plot2()
            except:
                pass
            try:
                plot(df_user).plot3()
            except:
                pass
            try:
                plot(df_user).plot4()
            except:
                pass
            try:
                plot(df_user).plot5()
            except:
                pass
            try:
                plot(df_user).plot6()
            except:
                pass
                    #Insert plotting function here. Incorporate the prediction  in the plot, using matplotlib.text.Text.
                    #Use df_user as the df for plotting
            option = letscontinue()
            if option == 'quit':
                break

            #except:
                #baudout(FileError('Unfortunately, the unlikely event happened that your midi file is encoded in a way that cannot be parsed by the program. \n Try entering another midi file path for prediction.\n').message)
    elif option == 'quit':
            break
    else: 
        print(InputError('Invalid Input. Please type either 1 or 2, then enter. If you want to quit the program, simply type \'quit\' and enter.\n').message)
        option = input()
        
