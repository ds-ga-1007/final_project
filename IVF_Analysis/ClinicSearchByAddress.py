# -*- coding: utf-8 -*-

import PrintFunctions as pt
import InputFunctions as ip
import numpy as np
import geocoder as geo
from geopy.distance import vincenty
import sys

''' One function, constructed using all the functions in ClinicSearcByAdress_Functions.py
    This function asks the user for his or her address and outputs the 10 nearest clinics.'''
    
class NoConectionException(Exception):
    
    '''Exception to raise when Internet connection is necessary but no connection is available 
       or when any other internet problem happens'''
    def __str__(self):
        return "Problems with internet connection"

def AddressLookUp():
    
    ''' Georeference the desired address using geocoder package '''
    ''' CAREFUL!!! With the API limit google has '''
    ''' If limit is expected to be surpased, use another provider '''
    ''' Check documentation for additional providers '''
    
    yourAddress = ip.delay_input("What's your address?")
    
    try:
        yourAddress = geo.google(yourAddress)
    except:
        #NOTE: All exceptions are inherited from the request package. 
        #      I have decided to catch them all instead
        raise NoConectionException() 
    
    return yourAddress
    
def AddressValidation(someAddress):    
    
    ''' Function that inputs 'geocoder.google.Google' class '''
    ''' Ask user if adrees it's his, returns True or False '''
    
    addressForUserValidation = someAddress.address
    userResponse = None
    while userResponse is None:
        try: 
            userValidation = ip.delay_input("Is this your address? [y/n] \n {} ".format(addressForUserValidation))
            userResponse = ip.yesNoParser(userValidation)     
        except ip.yesNoParserException: 
            pt.delay_print("Sorry, I didn't get that. \n Remember, that I can understand only yes or no answers \n ")
            pass        
    return userResponse

def exitStrategyAddress(someTextForQuestion):
    
    ''' Function to attend issues with address after user responds valid address and it's in fact invalid.
        let the user leave the possibility to exit program'''
    
    continueStrategyParsed = None
    while continueStrategyParsed is None:
        try: 
            continueStrategy =  ip.delay_input(someTextForQuestion)
            continueStrategyParsed = ip.yesNoParser(continueStrategy)
        except ip.yesNoParserException: 
            pt.delay_print("Sorry, I didn't get that. \n Remember, that I can understand only yes or no answers \n ")
            pass
    if continueStrategyParsed is True:
        pt.delay_print("Sorry to hear about that. Goodbye")
        sys.exit()
    else: 
        addressIsOk = False 
        
    return addressIsOk


def distanceEstimator(YourAddress):
    
    ''' Function to read the CSV with data from the clinics by city '''
    ''' It automatically adds a column with the distance to your address '''
    
    # CHECK PATH IS OK #
    clinicDataByYear = ip.importMyCsv("FIX_Georeferenced07_14", extraFilePath="IVF_Analysis/Data/", encoding="mac_latin2")
    clinicDataByYear["DistanceToAdressInMiles"] = np.nan
    for row in range(0, clinicDataByYear.shape[0]): 
        CityLatLonTouple = (clinicDataByYear.loc[1, "lat"], clinicDataByYear.loc[row, "lon"])
        distance = vincenty(YourAddress.latlng , CityLatLonTouple)
        clinicDataByYear.loc[row, "DistanceToAdressInMiles"] = distance.mi    
        
    return clinicDataByYear


def nearestCities(DataFrame, distanceVar="DistanceToAdressInMiles", countVar="y2014", idVar="AdressToQuery", nregistries=10):
    
    ''' Function to return the N nearest registries from a data frame'''
    
    DataFrame = DataFrame.sort_values(distanceVar, ascending=True)
    DataFrame = DataFrame[DataFrame[countVar] > 1]
    DataFrame.reset_index(inplace=True, drop=True) 
    numberOfRecords = DataFrame.loc[0, countVar]
    row = 0
    for x in range(1, DataFrame.shape[0]): 
        if numberOfRecords < nregistries:
            numberOfRecords += DataFrame.loc[x, countVar]
            row += 1 
    DataFrame = DataFrame[0:row + 1]
    return DataFrame[idVar]

def searcherOfClinics2014(YourAddress, dataDirectory):
    
    ''' Function to search the nearest clinics from you '''
    ''' Returns a pandas data frame with clinics for 2014 '''
    
    yourCities = distanceEstimator(YourAddress)
    yourCities = nearestCities(yourCities)
    clinicData = dataDirectory[2014]
    clinicData["AdressToQuery"] = clinicData["ClinCityCode"] + ", " + clinicData["ClinStateCode"] + ", USA"
    clinicData = clinicData[clinicData.AdressToQuery.isin(yourCities)]
    clinicData.reset_index(inplace=True, drop=True) 
    return clinicData
       
def searchClinics(dataDirectory):
    
    ''' Final functions to ask for adresss, overcome errors, and apply searcherOfClinics2014'''
    ''' It overcomes every possible mistake or error '''
    
    addressIsOk = False
    while addressIsOk is False: 
        
        try: 
            address = AddressLookUp()
            addressIsOk = AddressValidation(address)
            
            if addressIsOk is False: 
                pt.delay_print("Sorry about that, please repeat. Try to be more specific \n") 
            
            if address.address is None and addressIsOk is True: 
                addressIsOk = exitStrategyAddress("I still don't have your address \n This will terminate the program. Terminate? [y/n]")
        
            if address.country!= 'US' and addressIsOk is True:
                addressIsOk = exitStrategyAddress("I think your address is not in the US. \n This will terminate the program. Terminate? [y/n]")
        
        except NoConectionException:
            addressIsOk = exitStrategyAddress("I'm having trouble connecting to Internet. I can retry or terminate . Terminate? [y/n]")        
          

    pt.delay_print("Ok, now I'm going to search for at least 10  IVF clinics near you \n")
    pt.delay_print("...")
    pt.spacing()

    clinics = searcherOfClinics2014(address, dataDirectory)
    
    return clinics
