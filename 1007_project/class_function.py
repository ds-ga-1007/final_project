'''
Created on  Dec 5th 2016
@Project Name:World bank data explorer
@Author:Liwei Song, Zoe Ma, Yichao Chen
'''
import glob
import re
import csv
import sqlite3
import pandas as pd
import sys
import pickle

'''
This module contains all the class and functions used in main() in main file
It defines different error and exceptions and defines input requirement for year, feature and countries in forms of class
'''

#this function checks whether users input an empty list
def sub_input(list):
    #returns 1 if empty
    if len(list)==0:
        print('Nothing has been input into the system')
        return 1
    elif len(list)!=0:
        #returns 1 if not empty
        reedit=input('Do you want to edit your input?Y to edit,Q to exit the system,Anything else back to main menu')
        if reedit.upper()=='Y':
            print('Return to the input menu')
            return 0
        elif reedit.upper()=='Q':
            sys.exit(1)
        else:
            return 1
                   
#defines exception for all types of errors
class InputError(Exception):
    def __init__(self):
        pass

class CountryError(Exception):
    def __init__(self):
        pass

class YearError(Exception):
    def __init__(self):
        pass

class FeatureError(Exception):
    def __init__(self):
        pass
 

#define a db_build class for build a database
class db_build(object):
    #init attributes
    def __init__(self,name):
        self.name=name+'.db'
    def define_files(self):
        #define files and read in allfiles in specific fileholer.
        #fileholder could be changed so this could be put into general use
        feature_names=[]
        for name in glob.glob('./data/data_econ/*.csv'):
            feature_names.append(name)
        for demoname in glob.glob('./data/data_demo/*.csv'):
            feature_names.append(demoname)
        self.all_csv=feature_names
    def form_db(self):
        data_frames={}
        conn = sqlite3.connect(self.name)
        all_csv=self.all_csv
        for files in all_csv:
            #read in all csv and convert them to dataframes
            rd=pd.read_csv(files,index_col=1).drop('Unnamed: 0',1)
            newfile=files[17:-4]
            data_frames[newfile]=rd
        for key in data_frames:
            #convert dataframes into sql table
            df=data_frames[key]
            df.to_sql(key,conn ,if_exists='replace',index=False,)
        conn.commit()
        conn.close()


class country_interval(object):
    #define a country_input class
    def __init__(self,country_string):
        self.country_string=country_string
        if len(country_string)<=2:
            raise CountryError
        if country_string[0] != '[':
            raise CountryError
        if country_string[-1] !=']':
            raise CountryError
            #raise error if not in [] form
        countries=country_string[1:-1].split(',')
        with open('countryname_list.df', 'rb') as temc:
            country_df = pickle.load(temc)
        country_names=list(country_df['Country'])
        names=[]
        for country in countries:
            if country not in country_names:
                raise CountryError
            else :
                names.append(country)
        if len(names)==0:
            raise CountryError
        if len(names) != len(set(names)):
            raise CountryError
        self.names=names
        #make sure country names are unique and nonempty
        
class year_interval(object):
    def __init__(self,year_string):
        self.year_string=year_string
        if len(year_string)<=2:
            raise YearError
        if year_string[0] != '[':
            raise YearError
        if year_string[-1] !=']':
            raise YearError
        new_year=year_string[1:-1].split(',')
        with open('year_list.df', 'rb') as tem_yr:
            year_df = pickle.load(tem_yr)
        year_list=list(year_df['Year'])
        #later edit
        year_names=[]
        for y in new_year:
            if y.isdigit():
                if int(y) in year_list:
                    year_names.append(y)
                else: 
                    raise YearError
            else:
                raise YearError
        if len(year_names)!=2:
            raise YearError
        if len(year_names) != len(set(year_names)):
            raise YearError
        if year_names[-1]<year_names[0]:
            raise YearError
            #make sure the year input is in correct forms
        self.names=year_names
        #make sure the end year is larger than the begining year
        
class feature_interval(object):
    #define a feature_interval for feature input
    def __init__(self,feature_string):
        self.feature_string=feature_string
        if len(feature_string)<=2:
            raise FeatureError
        if feature_string[0] != '[':
            raise FeatureError
        if feature_string[-1] !=']':
            raise FeatureError
            #raise error if not in [] form
        features=feature_string[1:-1].replace(',',' ').split()
        feature_names=[]
        for name in glob.glob('./data/data_econ/*.csv'):
            feature_names.append(name[17:-4])
        for demoname in glob.glob('./data/data_demo/*.csv'):
            feature_names.append(demoname[17:-4])
            # form a feature list from all data
        names=[]
        for f in features:
            if f not in feature_names:
                raise FeatureError
            else :
                names.append(f)
                #raise error feature not in feature list
        if len(names)==0:
            raise FeatureError
        if len(names) != len(set(names)):
            raise FeatureError
        if len(names)>5:
            raise FeatureError
        self.names=names  
        #make sure length is not 0, and if length is larger than 5, return error



        
        
        
       
        
                
     
        
        
        
    
    