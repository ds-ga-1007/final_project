

import sys
import pandas as pd

from h1b_exploring.All_about_input import option_input
from h1b_exploring.exception_list import wrong_option_exception

from h1b_exploring.class_collections_ranking import industry_level
from h1b_exploring.popular_industry import popular_industry
from h1b_exploring.customized_industry import customized_industry

'''
industry_exploring(merged_data)
'''
def industry_exploring(data):
    
    print("loading data....")
    industry_data = industry_level(data)
    
    Flag = True
    
    while Flag:
        try:
    

            print ("================================ H1b Visa Approve Rate Exploring ================================")
            print ("")
            print ("                             Please choose ONE level you interested in                           ")
            print ("                              <a>  : Popular Industry                                            ")
            print ("                              <b>  : Customized Job Inquiry                                      ")
            print ("                              <r>  : Go back to main menu                                        ")  
            print ("")
            print ("=================================================================================================")
   
            key = option_input()
            if key == 'a':
                popular_industry(industry_data)
            if key == 'b':
                customized_industry(industry_data, data)
            if key == 'r':
                Flag = False
        except wrong_option_exception:
            print ("Invalid option, please reselect.")
            
