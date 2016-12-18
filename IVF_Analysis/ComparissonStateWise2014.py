# -*- coding: utf-8 -*-

''' Module with several usefull functions to compute the comparisson statewise in 2014'''

import pandas as pd
import numpy as np
import UserProfile as up
import PrintFunctions as pt
import pylab
import matplotlib.pyplot as plt


dict = {'FshDnrEmbryosRate':       'Avg # of embryos transferred  ',
    'FshDnrLvBirths_TransRate':  'Live births per 100 transfers ',
    'FshDnrTotCycles':           'Number of cycles              ',
    'FshDnrTransPregRate':       'Pregnancies per 100 transfers ',
    'FshDnrTransfers':           'Number of transfers           ',
    'FshNDCansRate':             'Cancellations per 100 cycles  ',
    'FshNDCycle':                'Number of cycles              ',
    'FshNDEmbryosRate':          'Avg # of embryos transferred  ',
    'FshNDLvBirthsRate':         'Live births per 100 cycles    ',
    'FshNDLvBirths_TransRate':   'Live births per 100 transfers ',
    'FshNDPregRate':             'Pregnancies per 100 cycles    ',
    'FshNDTransPregRate':        'Pregnancies per 100 transfers ',
    'FshNDTransfers':            'Number of transfers           ',
    'ThwDnrEmbryosRate':         'Avg # of embryos transferred  ',
    'ThwDnrLvBirths_TransRate':  'Live births per 100 transfers ',
    'ThwDnrTotCycles':           'Number of cycles              ',
    'ThwDnrTransPregRate':       'Pregnancies  per 100 transfers',
    'ThwDnrTransfers':           'Number of transfers           ',
    'ThwNDEmbryosRate':          'Avg # of embryos transferred  ',
    'ThwNDLvBirths_TransRate':   'Live births per 100 transfers ',
    'ThwNDTotCycles':            'Number of cycles              ',
    'ThwNDTransPregRate':        'Pregnancies per 100 transfers ',
    'ThwNDTransfers':            'Number of transfers           ' }

def embryo_cat_variables(ob):  
    
    ''' Function that accepts the user class (UserProfile) and generates list of variables to be plotted for categories of the user'''
    
    if ob.categorizer()[0] == 1: 
        embryo_cat_variables = pd.Series(['FshNDCycle', 'FshNDCansRate', 'FshNDEmbryosRate', 'FshNDLvBirthsRate', 
                   'FshNDPregRate', 'FshNDTransfers', 'FshNDLvBirths_TransRate','FshNDTransPregRate'])

    elif ob.categorizer()[0] == 2: 
        embryo_cat_variables = pd.Series(['ThwNDTotCycles', 'ThwNDEmbryosRate', 'ThwNDTransfers', 'ThwNDLvBirths_TransRate',
                  'ThwNDTransPregRate'])

    elif ob.categorizer()[0] == 3: 
        embryo_cat_variables = pd.Series(['FshDnrTotCycles', 'FshDnrEmbryosRate', 'FshDnrTransfers',
                    'FshDnrLvBirths_TransRate', 'FshDnrTransPregRate'])

    elif ob.categorizer()[0] == 4: 
        embryo_cat_variables= pd.Series(['ThwDnrTotCycles', 'ThwDnrEmbryosRate', 'ThwDnrTransfers', 
                    'ThwDnrLvBirths_TransRate', 'ThwDnrTransPregRate'])
    return embryo_cat_variables

# Change state_of_clinic_of_interest to state and pass it as a function argument. 

# PAss clinic_name=   state = 
# yearData --> data2014

def other_clinics_set(clinic_name, state, yearData):
    intermediate = yearData[yearData.ClinStateCode==state]
    other_clinics = pd.DataFrame(intermediate[intermediate.PrevClinName1 !=clinic_name])
    return other_clinics

def clinic_stats_own_eggs(clinic_name, state, yearData, ob):
    
    ''' Generate a clinic table when user is using her own eggs '''
    
    print()
    print("CLINIC OF INTEREST: ", clinic_name.lower().title())
    print("STATE:              ", state)
    print("CATEGORY:           ", ob.categorizer()[1])
    print("AGE:                ", ob.age_grouper()[1].title())
    print()
    print("COMPARISON OF YOUR CLINIC WITH OTHER CLINICS IN " + state.upper() + ":")
    print()
    
    age = ob.age_grouper()[0]
    temp_table = []
    for i in embryo_cat_variables(ob):
        var_clinic_of_interest = yearData['{var}{age}'.format(var=i,age=age)][yearData.PrevClinName1 == clinic_name].values[0]
        var_clinic_nearby = np.array(other_clinics_set(clinic_name, state, yearData)['{var}{age}'.format(var=i,age=age)].dropna())
        var_clinic_nearby_mean = np.mean(var_clinic_nearby.astype(float))
        var_clinic_nearby_median = np.median(var_clinic_nearby.astype(float))
        temp_table.append([dict[i], float(("{0:.2f}".format(var_clinic_of_interest))), 
                           float(("{0:.2f}".format(var_clinic_nearby_mean))),
                          float(("{0:.2f}".format(var_clinic_nearby_median)))])
    
    temp_table.append(["Number of clinics", 1, int(len(other_clinics_set(clinic_name, state, yearData))),int(len(other_clinics_set(clinic_name, state, yearData)))])
    table = pd.DataFrame(temp_table, columns = ['VARIABLES                   ','YOUR CHOICE',
                                                'AVERAGE OTHERS', 'MEDIAN OTHERS'])
    print(table)
    return table

