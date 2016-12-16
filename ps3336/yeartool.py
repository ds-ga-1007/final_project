'''
Created on Dec 11, 2016

@author: peimengsui
@desc: This class is defined for analysis based on time for year option
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class yeartool:
    '''
    This class includes methods for time based analysis
    '''

    def __init__(self,year,dataset):
        '''
        Constructor
        '''
        self.year = year
        self.dataset = dataset[dataset["year"]==year]
        self.dataset = self.dataset.drop(["matches","minutes","minutes_per_goal","handle"],axis=1)
        
    def income_age_dist(self,save):
        '''
        This function is used to plot incoming players' age distribution for different years
        '''
        data = self.dataset[self.dataset.transfer_status=="in"]
        fig = plt.figure()
        plt.hist(data["age"])
        plt.title("Transfer In Players' Age Distribution"+str(self.year))
        plt.xlabel("Age")
        plt.ylabel("count")
        print("close image to continue")
        if save=='y':
            fig.savefig('In_Age_Distribution_'+str(self.year)+'.pdf')
        plt.show()
        
    def out_age_dist(self,save):
        '''
        This function is used to plot outgoing players' age distribution for different years
        '''
        data = self.dataset[self.dataset.transfer_status=="out"]
        fig = plt.figure()
        plt.hist(data["age"])
        plt.title("Transfer Out Players' Age Distribution"+str(self.year))
        plt.xlabel("Age")
        plt.ylabel("count")
        print("close image to continue")
        if save=='y':
            fig.savefig('Out_Age_Distribution_'+str(self.year)+'.pdf')
        plt.show()
    
    def transfer_fee_amount(self,save):
        '''
        This function plot the total transfer fee amount by clubs
        '''
        data = self.dataset.groupby(["club","transfer_status"])["transfer_fee_pounds_int"].sum()
        N = len(data.index.get_level_values("club").unique())
        transfer_in = np.array(data[data.index.get_level_values('transfer_status') == 'in'])
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars
        
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, transfer_in, width, color='r')
        
        transfer_out = np.array(data[data.index.get_level_values('transfer_status') == 'out'])
        
        rects2 = ax.bar(ind + width, transfer_out, width, color='y')
        
        # add some text for labels, title and axes ticks
        ax.set_ylabel('Transfer Fee Amount')
        ax.set_title('Transfer Fee Amount by Club')
        ax.set_xticks(ind + width)
        
        ax.set_xticklabels(sorted([x[0:5] for x in set(data.index.get_level_values('club'))]),rotation=90)
        
        ax.legend((rects1[0], rects2[0]), ('In', 'Out'))
        if save=='y':
            fig.savefig('Transfer_Fee_Amount_'+str(self.year)+'.pdf')
        plt.show()
        
    def position_table(self):
        '''
        This function print a table of number of transfered in and out different positions for clubs
        '''
        pd.set_option('display.max_rows', 1000)
        print (self.dataset.groupby(["club","transfer_status","position"]).size())
    
    def investment_return(self,save):
        '''
        This function print a table of calculated investment return for each club
        '''
        data = self.dataset[self.dataset["transfer_status"]=="in"]
        group = data.groupby("club")["transfer_fee_pounds_int","goals","assists"].sum()
        group["pounds_per_goal"] = group["transfer_fee_pounds_int"]/group["goals"]
        group["pounds_per_assist"] = group["transfer_fee_pounds_int"]/group["assists"]
        group["pounds_per_goal"].plot(kind="barh")
        plt.title("Pounds Spent per Goal "+str(self.year))
        print("close image to continue")
        if save=='y':
            plt.savefig('pounds_per_goal_'+str(self.year)+'.pdf')
        plt.show()
        group["pounds_per_assist"].plot(kind="barh")
        plt.title("Pounds Spent per Assist "+str(self.year))
        print("close image to continue")
        if save=='y':
            plt.savefig('pounds_per_assist_'+str(self.year)+'.pdf')
        plt.show()
        