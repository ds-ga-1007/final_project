# -*- coding: utf-8 -*-

''' General module for input functions and parsers from user inputs'''

import time
import sys
import os
import pandas as pd
import PrintFunctions as pt


def delay_input(myInput, timeSleep=0.04):
    
    ''' Function to pretty print output, letter by letter
        The function accepts a parameter that is the the time it takes to print '''  
    # This function was adapted form the delay_print: from: http://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
    
    s = myInput + "\n >> "
    for c in s:
        sys.stdout.write( '%s' % c )
        sys.stdout.flush()
        time.sleep(timeSleep)
    return input()


class yesNoParserException(Exception):
    
    ''' Exception when input "yes" or "no" was not recognized '''
    def __str__(self):
        return "Impossible to parse Yes/No input"

def yesNoParser(UserInput):
    
    '''Function to parse Yes/No answers. If not possible, raise yesNoParserException'''
    ''' The list includes every possible positive or negative responses from users '''
   
    listOfYes = ["yes", "Yes", "yEs", "yeS", "y", "Y", "yES", "YES", "YEs", "YeS", "True", "1", "ok", "Ok", "OK"]
    listOfNo = ["no", "No", "nO", "NO", "n", "N", "False", "0"]
    
    if (UserInput in listOfYes):
        return True
    elif (UserInput in listOfNo):
        return False
    else: 
        raise yesNoParserException()
    
   
def importMyCsv(file_name, extraFilePath="", header=0, encoding = "utf-8"):
    
    '''Function to import csv from upper level dir: assumes header but can change defaults'''
    
    currentDirectory = os.getcwd()
    datadir = "/".join(currentDirectory.split('/')[0:-1]) + "/"
    file = pd.read_csv(datadir + extraFilePath + file_name + ".csv", header=header, encoding=encoding)
    return file

def load_data(comments=True):
    
    '''This function loads multiple data files from the Data directory'''
    
    data_all = {}
    years = range(2007, 2015)
    
    # Check final directory. 
    currentDirectory = os.getcwd()
    datadir = "/".join(currentDirectory.split('/')[0:-1]) + "/IVF_Analysis/Data/"
    
    if comments is True:
        pt.delay_print("Give me a couple of seconds to load the data \n")
    
    for year in years:
        data = pd.read_excel(datadir + 'clinic_tables_data_' + str(year) + '.xls')
        data_all[year] = data
        if year == 2010 or year==2013:
            if comments is True:     
                pt.delay_print("... \n", 0.1)
            
    if comments is True:        
        pt.delay_print("READY!!! \n")
    
    return data_all
    
class nonNumericInput(Exception):
    
    ''' Exception when non numeric input is typed where numeric is expected '''
    def __str__(self):
        return "Numeric input needed"
    
class negativeInput(Exception):
    
    ''' Exception when negative input is given and positive is expected '''
    def __str__(self):
        return "Positive input needed"    
    
class nonIntegerInput(Exception):
    
    ''' Exception when non-integer input is given and integer is expected '''
    def __str__(self):
        return "Integer input needed"        

def wholeNumericPositiveInputParser(UserInput):
    
    '''Function to parse whole numeric input. If not possible, raise exceptions'''
    
    try: 
        UserInput = float(UserInput)
    except ValueError: 
        raise nonNumericInput()
    
    if UserInput<0:
        raise negativeInput()
    
    if UserInput.is_integer() is False: 
        raise nonIntegerInput()
        
    return int(UserInput)
        
def MultiOptionInput(listOfOptions):
    
    '''Function to ask user to select from several options'''
    
    pt.delay_print("*Input the number of your selection* \n")

    for number in range(0, len(listOfOptions)):
        string = str(number +  1) + ") " + listOfOptions[number] + "\n"
        pt.delay_print(string)
    
    answerIsOk = False
    while answerIsOk is False:
        
        try: 
            userSelection = input(" >> ")    
            userSelection = wholeNumericPositiveInputParser(userSelection)   
            if userSelection>len(listOfOptions) or userSelection==0:
                pt.delay_print("Sorry, range out of bounds \n")  
                pt.delay_print("Please enter a whole number between {} and {} \n".format(1, len(listOfOptions))) 
                answerIsOk = False
            else: 
                answerIsOk = True
                     
        except negativeInput:
            pt.delay_print("Sorry, I can't accept negative numbers numbers \n")
            pt.delay_print("Please enter a whole number between {} and {} \n".format(1, len(listOfOptions))) 
            pass
        except nonNumericInput:
            pt.delay_print("Sorry, I can only accept numbers \n")
            pt.delay_print("Please enter a whole number between {} and {} \n".format(1, len(listOfOptions))) 
            pass
        except nonIntegerInput:  
            pt.delay_print("Sorry, I can't accept any real number, just whole numbers \n")
            pt.delay_print("Please enter a whole number between {} and {} \n".format(1, len(listOfOptions)))   
            pass
    
    return userSelection 

def selectorFromList(minSelection, maxSelection):
    
    ''' Same function as above, but to select one option of a previously printed list '''
    
    answerIsOk = False
    while answerIsOk is False:
        
        try: 
            userSelection = input(" >> ")    
            userSelection = wholeNumericPositiveInputParser(userSelection)   
            if userSelection>maxSelection or userSelection<minSelection:
                pt.delay_print("Sorry, range out of bounds \n")  
                pt.delay_print("Please enter a whole number between {} and {} \n".format(minSelection, maxSelection)) 
                answerIsOk = False
            else: 
                answerIsOk = True
                     
        except negativeInput:
            pt.delay_print("Sorry, I can't accept negative numbers numbers \n")
            pt.delay_print("Please enter a whole number between {} and {} \n".format(minSelection, maxSelection)) 
            pass
        except nonNumericInput:
            pt.delay_print("Sorry, I can only accept numbers \n")
            pt.delay_print("Please enter a whole number between {} and {} \n".format(minSelection, maxSelection)) 
            pass
        except nonIntegerInput:  
            pt.delay_print("Sorry, I can't accept any real number, just whole numbers \n")
            pt.delay_print("Please enter a whole number between {} and {} \n".format(minSelection, maxSelection))   
            pass
        
    return userSelection

def continueFunction():
    
    ''' Function to ask user to coninue'''
    ''' It should only be a pause '''
    
    userResponse = None
    while userResponse is None:
        try: 
            userValidation = delay_input("Continue? [y/n]")
            userResponse = yesNoParser(userValidation)
            if userResponse is False: 
                userResponse = None   
        except yesNoParserException: 
            pt.delay_print("Sorry, I didn't get that. \n Remember, that I can understand only yes or no answers \n ")
            pass        
    return userResponse
    
    