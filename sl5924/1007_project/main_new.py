"""
This is the main module of the project, all the functions are imported from package H1b

Author:  ShengLiu (sl5924)
"""

#from h1b_exploring import *

import sys
import pandas as pd
from h1b_exploring.exception_list import wrong_option_exception

from h1b_exploring.All_about_input import option_input,h1bdata_loading
from h1b_exploring.h1b_data import h1b_data
from h1b_exploring.Overview import overview
from h1b_exploring.Location import location
from h1b_exploring.company import company_exploring
from h1b_exploring.industry import industry_exploring


def main():
    """
    The whole project start here.
    """

    # start at loading the dataset
    data = h1bdata_loading()
    merged_data = pd.concat([data[year] for year in range(2010,2017)], ignore_index= True)
    raw_data = h1b_data(data)
    
  

    # Then clean the data
    #h1b_data = Clean_df(raw_data)
    #print("data cleaned >>>")


    while True:
        try:
            print ("================================ H1b Visa Approve Rate Exploring ================================")
            print ("")
            print ("                             How do you want to explore the H1b Data?                            ")
            print ("                              <a>  : Overview                              		                 ")
            print ("                              <b>  : Location                                                    ")
            print ("                              <c>  : Industry                                                    ")
            print ("                              <d>  : Company                                                     ")  
            print ("                              You can always input 'quit' to leave the system                    ")
            print ("=================================================================================================")

            key = option_input()
            if key == 'a':
                overview(data)
            if key == 'b':
                location(data)
            if key == 'c':
                industry_exploring(merged_data)
            if key == 'd':
                company_exploring(merged_data)
        except wrong_option_exception:
            print ("Invalid option, please reselect.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sys.exit()

