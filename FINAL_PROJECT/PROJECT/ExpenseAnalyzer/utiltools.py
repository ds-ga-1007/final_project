# -*- coding: utf-8 -*-
"""
Created on Sat Dec 3 2016

@author: jub205/ak6201

@desc: This script contains utility tools for Election expense analyzer
"""

import pandas as pd
from datetime import datetime

def format_number(number):
    '''This function formats dollar amount and change type to float'''
    number = str(number).strip().replace('$','').replace(',','')
    if number.find('(')>=0:
        number = number.replace('(','').replace(')','')
        number = '-' + number
    
    return float(number)
    
def format_date(date):
    '''This function formats date in string format('mm/dd/YYYY') into Python datetime type'''
    
    formatted_date = datetime.strptime(str(date).strip(),'%m/%d/%Y').date()
    
    return formatted_date
 
def load_master_data():
    '''This function loads expense data and result data and creates a master dataframe
       with expense and result data merged
    '''
    
    print("Loading Master Data...Please wait")
    expensefilenames = ['data/all_house_senate_2010.csv', 'data/all_house_senate_2012.csv', 'data/all_house_senate_2014.csv']
    resultfilenames = ['data/result_2010.csv', 'data/result_2012.csv', 'data/result_2014.csv']
    
    masterdata = pd.DataFrame()
    
    for expense,result in zip(expensefilenames, resultfilenames):
        
        expensedata = load_expense_data(expense)
        resultdata = load_result_data(result)
        merged_data = merge_expense_result(expensedata, resultdata)
        merged_data.RESULT.fillna('L', inplace=True) #Fill RESULT column for losers
        masterdata = pd.concat([masterdata, merged_data])

    masterdata = masterdata.reset_index(drop=True)

    return masterdata
   
def load_expense_data(filename):
    '''This function loads the expense data from 2010 to 2014'''
    
    expensedata = pd.read_csv(filename)
    expensedata = expensedata.dropna()
    expensedata['dis_amo'] = expensedata['dis_amo'].apply(format_number)
    expensedata['dis_dat'] = expensedata['dis_dat'].apply(format_date)
    expensedata['month'] = expensedata['dis_dat'].apply(lambda x: x.month)
    expensedata['day'] = expensedata['dis_dat'].apply(lambda x: x.day)   

    return expensedata
    
def load_result_data(filename):
    '''This function loads the election result from 2010 to 2014'''
    
    result = pd.read_csv(filename)
    result = result.drop(['STATE'], axis=1)
    
    return result
        
def merge_expense_result(expensedata, resultdata):
    '''This function merges expense data and result data'''
    
    merged_data = pd.merge(expensedata, resultdata, how='left', on=['can_id'])
    
    return merged_data
