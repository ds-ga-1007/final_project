'''
Created on  Nov 20th 2016
@Project Name:World bank data explorer
@Author:Liwei Song, Zoe Ma, Yichao Chen
'''


import glob
from class_function import *
import sys
from country_input import *
from year_input import *
from feature_input import *
from db_input import *
import pickle
from plot_input import *
'''
This is the main module for the world bank data explorer.
It contains two stages: 
1, User has to input all required values for features, years interval and country lists in a required format
2,User could choose one plot type outof 8 types, and users could return to the first stage flexibly to edit those three input values.
'''

def main(countries,features,years,a):
    try:
        a=a
        print('countries,year,features')
        print (countries,features,years)
        while True:
            #List all the possible options for the user
            print('################################################################################')
            print('This is the variables input menu, and you have 5 options')
            print('option1:enter database builder, option2: choose interested countries\noption3: choose interested features option4: choose interested year(s).\nPlease choose values for countries, features and years to next stage')
            print('Or you could enter Q to exit the system \nenter C to continue \n')
            main_input=input('enter your options from [1,2,3,4,C,Q]:\n')
            option_list=['0','1','2','3','4','Q','C','c']
            #print out invalid message for invalid input
            if main_input not in option_list:
                print('You enter an invalid option\n')
            elif main_input.upper()=='C':
                if len(countries)==0 or len(features)==0 or len(years)==0:
                    print('\n\nCould not proceed to the next stage,\nas one of the three attributes might be empty\n ')
                else:
                    break
            elif main_input.upper()=='Q':
                sys.exit(1)
            elif int(main_input)==1:
                database_builder()
                while True:
                    #give user to quit or go back to previous/main menu
                    db_end=input('\nYou want to exit(E) the system, or you want to return(R) to the main menu?\n')
                    if db_end not in ['E','e','R','r']:
                        print('Invalid Input\n')
                    elif db_end.upper()=='E':
                        sys.exit(1)
                    else:
                        break

            elif int(main_input)==2:
                b=0
                while (b==0):
                    countries=country_input()
                    b=sub_input(countries)
            elif int(main_input)==3:
                b=0
                while (b==0):
                    features=feature_input()
                    b=sub_input(features)
            elif int(main_input)==4:
                b=0
                while (b==0):
                    years=year_input()
                    b=sub_input(years)
            elif main_input.upper()=='C':
                break
            else:
                sys.exit()
        print('################################################################################')      
        print('countries,year,features\n')
        print(countries, years, features)
        print('################################################################################')
          
    except KeyboardInterrupt:
        sys.exit(1)
    except EOFError:
        sys.exit(1)     
    return (countries, years, features,a)

def main2(countries,features,years,a):
    #convert years from an interval to a list of integers
    years=list(range(years[0],years[-1]))
    print('################################################################################')
    print('\nHere are your interested countries list')
    print(countries)
    print('Here are your interested features list')
    print(features)
    print('Here are your interested years list')
    print(years)
    print('################################################################################')
    while(True):
        print('################################################################################')
        quit_option=input('Enter R to return to the variable input menu to edit.\nE to exit the system.\nAnything else to continue\n');
        print('################################################################################')
        if quit_option in ['R','r']:
            a=1
            plot_option=None
            one_feature=None
            break
        elif quit_option in ['E','e']:
            sys.exit(1)
        else:
            try:
                while(True):
                    #ask user to choose plot types later
                    print('You could see different types of plots in the next stage !Enter Q to exit now.Anything else to continue')
                    one_feature=input('Your choice\n')
                    if one_feature=='Q':
                        sys.exit(1)
                    else:
                        print('Now choose your desired plot type')
                        a=plot_input(years,features,countries)
                    a=0
                    break
            except KeyboardInterrupt:
                sys.exit(1)
            except EOFError:
                sys.exit(1)
            
               
    return  a 
                
               

        
            
if __name__ == "__main__":
    #excute the code below when we run this module as the main file.
    try:
        print('Welcome to the world bank data explorer')
        countries=[]
        years=[]
        features=[]
        a=1
        while(a==1):
            countries, years, features,a = main(countries,features,years,a)
            a=main2(countries,features,years,a)
    except KeyboardInterrupt:
        sys.exit(1)
    except EOFError:
        sys.exit(1)