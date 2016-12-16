'''
Created on Dec 15, 2016

@author: sj238
'''
import pandas as pd
from overall_analysis import *
from load_data import *
from clean_data import *

def main():
    raw_data = safely_input()
    print ("dataset loaded successfully >>>")
    print (">>>")

    # Then clean the data
    clean_data = Clean_df(raw_data)
    print ("data cleaned >>>")
    overall_analysis(clean_data)
    
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sys.exit()








