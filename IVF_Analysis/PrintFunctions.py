# -*- coding: utf-8 -*-

''' General module for functions for pretty printing '''

import time
import sys

def delay_print(s, timeSleep =0.04):
    
    ''' Function to pretty print output, letter by letter
        The function accepts a parameter that is the the time it takes to print '''    
    # Delay print function from: http://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
    
    for c in s:
        sys.stdout.write( '%s' % c )
        sys.stdout.flush()
        time.sleep(timeSleep)


def spacing(n=1):
    
    ''' Function for vertical spacing between printing lines. Default = 1 '''
    for x in range(0,n):
        print("\n")    
        
def instructions():
    delay_print("I am designed to explore clinics that perform In Vitro Fertilization (IVF) across the United States \n") 
    delay_print("Whenever you see a '>>' symbol,  means I'm expecting an answer from you \n")
    delay_print("If after each question you see '[y/n]', it means I'm expecting a 'yes' or 'no' type of answer \n")
    delay_print("If after each question you see '[number]', it means I'm expecting a number \n")
    delay_print("You can always quit the program by typing ctrl-c \n")
    delay_print("Lets get going!!")
    spacing()           
        
def printPandasSeries(pandasSeries):
    
    ''' Function to pretty print any pandas series '''
    ''' Uses delay_print with lower timeSleep param '''
    
    pandasSeries.reset_index(inplace=True, drop=True)
    for row in range(0, len(pandasSeries)):
        string = str(row) + ") " + pandasSeries[row] + "\n"
        delay_print(string, 0.01)
        
def printPandasSeriesList(listOfPandasSeries, sep=", "):
    
    ''' Function to pretty print list of pandas series '''
    ''' it concatenates by row using "sep", and prints using numbers "x)"'''
    ''' CAREFULL --> Series must be the same size. Function takes the size '''
    ''' of first series in the list'''
    
    for row in range(0, len(listOfPandasSeries[0])):
        string = str(row + 1) + ") " + listOfPandasSeries[0][row]
        for series in range(1, len(listOfPandasSeries)):
            string = string + sep + listOfPandasSeries[series][row]
        
        string = string + "\n"
        delay_print(string, 0.01)   
        
 
        