'''
Created on  Dec 5th 2016
@Project Name:World bank data explorer
@Author:Liwei Song, Zoe Ma, Yichao Chen
'''
from class_function import *
import sys
import pickle
import pandas as pd

'''
This module contains the contry input function
'''

def country_input():
    #I have convert the all countryname into a dataframe saved in pickle
    with open('countryname_list.df', 'rb') as c_handle:
        country_names = pickle.load(c_handle)
    country_names=list(country_names['Country'])
    init={}
    for country in country_names:
        if country[0] not in init:
            init[country[0]]=[]
            init[country[0]].append(country)
        else:
            init[country[0]].append(country)
    #create a dictionary using initial letters of countries the keys.
    init_dic=list(init.keys())

    country_input=[]
    while True:
        try:
            #ask users to enter a list of countries
            print('Enter countries names in forms of list,such as [A, B, C]!\nNo white space between country names')
            countries=input("Please enter your interested countries! Enter H for country name lookup!\nEnter B to return to main menu\nEnter A for all countries and enter Q to quit:\nIf you choose all, be cautions with tons of plots")
 
            if countries=='H':
                while True:
                    #ask users to input initial letter to look up countries
                    country_init=input('Please enter the initial your country, and enter Back to go back：\n')
                    
                    if country_init not in init_dic and country_init != 'Back':
                        print ('Invalid country name initial\n')
                    elif country_init == 'Back':
                        break
                    else:
                        print (init[country_init])
            #give options to alternae or quit and etc.
            elif countries=='B':
                break
            elif countries=='A':
                country_input=country_names
                break
            elif countries=='Q':
                sys.exit()
                    
            else:
                try:
                    country_list=country_interval(countries)
                    country_input=country_list.names
                    break
                except CountryError:
                    print('Invalid country name\n')
        except KeyboardInterrupt:
            sys.exit(1)
        except EOFError:
            sys.exit(1)
    return country_input