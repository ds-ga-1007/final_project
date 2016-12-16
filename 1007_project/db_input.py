'''
Created on  Dec 5th 2016
@Project Name:World bank data explorer
@Author:Liwei Song, Zoe Ma, Yichao Chen
'''
from class_function import *
import sys

'''
This module contains the database input function
Database secures all the tables and we hope to use db to conduct files storage and data query in the future.
'''

def database_builder():
    while True:
        try:
            #ask user to install worldbank database or not
            enter_value=input('Do you want to install the worldbank.db? Enter Y for yes, N for No.\nor Enter Q to exit the system: \n')
            all_database=glob.glob( '*.db')
            if enter_value not in ('Y','N','Q'):
                print('Invalid Input\n')
            elif enter_value.upper()=='Y':
                #if db exist, then print unable to install information
                if 'worldbank.db' in all_database:
                    print ('worldbank.db already exists.\n')
                else:
                    #if not , install the db.
                    x=db_build('worldbank')
                    x.define_files()
                    x.form_db()
                    break
            elif enter_value.upper()=='N':
                break
            elif enter_value.upper()=='Q':
                sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)
        except EOFError:
            sys.exit(1)
            
  