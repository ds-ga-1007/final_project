# -*- coding: utf-8 -*-
"""
Created on Sat Dec 3 2016

@author: jub205/ak6201

@desc: This script contains functions for user interaction
"""
import ExpenseAnalyzer.DataHandler as dh
import numpy as np
import sys

VALID_YEARS = ['2010', '2012', '2014']

def print_description():
    '''This function prints overall behavior of the program'''
    intro = 'The following program is to visualize the distribution of expenditure\n'\
            'incurred by the US Senate and House candidates for the years 2010, 2012, 2014.\n'\
            'The distribution of expenditure is different in every state for every year the election was held.\n'\
            'Please choose from the below options to continue your analysis and visualiztion\n'
    print(intro)
    
def get_user_input(valid_input_list, prompt_msg="Please enter the option number: ", expected_len=1):
    '''This function is a generic user input handler. Valid input list
       is provided and used for input validation check
    '''
    
    input_valid = False
    
    while not input_valid:
        
        try:
            choice = input(prompt_msg).upper().split(',')
            choice = [i.strip() for i in choice]
        
        except KeyboardInterrupt:
            print("Keyboard Interrupt, terminating the program")
            sys.exit()
        
        else:
            if len(choice)==expected_len or len(choice)==(expected_len-1):
                valid_input_counter = 0
                for c in choice:
                    if c in valid_input_list:
                        valid_input_counter += 1
                if valid_input_counter == len(choice):
                    input_valid = True
                else:
                    print("Invalid input, please check!")
            else:
                print("Invalid input, please check!")

    return choice
    
def get_program_menu():
    '''This function asks user to choose an option for data analysis'''
    
    print("\nExpense Data analysis")
    print("[1] Analysis by Year")
    print("[2] Analysis by State")
    print("[3] Year Comparison analysis")
    print("[4] Exit the program")
    
    valid_input_list = ["1", "2", "3", "4"]
    
    choice = get_user_input(valid_input_list,"Please enter the option number: ")
    
    return choice
    
def yearly_analysis_menu(masterdata):
    '''This function is called when candidate analysis option is chosen.
       It asks user for addional choice for candidate expense data analysis
    '''
    
    year_data = dh.YearAnalyzer(masterdata)
        
    year = get_user_input(VALID_YEARS,"Please enter the year you are interested in[2010,2012,2014]: ")
    year = np.array(year).astype(int)
        
    year_data.set_year_data(year)
    
    GotoMainMenu = False
    
    while not GotoMainMenu:
        
        #Display available options for the user
        print("\n[1] Show quick summary of the year")
        print("[2] Show distribution of expenditure") 
        print("[3] Show expenditures by states")
        print("[4] Show Top/Bottom 5 candidates by expenditure")
        print("[5] Show Top/Bottom N candidates by expenditure *30 Max*")
        print("[6] Show Winners VS Losers expense comparison")
        print("[7] Show monthly expenditure")
        print("[8] Change Year")
        print("[0] Main Menu")
        
        menu_choice = get_user_input(["0","1","2","3","4","5","6","7","8"], "Please enter the option number: ")
        menu_choice = menu_choice[0]
        
        if menu_choice == "1":
            year_data.show_year_summary()
            input("\nPlease press ENTER to continue")
        elif menu_choice == "2":
            year_data.show_expense_distribution()
        elif menu_choice == "3":
            year_data.show_expense_by_state()
        elif menu_choice == "4":
            year_data.show_top_bottom_N(5)
        elif menu_choice == "5":
            N = get_user_input(np.arange(1,31).astype(str),"Please enter N[Max=30]: ")
            year_data.show_top_bottom_N(int(N[0]))
        elif menu_choice == "6":
            year_data.show_winner_vs_loser()
            year_data.show_winner_vs_loser_bar()
        elif menu_choice == "7":
            year_data.show_monthly_expense()
        elif menu_choice == "8":
            year = get_user_input(VALID_YEARS,"Please enter the year you are interested in[2010,2012,2014]: ")
            year = np.array(year).astype(int)
            year_data.set_year_data(year)
        else:
            GotoMainMenu = True
    
def state_analysis_menu(masterdata):
    '''This function is called when candidate analysis option is chosen.
       It asks user for addional choice for candidate expense data analysis
    '''
    state_data = dh.StateAnalyzer(masterdata)
    VALID_STATES = state_data.get_state_list()
    state_data.print_state_list()
    state = get_user_input(VALID_STATES, "Select the state: ")
    state = state[0]
    state_data.set_state_data(state) #Qeury data for given state
    
    GotoMainMenu = False
    
    while not GotoMainMenu:
        #Display available options for the user
        print("\n[1] Show quick summary of the state")
        print("[2] Show distribution of expenditure")
        print("[3] Show monthly expenditure")
        print("[4] Show winner vs loser comparison")
        print("[5] Change State")
        print("[0] Main Menu")
        
        menu_choice = get_user_input(["0","1","2","3","4","5"], "Please enter the option number: ")
        menu_choice = menu_choice[0]
        
        if menu_choice == "1":
            state_data.show_state_summary()
        elif menu_choice == "2":
            state_data.show_expense_distribution()
        elif menu_choice == "3":
            state_data.show_monthly_expense()
        elif menu_choice == "4":
            state_data.show_winner_loser_comparison()
        elif menu_choice == "5":
            VALID_STATES = state_data.get_state_list()
            state_data.print_state_list()
            state = get_user_input(VALID_STATES, "Select the state: ")
            state = state[0]
            state_data.set_state_data(state) #Qeury data for given state
        else:
            GotoMainMenu = True
    
def year_comparison_analysis_menu(masterdata):
    '''This function is called when candidate analysis option is chosen.
       It asks user for addional choice for candidate expense data analysis
    '''
    
    year_data = dh.YearAnalyzer(masterdata)
   
    year = get_user_input(VALID_YEARS,"Please enter the years you are interested in(comma separated)[2010,2012,2014 ONLY]: ", expected_len=3)
    year = np.array(year).astype(int)
        
    year_data.set_year_data(year) #Set filtered_data in YearAnalyzer
    
    GotoMainMenu = False
    
    while not GotoMainMenu:
        #Display available options for the user
        print("\n[1] Show distribution of expenditure by year")
        print("[2] Show monthly expenditure")
        print("[3] Show winner vs loser comparison")
        print("[0] Main Menu")
        
        menu_choice = get_user_input(["0","1","2","3"], "Please enter the option number: ")
        menu_choice = menu_choice[0]
        
        if menu_choice == "1":
            year_data.show_expense_distribution()
        elif menu_choice == "2":
            year_data.show_monthly_expense()
        elif menu_choice == "3":
            year_data.show_winner_vs_loser_bar()
        else:
            GotoMainMenu = True
        
    
    
