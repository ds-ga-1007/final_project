from project import *
import numpy
import pandas as pd
import os

'''
This program will add a new variable to the end of each dataframe
the variable will be the top class of the job type
'''

# Set working directory
datadir = 'C:/Users/Zhaopeng/1007/project/'
os.chdir(datadir)

# Read in csv containing the big class of the job type
defn = pd.read_csv('soc_2010_definitions.csv',encoding = 'iso-8859-1')
stc = pd.read_csv('soc_structure_2010.csv',encoding = 'iso-8859-1')
data = stc[stc['Major Group'].notnull()]
data = data.drop(data.columns[[1,2,3]], axis=1)
data.columns = ['Major','Title']
data.Title[0]

# convert the dataframe containing key and big class to a dictionary
data_stc = stc[stc['Major Group'].notnull()]
data_stc = data_stc.drop(data_stc.columns[[1,2,3]], axis=1)
data_stc.columns = ['Major','Title']
data_stc['Major'] = data_stc['Major'].apply(lambda x: x.split('-')[0])
dict = data_stc.set_index('Major')['Title'].T.to_dict()


'''
1, set all the variables to the same name in each year's file
2, SOC_CODE have a format of 11-1152, 11 represent the big class, 1152 represent the detailed class
3, clean the data where SOC_CODE is not formated
4, break the SOC_CODE by "-", and store the first two digit to a temp variable
5, create a new variable and mapping the value with the key
6, write the new dataframe to the csv
'''

data = {}
for year in range(2010,2017):
    data[year]= pd.read_csv('H-1B_FY'+str(year)+'_clean.csv',encoding = 'iso-8859-1')
    data[year].columns = ['CASE_NUMBER', 'CASE_STATUS', 'VISA_CLASS', \
       'EMPLOYER_NAME', 'EMPLOYER_CITY', 'EMPLOYER_STATE', 'SOC_CODE', \
       'SOC_NAME','JOB_TITLE', 'FULL_TIME_POSITION', 'PREVAILING_WAGE', \
       'PW_UNIT_OF_PAY', 'STATUS_APPROVE', 'RELOCATE', 'year']
    data[year] = data[year][~data[year].SOC_CODE.str.contains('Nov|132011|2-')]
    data[year] = data[year][data[year].SOC_CODE != '-']
    
    # several special class needed to be subtituted
    data[year].SOC_CODE.replace('15 - 1051', '15-1051', inplace = True)
    data[year].SOC_CODE.replace('15 -1051', '15-1051', inplace = True)
    data[year].SOC_CODE.replace('15 - 1132', '15-1132', inplace = True)
    temp = data[year].SOC_CODE.apply(lambda x: x.split('-')[0])
    data[year]['descrpt'] = temp
    data[year].replace({'descrpt': dict},inplace = True)
    
    # when the key contain the following number, they are invalid keys
    data[year] = data[year][~data[year].descrpt.str.contains(':13|16|10|14|20|28|1511|115|24|54|60|26')]
    data[year].to_csv('H-1B_FY'+str(year)+'_clean.csv', sep=',',encoding = "ISO-8859-1")