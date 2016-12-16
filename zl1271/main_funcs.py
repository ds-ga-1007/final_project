'''
Created on Dec 13, 2016

@author: felix
'''
import matplotlib.pyplot as plt
import re
import pandas as pd
from Data import Data
from Correlation import Correlation
from instructions import *

    
def rm_ws(string):
    # remove white spaces
    new_str = re.sub(r'\s+', '', string)
    return new_str
    
def clean_str(string):
    string = rm_ws(string)
    string = string.lower()
    return string

def valid_input(string, valid_input_list):
    string = clean_str(string)
    return string in valid_input_list

def get_valid_user_input(valid_input_list = ['all', 'quit', 'explore']):
    user_input_str = ''
    while not valid_input(user_input_str, valid_input_list):
        user_input_str = input('Please enter a valid input.\n')
    return clean_str(user_input_str)

def get_categories(df, variable_name):
    return list(pd.unique(df[variable_name].values))

def get_data_by_category(df, variable_name, category):
    # get the data of a certain category out of a df
    return df[(df[variable_name]==category)]

def run_all_model():
    mydata = Data()
    mod1_data = mydata.data_clean[:] 
    mod1 = Correlation(mod1_data)
    mod1.save_summary()
    
def run_explore():
    while True:
        try:
            explore_instructions()
            user_input_str = get_valid_user_input(['describe','regression','quit'])
    
            if user_input_str == 'describe':
                run_describe()
            elif user_input_str == 'quit':
                pass
            elif user_input_str == 'regression':
                run_regression()
            else:
                raise Exception
            break
        
        except KeyboardInterrupt:
            break
        except:
            print('Unexpected input')
            pass
        
def run_describe():
    while True:
        try:
            describe_instructions()
            user_input_str = get_valid_user_input(['all','sex','race','age','educ','quit'])
            
            mydata = Data()
            mydata.rename_columns()
            
            def plot_by_category(cat_header, cont_hearder = 'income', plot_data = mydata.data):
                # plot boxpolots of a continuous variable by a categorical one
                plot_data.boxplot(column = cont_hearder, by = cat_header)
                
                if cat_header is None:
                    figure_name = './Results/Plots/' + 'Boxplots of ' + cont_hearder.capitalize() + '.pdf'
                else:
                    figure_name = './Results/Plots/' + 'Boxplots of ' + cont_hearder.capitalize() + ' by ' + cat_header.capitalize() + '.pdf'
                plt.savefig(figure_name)
                print('Plot saved')
                plt.show()
                plt.close()
            
            if user_input_str == 'quit':
                pass
            elif user_input_str == 'all':
                plot_by_category(None)
            else:
                plot_by_category(user_input_str)
            break
        
        except KeyboardInterrupt:
            break
        except:
            print('Unexpected input')
            pass
        
def select_predictor(list_of_predictors = ['sex','race','age','educ']):
    while True:
        try:
            selec_predictor_instructions()
            user_input_str = get_valid_user_input(['sex','race','age','educ','quit'])
            return user_input_str
        
        except KeyboardInterrupt:
            break
        except:
            print('Unexpected input')
            pass

def get_a_category(cat_list):
    temp_str = ''
    for a_str in cat_list:
        temp_str = temp_str + ', \'' + a_str + '\''
    prompt_str = 'Choose a category from the following: ' + temp_str[1:]
    regression_instructions3(prompt_str)
    cat_list.append('quit')
    user_input_str = get_valid_user_input(cat_list)
    return user_input_str
    

def run_regression():
    while True:
        try:
            regression_instructions1()
            user_input_str = get_valid_user_input(['all','part','quit'])
            
            if user_input_str == 'quit':
                pass
            elif user_input_str == 'part':
                regression_instructions2()
                user_input_str = get_valid_user_input(['sex','race','quit'])
                
                if user_input_str == 'quit':
                    pass
                else:
                    var_name = user_input_str
                    mydata = Data()
                   
                    cat_list = get_categories(mydata.data_clean, var_name)

                    category_choice = get_a_category(cat_list)

                    if category_choice == 'quit':
                        pass
                    else:
                        mod_data = get_data_by_category(mydata.data_clean,var_name,category_choice)
                        new_outcome_name = 'conrinc_' + category_choice
                        mod_data.rename(columns={'conrinc': new_outcome_name}, inplace=True)
                    
                        mod = Correlation(mod_data)
                        mod.save_summary()
                    

                
            else:
                predictor = select_predictor()
                
                if predictor == 'quit':
                    pass
                else:
                    df_list = ['conrinc']
                    df_list.append(predictor)
                    mydata = Data()
                    mod1_data = mydata.data_clean[df_list] 
                    mod1 = Correlation(mod1_data)
                    mod1.save_summary()
                    
                    # for continuous variables, show plot
                    if predictor in ['age','educ']:
                        mod1.plot_regression()
            
            break        
        
        
        except KeyboardInterrupt:
            break
        except:
            print('Unexpected input')
            pass





