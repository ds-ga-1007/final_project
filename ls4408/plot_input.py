'''
Created on  Dec 10th 2016
@Project Name:World bank data explorer
@Author:Liwei Song, Zoe Ma, Yichao Chen
'''

from plot import *
from class_function import *
import sys
from plotly import *
import matplotlib.pyplot as plt

'''
This module is plot_input function. It asks users to enter a plot type and return the plot.
'''

def plot_input(year,feature,country):
    a=1
    size=len(feature)
    feature_plot_list=[]
    for item in range(size):
        feature_df= pd.read_csv('./data/alldata/'+feature[item]+'.csv').drop('Unnamed: 0',axis=1)
        #read in all the user-required features csv files and convert them to dataframe
        feature_df = feature_df.set_index(feature_df['Year']).drop(['Year'],axis=1)
        feature_plot_list.append(plot(feature_df,country,year))
        #use plot class for all the dataframes and combine all the plot objects into a list
    try:
        while(a==1):
            print('you could choose plot types below:')
            print('1,time_series_plot 2,barplot\n3,scatter_plot 4,histogram\n5,boxplot_year 6,boxplot_country\n7,heatmap 8,choropleth\n9,pie_plot\nEnter Q to quit and Enter R to return to previous menu')
            plot_type = input('Please select a plot type')
            if plot_type.isdigit():
                option=int(plot_type)
            elif plot_type=='Q':
                sys.exit(1)
            elif plot_type=='R':
                a=0
                break
            else:
                raise InputError
            #choose different plots
            if option==1:
                for dplot in feature_plot_list:
                    dplot.time_series_plot()
            if option==2:
                for dplot in feature_plot_list:
                    dplot.bar_plot()
            if option==3:
                for dplot in feature_plot_list:
                    dplot.scatter_plot()
            if option==4:
                for dplot in feature_plot_list:
                    dplot.histogram()
            if option==5:
                for dplot in feature_plot_list:
                    dplot.boxplot_year()
            if option==6:
                for dplot in feature_plot_list:
                    dplot.boxplot_country()
            if option==7:
                for dplot in feature_plot_list:
                    dplot.heatmap()
            if option==8:
                for dplot in feature_plot_list:
                    dplot.choropleth()
            if option==9:
                for dplot in feature_plot_list:
                    dplot.pie_chart()
            #for different option, the system return different type of plot
    except InputError:
        print('Invalid input option')
    except KeyboardInterrupt:
        sys.exit(1)
    except EOFError:
        sys.exit(1)
    return a
