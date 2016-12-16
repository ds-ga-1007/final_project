'''This is a module for classification created by Shasha Lin.
It extracts from the pooled midi dataframe features of melody and beats, using the method from this paper:
http://cs229.stanford.edu/proj2014/Kedao%20Wang,%20Predicting%20Hit%20Songs%20with%20MIDI%20Musical%20Features.pdf'''

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from scipy.sparse import hstack
from sklearn.linear_model import SGDClassifier

def featureExtract(md):
    #Get a df with note duration information.     
    modeldf = pd.DataFrame()
    modeldf['MidiName'] = md.MidiName.unique()
    realtime = list()
    for name in modeldf.MidiName.unique():
        realtime.append(','.join(md[md.MidiName == name].Real_time.astype(str)))
    modeldf['Time_sequence'] = realtime 

    #Extract percussion note duration as a separate Feature
    percussionTime = list()
    for name in modeldf.MidiName.unique():
        slice1 = md[md.MidiName == name]
        slice2 = slice1[slice1.Type == 'Percussion Track 10']
        percussionTime.append(','.join(slice2.Real_time.astype(str)))
    modeldf['Percussion_time'] = percussionTime
    modeldf['Percussion_time'] =  modeldf['Percussion_time'].replace('', np.nan)
    
    #Extract melody information as instrument + note tokens, separated by comma.
    melody = list()
    for name in modeldf.MidiName.unique():
        slice1 = md[md.MidiName == name]
        melody.append(slice1[slice1['Instrument'].notnull()]['Instrument'] + 
                      slice1[slice1['Instrument'].notnull()]['Note'].astype(str))
    for index in modeldf.index:
        modeldf.loc[index, 'Melody'] = ','.join(melody[index])
    
    #Add label to dataframe, with 1 being Jazz and 0 being Classical.
    label = list()
    for name in modeldf.MidiName.unique():
        if (md[md.MidiName == name]['Genre'] == 'Jazz').sum() > 0:
            label.append(1)
        else:
            label.append(0)
    modeldf['Label'] = label
    return modeldf

#customerized tokenizer
def tokenize(text):
    return(text.split(','))

def classify(modeldf): #builds the classification model and save it as a pickle file for later use with user input midi.
    
    train = modeldf.sample(frac = .8) 
    test = modeldf.drop(train.index)
    
    #following 3 blocks of code extracts the time, percussion, melody features using tfidf vectorizer, and saves the vectorizer
    #in pickle files for later feature extraction from user input midi.
    tfidfTime = TfidfVectorizer(tokenizer = tokenize, ngram_range=(2, 3))
    Time_sequencex = tfidfTime.fit_transform(modeldf.Time_sequence)
    joblib.dump(tfidfTime, 'tfidfTime.pkl')

    tfidfPercussion = TfidfVectorizer(tokenizer = tokenize, ngram_range=(2, 3))
    Percussion_timex = tfidfPercussion.fit_transform(modeldf.Percussion_time.astype(str))
    joblib.dump(tfidfPercussion, 'tfidfPercussion.pkl')

    tfidfMelody = TfidfVectorizer(tokenizer = tokenize, ngram_range=(2, 3))
    Melodyx = tfidfMelody.fit_transform(modeldf.Melody)
    joblib.dump(tfidfMelody, 'tfidfMelody.pkl')
    
    #This is the sparse feature matrix
    featuresx = hstack([Time_sequencex, Percussion_timex, Melodyx]) 
    
    #Train the model, test it, and save the model as a picle file
    sgd = SGDClassifier()
    sgd.fit(featuresx.tocsr()[train.index, :], train.Label)
    score = sgd.score(featuresx.tocsr()[test.index, :], test.Label)
    joblib.dump(sgd, 'sgd.pkl')
    


