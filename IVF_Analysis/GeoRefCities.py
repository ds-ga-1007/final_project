# -*- coding: utf-8 -*-

''' This code generates a data frame with the cities georeferenced '''
''' It adds as columns the number of clinics per year '''
''' DANGER: Re-running this code would result in losing whatever was filled by hand '''

import pandas as pd
import numpy as np
import os
from geopy.geocoders import Nominatim

def ImportRawDataIVF(initYear, endYear):
    
    '''Function to import original data and append'''
    
    # Make sure your directory is correctly set    
    currentDirectory = os.getcwd()
    datadir = "/".join(currentDirectory.split('/')[0:-1]) + "/IVF_Analysis/Data/"
    alldataFrames = [] 
    
    for year in range(initYear, endYear + 1):
        yearlyData = pd.read_excel(datadir + "clinic_tables_data_" + str(year) + ".xls")
        yearlyData["year_id"] = year
        alldataFrames.append(yearlyData)
        
    DataFramesTogeteher = pd.concat(alldataFrames)
    return DataFramesTogeteher

def ClinicsByYearAndCity(initYear, endYear, cityVar='ClinCityCode', stateVar='ClinStateCode', yearVar='year_id'):
    
    ''' A function to give the number of observations in a Data Frame per year, city and state '''
    
    allData = ImportRawDataIVF(initYear, endYear)
    allData = allData[[cityVar, stateVar, yearVar]]
    allData["TotalObs"] = 1
    collapsedData = allData.groupby([cityVar, stateVar, yearVar])["TotalObs"].sum()
    collapsedData= collapsedData.unstack(level=-1)
    for x in range(initYear, endYear + 1):
        collapsedData = collapsedData.rename(index=str, columns={x: "y" + str(x)})
    collapsedData = collapsedData.replace(np.nan, 0)
    return collapsedData

citiesWithAClinic_07_14 = ClinicsByYearAndCity(2007, 2014)
index1 = [x[0] for x in citiesWithAClinic_07_14.index.values]
index2 = [x[1] for x in citiesWithAClinic_07_14.index.values]
citiesWithAClinic_07_14["AdressToQuery"] = str("NA")

for x in range(0, citiesWithAClinic_07_14.shape[0]):
    citiesWithAClinic_07_14["AdressToQuery"][x] = index1[x] + ", " + index2[x] + ", USA"
citiesWithAClinic_07_14.head()
     
citiesWithAClinic_07_14["lat"] = np.nan
citiesWithAClinic_07_14["lon"] = np.nan     

geolocator = Nominatim()
counter = 0
for x in range(0,len(citiesWithAClinic_07_14)):
    if np.isnan(citiesWithAClinic_07_14["lat"].iloc[x]):
        try:
            location = geolocator.geocode(citiesWithAClinic_07_14["AdressToQuery"].iloc[x], timeout=None)
            citiesWithAClinic_07_14["lat"].iloc[x] = location.latitude
            citiesWithAClinic_07_14["lon"].iloc[x] = location.longitude
        except:
            pass
    print(counter / len(citiesWithAClinic_07_14))
    counter += 1
        
currentDirectory = os.getcwd()
datadir = "/".join(currentDirectory.split('/')[0:-1]) + "/IVF_Analysis/Data/"
citiesWithAClinic_07_14.to_csv(datadir + "Georeferenced07_14.csv")

# FROM HERE, SOME VALUES HAVE TO BE COMPLETED BY HAND #