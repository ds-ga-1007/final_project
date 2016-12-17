'''
Created on Nov 27, 2016

@author: Yovela
'''
import sys
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display


class city_level:
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.newdf = city_level.city(self,dataset)

    def city(self,dataset):
    # calculate required statistics
        application_pool = (dataset.groupby("EMPLOYER_CITY").count())["STATUS_APPROVE"]
        approved_case = (dataset.groupby("EMPLOYER_CITY").sum())["STATUS_APPROVE"]
        approval_rate = (dataset.groupby("EMPLOYER_CITY").mean())["STATUS_APPROVE"]
        average_wage = (dataset.groupby("EMPLOYER_CITY").mean())["PREVAILING_WAGE"]
    
    # create a new DataFrame and rename indexes
        city_data = pd.concat([application_pool, approved_case, approval_rate,average_wage], axis =1)
        city_data.columns.values[0] = "application_pool"
        city_data.columns.values[1] = "approved_case"
        city_data.columns.values[2] = "approval_rate"
        city_data.columns.values[3] = "average_wage"
    
        return city_data

    def city_application_pool(self, city_level, city):
        return city_level.newdf.ix[city, "application_pool"]

    def city_approved_case(self, city_level, city):
        return city_level.newdf.ix[city, "approved_case"]
    
    def city_approval_rate(self, city_level, city):
        return city_level.newdf.ix[city, "approval_rate"]
    
    def city_average_wage(self, city_level, city):
        return city_level.newdf.ix[city, "average_wage"]
    
    def city_rank(self, city_level, n, indicator):
        # rank top n cities by indicator
        city_rank = city_level.newdf.sort_values(by = indicator).ix[-n:, indicator]
        city_rank.plot(kind = "barh", alpha = 0.7)
        plt.title("Top"+ str(n) + " Cities with highest " + indicator)
        return     

'''
industry level
'''

class industry_level:
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.newdf = industry_level.industry(self, dataset)

    def industry(self, dataset):
    # calculate required statistics
        application_pool = (dataset.groupby("descrpt").count())["STATUS_APPROVE"]
        approved_case = (dataset.groupby("descrpt").sum())["STATUS_APPROVE"]
        approval_rate = (dataset.groupby("descrpt").mean())["STATUS_APPROVE"]
        average_wage = (dataset.groupby("descrpt").mean())["PREVAILING_WAGE"]
    
    # create a new DataFrame and rename indexes
        industry_data = pd.concat([application_pool, approved_case, approval_rate,average_wage], axis =1)
        industry_data.columns.values[0] = "application_pool"
        industry_data.columns.values[1] = "approved_case"
        industry_data.columns.values[2] = "approval_rate"
        industry_data.columns.values[3] = "average_wage"
    
        return industry_data

    def industry_application_pool(self, industry_level, soc_name):
        return industry_level.newdf.ix[soc_name, "application_pool"]

    def industry_approved_case(self, industry_level, soc_name):
        return industry_level.newdf.ix[soc_name, "approved_case"]
    
    def industry_approval_rate(self, industry_level, soc_name):
        return industry_level.newdf.ix[soc_name, "approval_rate"]
    
    def industry_average_wage(self, industry_level, soc_name):
        return industry_level.newdf.ix[soc_name, "average_wage"]
    
    def occupation_rank(self, industry_level, n, indicator): 
        # rank top n occupations by indicator
        occupation_rank = industry_level.newdf.sort_values(by = indicator, ascending = False).ix[:n,indicator]
        df = industry_level.newdf.ix[occupation_rank.index, indicator]
        print('Top ' + str(n) + ' ' +indicator + ' occupation groups\n')
        print(df.to_string())
        return occupation_rank
    
'''
company level

'''

class company_level:
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.newdf = company_level.company(self, dataset)

    def company(self, dataset):
    # calculate required statistics
        application_pool = (dataset.groupby("EMPLOYER_NAME").count())["STATUS_APPROVE"]
        approved_case = (dataset.groupby("EMPLOYER_NAME").sum())["STATUS_APPROVE"]
        approval_rate = (dataset.groupby("EMPLOYER_NAME").mean())["STATUS_APPROVE"]
        average_wage = (dataset.groupby("EMPLOYER_NAME").mean())["PREVAILING_WAGE"]
    
    # create a new DataFrame and rename indexes
        company_data = pd.concat([application_pool, approved_case, approval_rate,average_wage], axis =1)
        company_data.columns.values[0] = "application_pool"
        company_data.columns.values[1] = "approved_case"
        company_data.columns.values[2] = "approval_rate"
        company_data.columns.values[3] = "average_wage"
    
        return company_data

    def company_application_pool(self, company_level, company_name):
        return company_level.newdf.ix[company_name, "application_pool"]

    def company_approved_case(self, company_level, company_name):
        return company_level.newdf.ix[company_name, "approved_case"]
    
    def company_approval_rate(self, company_level, company_name):
        return company_level.newdf.ix[company_name, "approval_rate"]
    
    def company_average_wage(self, company_level, company_name):
        return company_level.newdf.ix[company_name, "average_wage"]
    
    def company_rank(self, company_level, n, indicator): 
        # rank top n companies by indicator
        company_rank = company_level.newdf.sort_values(by = indicator, ascending = False).ix[:n,indicator]
        return company_rank    
    
