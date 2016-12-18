# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pylab as plt

def mean_finder(provideData, user):
    
    '''Accepts a user from the identifier class (UserProfile)  and  returns means of the same applicant for live births accross years'''
    
    means = []
    early_years = list(range(2007,2011))
    late_years = list(range(2011, 2015))
    main_var1 = user.main_variable_early()
    main_var2 = user.main_variable_late()
    
    for year in early_years:
        year_data = provideData[year]
        temp  = year_data[main_var1]
        means.append(temp.astype(float).mean())

    for year in late_years:
        year_data = provideData[year]
        temp  = year_data[main_var2]
        means.append(temp.astype(float).mean())

    means = pd.Series(means, name = user.categorizer()[1]+ ' ' + user.age_grouper()[1] )
    return means


def clinic_finder(clinic_name, user, provideData):
    early_years = list(range(2007,2011)) 
    late_years = list(range(2011, 2015))
    main_var1 = user.main_variable_early()
    main_var2 = user.main_variable_late()
    clinic_data = []
    for year in early_years:
        year_data = provideData[year]
        temp_row = year_data.loc[year_data['PrevClinName1'] == clinic_name]
        if temp_row.shape[0] == 0:
            clinic_data.append(np.nan)
        
        elif temp_row.shape[0] == 1:
            clinic_data.append(temp_row[main_var1])
        
        else: 
            temp_row = temp_row.loc[temp_row['ClinStateCode'] == user.state]
            clinic_data.append(temp_row[main_var1])
            
    for year in late_years:
        year_data = provideData[year]
        temp_row = year_data.loc[year_data['PrevClinName1'] == clinic_name]
        
        if temp_row.shape[0] == 0:
            clinic_data.append(np.nan)
        elif temp_row.shape[0] == 1:
            clinic_data.append(temp_row[main_var2])
            
        else: 
            temp_row = temp_row.loc[temp_row['ClinStateCode'] == user.state]
            clinic_data.append(temp_row[main_var2])
            
            
    clinic_data = pd.Series(clinic_data, name = user.categorizer()[1]+ ' ' + user.age_grouper()[1] )
    return clinic_data


def plotter(chosen_clinic_name, user, provideData): 
    fig = plt.figure(figsize= (16,10))
    fig.subplots_adjust(bottom=0.15)

    plt.ylabel('Average live births per 100', fontsize = 20)
    plt.xlabel('Time', fontsize = 20)
    plt.title('Average live birth over time for ' + mean_finder(provideData, user).name, fontsize = 20)
    plt.plot(mean_finder(provideData, user), 'o-', linewidth  = 4, label = 'national average', markersize = 10, color = 'pink')
    plt.xlim(-1,mean_finder(provideData, user).size)
    plt.ylim(-5,105)
    plt.xticks(range(mean_finder(provideData, user).size), list(map(str,range(2007, 2015))), fontsize = 15 )
    plt.yticks(fontsize = 15)
    plt.plot([mean_finder(provideData, user).size-1],clinic_finder(chosen_clinic_name, user, provideData).iloc[-1], '*', markersize= 30, 
             color ='yellow', label='_nolegend_' )
    plt.annotate('Latest data for ' + chosen_clinic_name, 
                 xy= (mean_finder(provideData, user).size-1, clinic_finder(chosen_clinic_name, user, provideData).iloc[-1]), 
                 xytext=(mean_finder(provideData, user).size-4, clinic_finder(chosen_clinic_name, user, provideData).iloc[-1]+10), 
                 arrowprops=dict(facecolor=[0,.4,.7], shrink=0.05, width = 1, headwidth = 5),color= [0,.4,.7])
    plt.plot(clinic_finder(chosen_clinic_name, user, provideData), 'o-', color= [0,.4,.7], 
             label = chosen_clinic_name) 
    plt.legend(loc = 2)
    if pd.isnull(clinic_finder(chosen_clinic_name, user, provideData)).any() :
        fig.text(0.03,.05,'Information about '+ chosen_clinic_name + ' is missing for some years', color =[0,.4,.7] , fontsize = 15 )
    plt.show()