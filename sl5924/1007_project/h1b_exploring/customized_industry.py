'''
This module is designed for interactions in customized industry query
Users may input  a industry name they interested in
This module will match user's industry with industry name list in database, and confirm with user
They will get statistical information about application pools, approve rate, average Wage

Created on Nov 27, 2016

@author: Yovela
'''

import sys
import pandas as pd

from h1b_exploring.class_collections_ranking import industry_level
from h1b_exploring.exception_list import invalid_industry_name, wrong_int_exception


'''
industry_data = industry_level(merged_data)
customized_industry(industry_data)

'''
def identify_user_industry_list(user_input, industry_list):
    # return all similar industry names
    industry_keyword = user_input.capitalize()
    user_industry_list = []
    k = 0
    for i in range(len(industry_list)):
        if industry_keyword in industry_list[i]:
            user_industry_list.append(industry_list[i])
            print(k,industry_list[i])
            k += 1
    return user_industry_list
        
      
def confirm_user_industry(user_industry_list):
    # confirm interested industry with user
    try:
      
        if len(user_industry_list) == 1:
            user_industry = user_industry_list[0]
           
        if len(user_industry_list) > 1:
            user_choice = input("please choose an industry you interested in, enter the number before it\n")
            try:
                user_industry = user_industry_list[int(user_choice)]
            except:
                raise ValueError
            
    except ValueError:
        print('please follow input instructions ')
    except KeyboardInterrupt:
        sys.exit(1)
            
    return user_industry

def search_industry(industry_name, industry_data):
    # return statistical information
    print("The total application pool for " + industry_name + " is: ")
    print(industry_data.industry_application_pool(industry_data, industry_name))
    print("The total number of approved case for " + industry_name + " is: ")
    print(industry_data.industry_approved_case(industry_data, industry_name))
    print("The average approval rate for " + industry_name + " is: ")
    print(industry_data.industry_approval_rate(industry_data, industry_name))
    print("The average wage for " + industry_name + " is: ")
    print(industry_data.industry_average_wage(industry_data, industry_name))

    return
    
def job_title(industry_name, df):
    # print all related job titles
    job_title = df[df['descrpt'] == industry_name]['SOC_NAME'].drop_duplicates() 
    df = pd.DataFrame(job_title).dropna()
    print("All related job titles are listed below:")
    print(df.to_string())
    return 

def customized_industry(industry_data, merged_data):
    
    industry_list = industry_data.newdf.index.unique()

    while True:
        try:
            print ("================================ H1b Visa Approve Rate Exploring ================================")
            print ("") 
            print ("        Please Input Your Interested Industry Name, i.e: computer, business, engineering         ")
            print ("                   You may input return to go back to Industry menu                              ")
            print ("=================================================================================================")
            
            user_input = input('Please input here: ') 
            if user_input == 'return':
                break
            if user_input == 'quit':
                sys.exit(1)
            
            try:
                user_industry_list = identify_user_industry_list(user_input, industry_list)
                if len(user_industry_list) ==0:
                    raise invalid_industry_name
                else:
                    user_industry = confirm_user_industry(user_industry_list)
                    user_input = input(user_industry+ ": is it the industry you interested in? please yes or no\n")
                    if user_input == 'yes':
                        search_industry(user_industry, industry_data)
                        job_title(user_industry, merged_data)
                    else: 
                        raise invalid_industry_name
                        
            except invalid_industry_name:
                print ("Invalid industry name, please input again")

        
        except invalid_industry_name:
            print ("Invalid industry name, please input again")
        except KeyboardInterrupt:
            sys.exit(1)