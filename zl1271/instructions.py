'''
Created on Dec 16, 2016

@author: felix
'''

def quit_instructions():
    print('Enter \'quit\' to quit.\n')

def begin_game_instructions():
    print('Enter \'all\' to run the full model predicting income.')
    print('Enter \'explore\' to explore the data')
    quit_instructions()

def explore_instructions():
    print('Enter \'describe\' to see plots')
    print('Enter \'regression\' to customize your regression model')
    quit_instructions()
    
def describe_instructions():
    print('Enter \'all\' to see a boxplot for all data on income')
    print('Enter \'sex\' to see income by sex')
    print('Enter \'race\' to see income by race')
    print('Enter \'age\' to see income by age')
    print('Enter \'educ\' to see income by years of education')
    quit_instructions()
    
def regression_instructions1():
    print('Enter \'all\' to use all data for regression')
    print('Enter \'part\' to set the category of your interest')
    quit_instructions()
    
def selec_predictor_instructions():
    print('Enter a variable to run a simple linear regress on income')
    print('Valid inputs include: \'age\', \'sex\', \'race\', and \'educ\' ')
    quit_instructions()
    
def regression_instructions2():
    print('Choose a category by enter \'sex\' or \'race\'')
    quit_instructions()
    
def regression_instructions3(first_instruction):
    print(first_instruction)
    quit_instructions()