'''
This module is designed for interactions in customized company query
Users may input  a company name they interested in
This module will match user's company with company name list in database, and confirm with user
They will get statistical information about application pools, approve rate, average Wage

Created on Nov 27, 2016

@author: Yovela
'''
import sys
import pandas as pd
import matplotlib.pyplot as plt

from h1b_exploring.class_collections_ranking import company_level
from h1b_exploring.exception_list import invalid_company_name

def identify_company_name(user_company, company_name_list):
    # generate a list contains all matching company names
        user_company_list = []
        for i in range(len(company_name_list)):
            if user_company in company_name_list[i]:
                user_company_list.append(company_name_list[i])
        
        return user_company_list
    


def search_company(company_data, company_name_list):
        # return statistical information
        df = company_data.newdf.ix[company_name_list]
        print(df.to_string())
        print("The total number of application pool is", df["application_pool"].sum())
        print("The total number of approved case is", df["approved_case"].sum())
        print("The approval rate is", df["approved_case"].sum()/df["application_pool"].sum())
        print("The average wage for this company is",df["average_wage"].sum()/len(df))  
        return
    
def customized_company(company_data):
    
    company_name_list = company_data.newdf.index.unique()
    
    while True:
        try:
            print ("================================ H1b Visa Approve Rate Exploring ================================")
            print ("")
            print ("                          Please Input Your Interested Company Name                              ")
            print ("                    You may input RETURN to go back to previous dictionary                       ")
            print ("")
            print ("=================================================================================================")
            user_input = input("Please input here:")
            
            if user_input == "quit":
                sys.exit(1)
            if user_input.upper() == 'RETURN':
                break
            
            # matching user's inputting name with company name list
            user_input = user_input.upper()
            user_company_list = identify_company_name(user_input, company_name_list)
            
            
            # confirm user's interested company                
            try:
                
                if len(user_company_list)<=20 and len(user_company_list) >0:
                    for user_company in user_company_list:
                        print(user_company)
                elif len(user_company_list)>20:
                    print("can't accurately locate your interested company, please try to enter the full name\n")
                    raise invalid_company_name
                elif len(user_company_list) == 0:
                    print("can't find your interested company, please re-enter a name\n")
                    raise invalid_company_name
                
                
            # return statistical results
                user_answer = input("if there are companies you interested in, please enter yes; otherwise, enter no\n")
            
                if user_answer == 'yes':
                     search_company(company_data, user_company_list)
                else:
                    raise invalid_company_name
            
            except invalid_company_name:
                pass
            except KeyboardInterrupt:
                sys.exit(1)
            

            
        except invalid_company_name:
            print ("Invalid company name, please input again")
        except KeyboardInterrupt:
            sys.exit(1)

   
    