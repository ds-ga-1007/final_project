# -*- coding: utf-8 -*-

import PrintFunctions as pt
from ClinicSearchByAddress import searchClinics
from ClinicSearchByAddress import exitStrategyAddress
import InputFunctions as ip 
import UserProfile as up
from NationalComparissonTime import plotter
from ComparissonStateWise2014 import generateStateTable, barh_chart

''' Main program '''

def runAllFunction():
    
    pt.delay_print("Hi! Welcome to the IVF-Search Clinic Program")
    pt.spacing()
    pt.instructions()
    big_data = ip.load_data()
    data2014 = big_data[2014]
    age, isDonnated, isFresh = up.userQuestions(instructions=True)
    
    repeatSearch = True 
    while repeatSearch is True: 
        clinics = searchClinics(big_data)
        pt.delay_print("This is what I found!!!")
        pt.spacing()
        pt.printPandasSeriesList([clinics.PrevClinName1, clinics.ClinCityCode, clinics.ClinStateCode])
        OkAnswer = False
        while OkAnswer is False:
            try: 
                repeatSearch = ip.delay_input("Do you want to repeat search using another address? [y/n]")
                repeatSearch = ip.yesNoParser(repeatSearch)
                OkAnswer = True
            except ip.yesNoParserException:
                pt.delay_print("Sorry, I didn't get that. \n Remember, that I can understand only yes or no answers \n ")
                pass
      
    pt.delay_print("Now...Please select a clinic of the above list using the number before the name so I can output the latest statistics! [number] \n")
    clinicSelectorNumeric = ip.selectorFromList(1, clinics.shape[0])
    selectedClinic = clinics[clinicSelectorNumeric-1:clinicSelectorNumeric]
    selectedClinic.reset_index(inplace=True, drop=True)
    userSpecification = up.identifier(age, isDonnated, isFresh, selectedClinic.ClinStateCode[0])
    
    exitStrategy = False   
    while exitStrategy is False:
        pt.delay_print("What do you want to do now? [number] \n")
        userSelection = ip.MultiOptionInput(["Compare clinic with state data in 2014", "Compare clinic with national data over time", "Select another clinic", "Exit this amazing program that deserves an A"])
        if userSelection==1:
            pt.delay_print("This table compares clinics over time")  
            generateStateTable(selectedClinic.PrevClinName1[0], selectedClinic.ClinStateCode[0], data2014, userSpecification)
            ip.continueFunction()
            pt.delay_print("SEE PLOT \n")
            barh_chart(selectedClinic.PrevClinName1[0], data2014, userSpecification, 1)           
            pt.delay_print("SEE PLOT \n")
            barh_chart(selectedClinic.PrevClinName1[0], data2014, userSpecification, 2)           
            exitStrategy = False
        if userSelection==2: 
            plotter(selectedClinic.PrevClinName1[0], userSpecification, big_data)
        if userSelection==3:
            pt.delay_print("Let me give you once again the list of clinics near you... \n")
            pt.printPandasSeriesList([clinics.PrevClinName1, clinics.ClinCityCode, clinics.ClinStateCode])
            pt.delay_print("Now...Please select a clinic of the above list using the number before the name so I can output the latest statistics! [number] \n")
            clinicSelectorNumeric = ip.selectorFromList(1, clinics.shape[0])
            selectedClinic = clinics[clinicSelectorNumeric-1:clinicSelectorNumeric]
            selectedClinic.reset_index(inplace=True, drop=True)
            userSpecification = up.identifier(age, isDonnated, isFresh, selectedClinic.ClinStateCode[0])                           
        if userSelection==4:
            exitStrategyAddress("Are you sure? [y/n]")       

if __name__ == '__main__':
    try:
        runAllFunction()
    except KeyboardInterrupt:
        pt.delay_print("\n Sorry to see you leave. Goodbye! \n")
        
        