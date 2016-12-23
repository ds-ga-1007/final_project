'''
Created on Dec 15, 2016

@author: sj238
'''
import sys
from Exception_list import *
from analysis import *


def overall_analysis(df):
    """
    This function used to display an interactive system letting the user to learn more
    about the Lending Club dataset.
    argument
    =========
    df: a dataframe

    """


    print ("================================  Lending CLub loan data Analysis  ==============================")
    print ("")
    print ("                 You can choose to learn more about the whole dataset: ")
    print ("              <a>  :  Learn about categorical data")
    print ("              <b>  :  Learn about numerical data")
    print ("              <c>  :  Learn about numerical vs. categorical data")
    print ("              <d>  :  Learn about numerical vs. numerical data")
    print ("              <e>  :  Learn about predicting interest rate using Gradient Boosted Regression Trees")
    print ("              <q>  :  Quit the program")
    print ("")
    print ("=================================================================================================")


    while 1:
        try:
            key = option_input()
            if key == 'a':
                cat_analysis(df)
            if key == 'b':
                num_analysis(df)
            if key == 'c':
                nvc_analysis(df)
            if key == 'd':
                nvn_analysis(df)
            if key == 'e':
                gbt_analysis(df)
                       
        except wrong_option_exception:
            print ("invalid option, please select from [a,b,c,d,x] or input 'q' to quit: ")
        
        
def option_input():
    """
    get the option selected by user, and verify it.
    Return
    ======
    return a verified option
    """
    print('')
    key = input("your_choice: ")
    options = list('abcdeq')
    if not(key in options):
        raise wrong_option_exception
    if key == 'q':
        print ('program shut down! bye!')
        sys.exit()
    return key
    