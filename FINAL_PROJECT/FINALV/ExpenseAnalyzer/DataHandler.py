# -*- coding: utf-8 -*-
"""
Created on Sat Dec 3 2016

@author: jub205/ak6201

@desc: This script contains data analyzer classes for yearly and state-wise analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore") #Pandas dataframe warning message for plots in some cases

class StateAnalyzer:
    '''This class is used for State level expense analysis.
       It contains methods that are used for different statistics analysis
       of a specific state given by a user and different form of visualization
       of analysis for the users
    '''
    
    def __init__(self, data, state='NY'):
        self.masterdata = data
        self.state = state
        self.filtered_data = data
        
    def set_state_data(self, state):
        '''Function to query masterdata based on state and sets it to filtered_data and sets state'''
        
        self.state = state
        self.filtered_data = self.masterdata[self.masterdata.can_off_sta == state]
        
    def get_state_list(self):
        '''Function returns a list of unique states in the data set'''
        
        states = list(self.masterdata.can_off_sta.unique())
        
        return states
        
    def print_state_list(self):
        '''Function prints out the list of states in a formatted way for users'''
        
        state_list = self.get_state_list()
        
        for i in range(0,len(state_list),10):
            states = state_list[i:i+10]
            print(" | ".join(states))
            
    def show_state_summary(self):
        '''Function displays simple statistics for a specific state in a yearly order'''
        
        years = self.filtered_data.ele_yea.unique()
        data = self.filtered_data.groupby(['ele_yea','can_nam']).dis_amo.sum()
        
        #Plot boxplot of expense by year
        for n, year in enumerate(years):
            plt.subplot(1, len(years), n+1)
            xdata = list(data[year].values)
            plt.boxplot(xdata)
            plt.ylabel("$")
            plt.title("Year %s"%str(year))
        print("Please close the figure to continue")
        plt.tight_layout()
        plt.show()
        plt.close('all')
               
    def show_expense_distribution(self):
        '''Function plots the distribution of expense for a given year'''
        
        years = self.filtered_data.ele_yea.unique()
        subplot_size = len(years)
        data = self.filtered_data.groupby(['ele_yea','can_nam']).dis_amo.sum()
        data = data/1000.0
        
        #Plot histogram for each year
        for n, year in enumerate(years):
            plt.subplot(subplot_size,1,n+1)
            xvalues = list(data[year].values)
            plt.hist(xvalues, bins=100)
            plt.xlabel('$ in thousand')
            plt.ylabel('Number of Candidates')
            plt.title("Distribution of expenditure across candidates for %s in year %s"%(self.state,str(year)))
        print("Please close the figure to continue") #Alert message for the user to close the plot to continue
        plt.tight_layout() #Plot formatting
        plt.show()
        plt.close("all")

    def show_monthly_expense(self):
        '''Function computes monthly expenditure and plots a line chart'''
        
        monthly = self.filtered_data.groupby(['ele_yea','month']).dis_amo.sum()
        years = self.filtered_data.ele_yea.unique()
        
        #Plot line chart for each year on a single plot
        for n, year in enumerate(years):
            plt.plot(monthly[year].index, monthly[year].values/1000000.0, label=str(year)) #Value in $ millions
            
        plt.xlabel("Month")
        plt.ylabel("Expense in  million $")
        plt.xlim((1,12))
        plt.title("Monthly expenditure in %s"%self.state)
        plt.legend(loc=2)
        plt.tight_layout()
        plt.show()
        plt.close("all")
        
    def show_winner_loser_comparison(self):
        '''Function to compare winner vs loser expense'''
        
        #Query data based on the result
        winners = self.filtered_data[self.filtered_data.RESULT == 'W'].groupby(['ele_yea']).dis_amo.sum()
        losers = self.filtered_data[self.filtered_data.RESULT == 'L'].groupby(['ele_yea']).dis_amo.sum()
        
        width = 0.35 #Bar width
        plt.bar(np.arange(len(winners.index)), winners.values, width, color = 'b', label='Winners') #Winner bar plot
        plt.bar(np.arange(len(losers.index))+width, losers.values, width, color = 'r', label='Losers') #Loser bar plot
            
        plt.xlabel('Year')
        plt.ylabel('$')
        plt.title('Yearly expense comparison by election result')
        plt.xticks(np.arange(0,len(winners.index))+width, losers.index)
        plt.legend(loc=2)
        print("Please close the figure to continue") #Alert message for the user to close the plot to continue
        plt.tight_layout()
        plt.show()
        plt.close('all')
                
class YearAnalyzer:
    '''This class is used for State level expense analysis.
       It contains methods that are used for different statistics analysis
       of a specific state given by a user and different form of visualization
       of analysis for the users
    '''
    
    def __init__(self, data, year=[2010]):
        self.masterdata = data
        self.year = year
        self.year.sort()
        self.filtered_data = data
        
    def set_year_data(self, year):
        '''Function to query data for given year from master data and set year and filtered_data'''
        
        self.year = year
        self.filtered_data = self.masterdata[self.masterdata.ele_yea.isin(year)]
                
    def show_year_summary(self):
        '''Function computes statistics and summary for given year'''

        number_of_can = len(self.filtered_data.can_nam.unique())
        expense_by_can = self.filtered_data.groupby('can_nam').dis_amo.sum().sort_values()
        
        #Compute stats for year summary
        total_expense = expense_by_can.sum()
        max_expense = expense_by_can[-1]
        min_expense = expense_by_can[0]
        avg_expense = expense_by_can.mean()
        med_expense = expense_by_can.median()
        std_dev_expense = expense_by_can.std()
        
        print("Total Number of candidates: %d"%number_of_can)
        print("Total Expense by all the candidates: %d"%total_expense)
        print("Maximum Expense: $ {0: .2f}".format(max_expense))
        print("Minimum Expense: $ {0: .2f}".format(min_expense))
        print("Average Expense: $ {0: .2f}".format(avg_expense))
        print("Median Expense: $ {0: .2f}".format(med_expense))
        print("Standard Deviation of expense: {0: .2f}".format(std_dev_expense))

    def show_expense_distribution(self):
        '''Function plots the distribution of expense for given year(s)'''
        
        subplot_size = len(self.year)
        data = self.filtered_data.groupby(['ele_yea','can_nam']).dis_amo.sum()
        data = data/1000.0 #Change unit to thousand $

        #Plot histogram of expense        
        for n, year in enumerate(self.year):
            plt.subplot(subplot_size,1,n+1)
            xvalues = list(data[year].values)
            plt.hist(xvalues, bins=100)
            plt.xlabel('$ in thousand')
            plt.ylabel('Number of Candidates')
            plt.title("Distribution of expenditure across candidates for %s"%str(year))
        print("Please close the figure to continue")
        plt.tight_layout()
        plt.show()
        plt.close("all")
        
    def show_expense_by_state(self):
        '''Function plots bar chart for expense by state'''
        
        data = self.filtered_data.groupby('can_off_sta').dis_amo.sum()
        data = data/1000.0  #Change unit to thousand $      
        plt.figure(figsize=(10,6))
        ind = np.arange(len(data.values))
        #Plotting bar chart
        plt.bar(ind, data.values, width=0.35, linewidth=1.5)
        plt.xticks(ind+0.35, data.index, rotation='vertical')
        plt.xlabel("State")
        plt.ylabel("$ in thousand")
        plt.title("Bar plot of total expenditure by state")
        print("Please close the figure to continue")   
        plt.tight_layout()
        plt.show()
        plt.close("all")
        
    def show_top_bottom_N(self, N=5):
        '''Function shows top and bottom N candidates by expense'''
        
        data = self.filtered_data.groupby('can_nam').dis_amo.sum().sort_values()
        topN = data[-N:]
        bottomN = data[:N]
        
        #Print Top/Bottom N candidates
        print("Top %d candidates by expenditure:"%N)
        print_series(topN)
        print("\n")
        print("Bottom %d candidates by expenditure:"%N)
        print_series(bottomN)
        
        #Plot bar chart for top and bottom spenders
        plt.figure(figsize=(10,6))
        #Subplot of top N spenders
        plt.subplot(1,2,1)
        plt.bar(np.arange(N),topN.values, 0.35, color = 'b', label='Top spenders')
        plt.xlabel('Candidates')
        plt.ylabel('$')
        plt.title('Top %s candidates by expenditure'%str(N))
        plt.xticks(np.arange(N)+0.35, topN.index, rotation='vertical')
        plt.legend(loc=2)
        #Subplot of bottom N spenders
        plt.subplot(1,2,2)
        plt.bar(np.arange(N),bottomN.values, 0.35, color = 'r', label='Bottom spenders')
        plt.xlabel('Candidates')
        plt.ylabel('$')
        plt.title('Bottom %s candidates by expenditure'%str(N))
        plt.xticks(np.arange(N)+0.35, bottomN.index, rotation='vertical')
        plt.legend(loc=2)
        print("Please close the figure to continue")  
        plt.tight_layout()
        plt.show()
        plt.close("all")

    def show_winner_vs_loser(self):
        '''Function shows statistics on winners and losers of the election'''
        
        winnersdata = self.filtered_data[self.filtered_data.RESULT == 'W']
        losersdata = self.filtered_data[self.filtered_data.RESULT == 'L']
        
        #Compute stats for winners and losers
        count_winners = len(winnersdata.can_nam.unique())
        count_losers = len(losersdata.can_nam.unique())
        total_winners = winnersdata.dis_amo.sum()
        total_losers = losersdata.dis_amo.sum()
        avg_exp_winners = winnersdata.dis_amo.sum() / count_winners
        avg_exp_losers = losersdata.dis_amo.sum() / count_losers
        med_exp_winners = winnersdata.groupby('can_nam').dis_amo.sum().median()
        med_exp_losers = losersdata.groupby('can_nam').dis_amo.sum().median()
        std_dev_exp_winners = winnersdata.groupby('can_nam').dis_amo.sum().std()
        std_dev_exp_losers = losersdata.groupby('can_nam').dis_amo.sum().std()
        
        print("Total Number of winners: %d"%count_winners)
        print("Total Number of losers: %d"%count_losers)
        print("Total Expense by winners: %d"%total_winners)
        print("Total Expense by losers: %d"%total_losers)
        print("Average Expense by winners: %.2f"%avg_exp_winners)
        print("Average Expense by losers: %.2f"%avg_exp_losers)
        print("Median Expense by winners: %.2f"%med_exp_winners)
        print("Median Expense by losers: %.2f"%med_exp_losers)
        print("Std. Deviation of Expense by winners: %.2f"%std_dev_exp_winners)
        print("Std. Deviation of Expense by losers: %.2f"%std_dev_exp_losers)
        
    def show_winner_vs_loser_bar(self):
        '''Function plots bar plot for winner vs loser comparison'''
        
        winners = self.filtered_data[self.filtered_data.RESULT == 'W'].groupby(['ele_yea']).dis_amo.sum()
        losers = self.filtered_data[self.filtered_data.RESULT == 'L'].groupby(['ele_yea']).dis_amo.sum()
        
        width = 0.35 #Bar width
        plt.bar(np.arange(len(winners.index)), winners.values, width, color = 'b', label='Winners') #Bar plot for winner
        plt.bar(np.arange(len(losers.index))+width, losers.values, width, color = 'r', label='Losers') #Bar plot for loser
            
        plt.xlabel('Year')
        plt.ylabel('$')
        plt.title('Yearly total expense comparison by election result')
        plt.xticks(np.arange(0,len(winners.index))+width, losers.index)
        plt.legend(loc=2)
        print("Please close the figure to continue") #Alert message for the user to close the plot to continue
        plt.tight_layout()
        plt.show()
        plt.close('all')
        
        
    def show_monthly_expense(self):
        '''Function computes monthly expenditure and plots a line chart'''
        
        monthly = self.filtered_data.groupby(['ele_yea','month']).dis_amo.sum()
        
        #Plot line chart for monthly expense
        for n, year in enumerate(self.year):
            plt.plot(monthly[year].index, monthly[year].values/1000000.0, label=str(year)) #Value in $ millions
            
        plt.xlabel("Month")
        plt.ylabel("Expense in  million $")
        plt.xlim((1,12))
        plt.title("Monthly expenditure in %s"%self.year)
        plt.legend(loc=2)
        plt.tight_layout()
        plt.show()
        plt.close("all")

def print_series(seriesdata):
    '''Function prints series data for index and value pair'''        
    for n,v in enumerate(seriesdata):
        print('{0: <20} $ {1: .2f}'.format(seriesdata.index[n],v))
