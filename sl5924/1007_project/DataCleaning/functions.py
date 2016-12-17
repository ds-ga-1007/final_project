import pandas as pd
import numpy as py

'''
this script contains all the functions that will be used for data cleaning
'''
## drop columns
def drop_col(data,name):
    data = data.drop(name,axis=1 )
    return data

## filter the data on city name
def check_city(data,city1,city2):
    data[city1].fillna("blank", inplace=True)
    data[city2].fillna("blank", inplace=True)
    data[city1]=data[city1].str.upper()
    data[city2]=data[city2].str.upper()
    data = data[~data[city1].str.contains("STREET|blank")]
    data = data[~data[city1].str.contains("0|1|2|3|4|5|6|7|8|9")]
    data = data[~data[city2].str.contains("STREET")]
    data = data[~data[city2].str.contains("0|1|2|3|4|5|6|7|8|9")]
    return data

##  filter the data on wage1 range and wage2
def check_wage_2(data,wage1_lo,wage1_hi,per1, wage2, per2):
    data[per1].fillna("blank", inplace=True)
    data[per2].fillna("blank", inplace=True)
    data = data[~data[per1].str.contains("Hour|blank|hr|HR")]
    data = data[~data[per2].str.contains("Hour|hr|HR")]
    data[wage1_lo][data[per1].str.contains("m|M")] = data[wage1_lo][data[per1].str.contains("m|M")]*12
    data[wage1_lo][data[per1].str.contains("WK|We")] = data[wage1_lo][data[per1].str.contains("m|M")]*26
    data[wage1_lo][data[per1].str.contains("B|b")] = data[wage1_lo][data[per1].str.contains("m|M")]*52
    data[wage1_hi][data[per1].str.contains("m|M")] = data[wage1_hi][data[per1].str.contains("m|M")]*12
    data[wage1_hi][data[per1].str.contains("WK|We")] = data[wage1_hi][data[per1].str.contains("m|M")]*26
    data[wage1_hi][data[per1].str.contains("B|b")] = data[wage1_hi][data[per1].str.contains("m|M")]*52
    
    data[wage2][data[per2].str.contains("m|M")] = data[wage2][data[per2].str.contains("m|M")]*12
    data[wage2][data[per2].str.contains("WK|Week")] = data[wage2][data[per2].str.contains("m|M")]*26
    data[wage2][data[per2].str.contains("B|b")] = data[wage2][data[per2].str.contains("m|M")]*52
    data[per1]='yr'
    data[per2]='yr'
    return data

##  filter the data on wage1,2
def check_wage_1(data,wage1,per1, wage2, per2):
    data[per1].fillna("blank", inplace=True)
    data[per2].fillna("blank", inplace=True)
    data = data[~data[per1].str.contains("Hour|blank|hr|HR")]
    data = data[~data[per2].str.contains("Hour|hr|HR")]
    data = data[data[wage2]>50]
    data[wage1][data[per1].str.contains("m|M")] = data[wage1][data[per1].str.contains("m|M")]*12
    data[wage1][data[per1].str.contains("WK|Week")] = data[wage1][data[per1].str.contains("m|M")]*26
    data[wage1][data[per1].str.contains("B|b")] = data[wage1][data[per1].str.contains("m|M")]*52
    data[wage2][data[per2].str.contains("m|M")] = data[wage2][data[per2].str.contains("m|M")]*12
    data[wage2][data[per2].str.contains("WK|Week")] = data[wage2][data[per2].str.contains("m|M")]*26
    data[wage2][data[per2].str.contains("B|b")] = data[wage2][data[per2].str.contains("m|M")]*52
    data[per1]='yr'
    data[per2]='yr'
    return data

##  add two new variables called STATUS_APPROVE and RELOCATE
def add_var(data, status, city1, city2):
    #new variable Status_APPROVE
    data['STATUS_APPROVE']= (data[status]=='CERTIFIED').astype(int)
    #LCA_CASE_EMPLOYER_CITY == LCA_CASE_WORKLOC1_CITY
    data['RELOCATE'] = (data[city1] == data[city2]).astype(int)
    return data
    
##  filter the data on fulltime
def filter_visa_full(data,program, full):
    data = data[data[program].str.contains("H-1B|R")]
    data = data[data[full]=="Y"]
    return data
##  filter the data on parttime
def filter_visa_part(data,program, part):
    data = data[data.PROGRAM.str.contains("H-1B|R")]
    data = data[data[part]=="N"]
    return data

## convert a variable to uppercase
def to_upper(data, variable):
    data.variable = data.variable.str.upper()
    
## convert int variable to float variable
def to_float(data, variable):
    data.variable.replace(',','')
    data.variable = data.variable.astype(float)
    data.round({variable: 2})
