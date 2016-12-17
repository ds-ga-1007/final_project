# -*- coding: utf-8 -*-
"""
Created on Sat Dec 3 2016

@author: jub205/ak6201

@desc: This program loads spending data for Federal election from year 2010,2012 and 2014
       and election result data from the same years. The program offers statistics analysis
       of expense data by year, state and also offers comparison of multiple years.
       It has visualization of data in different formats of charts; Histogram, line chart,
       bar chart and boxplots to visualize the analysis of data that the user is interested in.
"""

import ExpenseAnalyzer.utiltools as ut
import ExpenseAnalyzer.interface as inter
import sys

def main():
    
    ExitLoop = False #Exit loop condition holder
    
    try:
        masterdata = ut.load_master_data()
    except OSError:
        print("Error Loading Data files")
        sys.exit()

    inter.print_description() #Show program description when the program starts
    
    while not ExitLoop:
        
        MainMenu = inter.get_program_menu()
        MainMenu = MainMenu[0]
        
        if MainMenu == '1':
            #Single year analysis
            inter.yearly_analysis_menu(masterdata)
            
        elif MainMenu == '2':
            #State analysis
            inter.state_analysis_menu(masterdata)
            
        elif MainMenu == '3':
            #Multiple year comparison
            inter.year_comparison_analysis_menu(masterdata)
            
        else:
            ExitLoop = True
            pass
        
        
if __name__ == "__main__":
    
    try:
        main()
        
    except KeyboardInterrupt:
        print("Keyboard interrupted, Terminating the program")
        sys.exit()
    
