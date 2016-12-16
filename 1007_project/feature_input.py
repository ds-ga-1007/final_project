'''
Created on  Dec 5th 2016
@Project Name:World bank data explorer
@Author:Liwei Song, Zoe Ma, Yichao Chen
'''
from class_function import *
import sys
import pickle

'''
This module contains feature input function
'''

def feature_input():
    #create a dictionary contains all features with two key: economical features and demographical features
    feature_names=[]
    feature_dict={}
    feature_names=[]
    feature_dict={}
    feature_dict['Economical features']=[]
    feature_dict['Demographical features']=[]
    for name in glob.glob('./data/data_econ/*.csv'):
        feature_dict['Economical features'].append(name[17:-4])
        feature_names.append(name[17:-4])
    for demoname in glob.glob('./data/data_demo/*.csv'):
        feature_dict['Demographical features'].append(demoname[17:-4])
        feature_names.append(demoname[17:-4])
        
    
    feature_input=[]
    while True:
        try:
            #print out all features in two keys
            print('Economical features')
            print(feature_dict['Economical features'])
            print('Demographical features')
            print(feature_dict['Demographical features'])
            
                
            try:
                #ask users to choose features
                features=input('Input your interested features(Up to 5 each time) in forms of [X,Y,..Z]:\n Enter B to go back \nEnter Q to quit')
                if features.upper() == 'B':
                    break
                elif features.upper() == 'Q':
                    sys.exit(1)
                else:
                    while(True):
                        feature_list=feature_interval(features)
                        if len(feature_list.names)>5:
                               print('you input more than 5 feaures')
                        else:
                            feature_input=feature_list.names
                            break
                    break
            except FeatureError:
                print('Invalid feature selection')
        except KeyboardInterrupt:
            sys.exit(1)
        except EOFError:
            sys.exit(1)
    return feature_input
