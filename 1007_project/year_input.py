'''
Created on  Dec 5th 2016
@Project Name:World bank data explorer
@Author:Liwei Song, Zoe Ma, Yichao Chen
'''
from class_function import *
import sys
import pickle
'''
This module contains year_input function
'''
def year_input():
    year_input=[]
    while True:
        try:
            #ask user to enter a year interval
            print('Enter your interested years, and enter B to go back')
            try:
                years=input('Enter your interested years [A,B](B>A), such as [1991,1992].: \nAvailable years are from 1991 to 2016, and enter Q to quit\n')
                if years=='B':
                    break
                elif years=='Q':
                    sys.exit(1)
                else:

                    years_list=year_interval(years)
                    year_input=years_list.names
                    year_input = list(map(int, year_input))
                    break
            except YearError:
                print('Invalid year Input')
        except KeyboardInterrupt:
            sys.exit(1)
        except EOFError:
            sys.exit(1)
    return year_input