def clinic_stats_donor_eggs(clinic_name, state, yearData, ob):
    
    ''' Generate a clinic table when user is using donated eggs '''
    
    print()
    print("CLINIC OF INTEREST: ", clinic_name.lower().title())
    print("STATE:              ", state)
    print("CATEGORY:           ", ob.categorizer()[1])
    print("Statistics are not age-specific when using donor eggs")
    print()
    print("COMPARISON OF YOUR CLINIC WITH OTHER CLINICS IN " + state.upper() + ":")
    print()
    
    temp_table = []
    for i in embryo_cat_variables(ob):
        var_clinic_of_interest = yearData['{var}'.format(var=i)][yearData.PrevClinName1 == clinic_name].values[0]
        var_clinic_nearby = np.array(other_clinics_set(clinic_name, state, yearData)['{var}'.format(var=i)].dropna())
        var_clinic_nearby_mean = np.mean(var_clinic_nearby.astype(float))
        var_clinic_nearby_median = np.median(var_clinic_nearby.astype(float))
        temp_table.append([dict[i], float(("{0:.2f}".format(var_clinic_of_interest))), 
                           float(("{0:.2f}".format(var_clinic_nearby_mean))),
                          float(("{0:.2f}".format(var_clinic_nearby_median)))])
    
    temp_table.append(["Number of clinics", 1, int(len(other_clinics_set(clinic_name, state, yearData))),int(len(other_clinics_set(clinic_name, state, yearData)))])
    table = pd.DataFrame(temp_table, columns = ['VARIABLES                   ','YOUR CHOICE',
                                                'AVERAGE OTHERS', 'MEDIAN OTHERS'])
    print(table)
    return table

def generateStateTable(clinic_name, state, yearData, ob):
    
    ''' Selector to know what table to use, according to user '''
    
    if ob.categorizer()[0] == 1 or ob.categorizer()[0] == 2:   #FshND, 'ThwND'
        return clinic_stats_own_eggs(clinic_name, state, yearData, ob)

    elif ob.categorizer()[0] == 3 or ob.categorizer()[0] == 4:    #'FshDn','ThwDn'
        return clinic_stats_donor_eggs(clinic_name, state, yearData, ob)

def clinics_to_plot(clinic_name, var_to_plot, dataInput, ob):

    clinics_to_plot = dataInput[dataInput.ClinStateCode==ob.state][[var_to_plot, 'PrevClinName1']]     
    clinics_to_plot['color']=0
    clinics_to_plot.loc[clinics_to_plot.PrevClinName1==clinic_name,'color']=1
    clinics_to_plot =clinics_to_plot.set_index(['PrevClinName1'])
    return clinics_to_plot

def plot(plot_input, ob):
    if plot_input == 1:
        var_to_plot = ob.total_cycles_plot()
        title = "Number of Cycles"
        
    elif plot_input ==2:
        var_to_plot = ob.live_births_transfer_plot()
        title = "Live Births per 100 Transfers"
        
    return var_to_plot, title

def barh_chart(clinic_name, dataInput, ob, plot_input):

        
    var_to_plot = plot(plot_input, ob)[0]
    data = clinics_to_plot(clinic_name, var_to_plot, dataInput, ob).sort_values([var_to_plot],ascending=[True])
    if ob.categorizer()[0] == 1 or ob.categorizer()[0] == 2:
        Title = "Ranking of Clinics in " + ob.state + " by " + plot(plot_input, ob)[1] + " \n Ages " + ob.age_grouper()[1] + "\n"
    elif ob.categorizer()[0] == 3 or ob.categorizer()[0] == 4:
        Title = "Ranking of Clinics in " + ob.state + " by " + plot(plot_input, ob)[1] + " \n (donor egg => not age-specific) \n"

    ax = data[var_to_plot].dropna().plot.barh(title = Title, width = 1.2, color = data['color'].map({1:'r', 0: 'b'}), figsize = (12, 8), fontsize = 6)

    ax.set_xlabel(plot(plot_input, ob)[1])
    ax.set_ylabel("Clinics")
    ax.xaxis.set_ticks_position('top')
    pylab.show()




