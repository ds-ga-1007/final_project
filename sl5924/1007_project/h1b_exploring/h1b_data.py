"""
This is the h1b_data module of the project
calc_application_pool: calculate application pool in different levels
calc_approve_rate: calculte approve rate in different levels
calc_average_wage: calculate average wage in different levels
All calculations are for plot line charts and maps

Created on 2016/12/01
Version: 1.0
@author: Sheng Liu
ShengLiu Copyright 2016-2017

"""
import sys
import pandas as pd
import numpy as np

class h1b_data:
    def __init__(self,data):
        
        self.data = data
        self.states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', \
         'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', \
         'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', \
         'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',\
         'VA', 'WA', 'WV', 'WI', 'WY']


    def calc_application_pool(self,level,year = 2012):
        application_pool = []
        if level == 'Overview':
            for year in range(2010,2017):
                application_pool.append(len(self.data[year]))
            return application_pool
        elif level == 'Country':
            data = self.data
            for state in self.states:
                data_year_in_state = data[year][data[year]['EMPLOYER_STATE'] == state]
                application_pool.append(len(data_year_in_state))
            return application_pool
        elif level == 'State':
            data = self.data
            for YEAR in range(2010,2017):
                data_year_in_state = data[YEAR][data[YEAR]['EMPLOYER_STATE'] == year]
                application_pool.append(len(data_year_in_state))
            return application_pool


    def calc_approve_rate(self,level,year = 2012):
        data = self.data
        if level == 'Overview':
            APPROVE_RATE_LIST = []
            for year in range(2010,2017):
                is_approve = data[year]['STATUS_APPROVE']
                rate = sum(is_approve)/len(data[year])*100
                APPROVE_RATE_LIST.append(rate)
            return APPROVE_RATE_LIST
        elif level == 'Country':
            states = self.states
            APPROVE_RATE_LIST_Country = []
            for state in states:
                data_year_in_state = data[year][data[year]['EMPLOYER_STATE'] == state]
                is_approve =data_year_in_state['STATUS_APPROVE']
                rate = sum(is_approve)/len(data_year_in_state)*100
                
                APPROVE_RATE_LIST_Country.append(rate)
            return APPROVE_RATE_LIST_Country
        elif level == 'State':
            if year == 2012:
                year = 'CA'
            APPROVE_RATE_LIST_State = []
            for YEAR in range(2010,2017):
                data_year_in_state = data[YEAR][data[YEAR]['EMPLOYER_STATE'] == year]
                is_approve =data_year_in_state['STATUS_APPROVE']
                rate = sum(is_approve)/len(data_year_in_state)*100
                APPROVE_RATE_LIST_State.append(rate)
            return APPROVE_RATE_LIST_State


    def calc_average_wage(self,level,year=2012):
        data = self.data
        
        if level == 'Overview':
            AVERAGE_WAGE_LIST = []
            for year in range(2010,2017):
                AVERAGE_WAGE_LIST.append(np.mean(data[year]['PREVAILING_WAGE']))
            return AVERAGE_WAGE_LIST
        
        elif level == 'Country':
            AVERAGE_WAGE_LIST_Country = []
            for state in self.states:
                data_year_in_state = data[year][data[year]['EMPLOYER_STATE'] == state]
                AVERAGE_WAGE_LIST_Country.append(np.mean(data_year_in_state['PREVAILING_WAGE']))
            return AVERAGE_WAGE_LIST_Country

        elif level == 'State':
            if year == 2012:
                year = 'CA'
            AVERAGE_WAGE_LIST_State = []
            for YEAR in range(2010,2017):
                data_year_in_state = data[YEAR][data[YEAR]['EMPLOYER_STATE'] == year]
                AVERAGE_WAGE_LIST_State.append(np.mean(data_year_in_state['PREVAILING_WAGE']))
            return AVERAGE_WAGE_LIST_State

