'''
Created on Dec 10, 2016

This is the module to predict the genre of unlabeled midi files 

@author: ShashaLin
'''
from midi_to_dataframe import *
from process_master import *

from sklearn.externals import joblib
from scipy.sparse import hstack

tfidfTime = joblib.load('tfidfTime.pkl') 
tfidfPercussion = joblib.load('tfidfPercussion.pkl') 
tfidfMelody = joblib.load('tfidfMelody.pkl') 
sgd = joblib.load('sgd.pkl') 

def toPredict(test):
    'This function does the prediction'
    Time_sequencey = tfidfTime.transform(test.Time_sequence)
    Percussion_timey = tfidfPercussion.transform(test.Percussion_time.astype(str))
    Melodyy = tfidfMelody.transform(test.Melody)
    featuresy = hstack([Time_sequencey, Percussion_timey, Melodyy]) 
    prediction = sgd.predict(featuresy.tocsr())
    
    return prediction





