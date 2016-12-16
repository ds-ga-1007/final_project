'''
This module is for combining group data by year and state
Created on 2016.11.20.
'''
import pandas as pd
import numpy as np
import os

cwd = os.getcwd()
datadir = '/'.join(cwd.split('/')[0:-1])+'/Infectious-Diseases-and-Effects-of-Vaccines/'
df=pd.read_csv('dataset.csv',index_col=0)

#use loc instead of state because there are data for NY city, NY, NY upstate seperately
#so it causes potential duplicates( there are three state named NY so it retrieve NY three times
#also due to the system, same records will retrieve twice under certain condition
df=df.drop_duplicates()
grouped=df.groupby(['year','loc','disease']).sum()


grouped=grouped.drop('week',1)
grouped=grouped.reset_index()

#remove the data of new york city and upstate new york because it potentially clashes with new york
group_NYout=grouped[np.logical_and(grouped['loc']!='NEW YORK CITY',grouped['loc'] != 'UPSTATE NEW YORK')]



