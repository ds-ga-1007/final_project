import pandas as pd
from project import *
import os
datadir = 'C:/Users/Zhaopeng/1007/project/'
os.chdir(datadir)

'''
In this script, it takes original csv file and clean it without dropping any columns
1, It will convert all the salary in weekly/bi-weekly/monthly to year-based.
2, It will check the correctness of two city variables in the data set.
3, It will add a new variable "approval_status" with two values, 0 and 1
4, It will filter the data set by type of "Program" and "Part_time", we 
   will only include the h1b case and full time job case.
5, It will add a new variable "year"
6, Output the cleaned file to the directory
'''

for year in range(2010,2017):
    data = pd.read_csv('H-1B_FY'+str(year)+'_clean.csv',encoding = 'iso-8859-1')

    wage1 = "PREVAILING_WAGE"
    per1 = "PW_UNIT_OF_PAY"
    wage2 = "PREVAILING_WAGE"
    per2 = "PW_UNIT_OF_PAY"
    data = check_wage_1(data,wage1,per1, wage2, per2)

    city1 = "EMPLOYER_CITY"
    city2 = "EMPLOYER_CITY"
    data = check_city(data,city1,city2)

    status = "APPROVAL_STATUS"
    data = add_var(data, status, city1, city2)

    program = "PROGRAM"
    part = "PART_TIME_1"
    data = filter_visa_part(data,program, part)

    data["year"]=year
    data.to_csv('H-1B_FY'+str(year)+'_clean.csv', sep=',',encoding = "ISO-8859-1")