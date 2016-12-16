'''
This is module which designed for interactions in city level
This function will automatically return a list of Top 20 Cities ranked by application pool
A pdf file contained graphs of application pools, approve rate, average wage will be automatically saved


Created on Nov 27, 2016

@author: Yovela
'''
import sys
import pandas as pd
import matplotlib.pyplot as plt
from h1b_exploring.class_collections_ranking import *
from matplotlib.backends.backend_pdf import PdfPages



def city_exploring(data):
    print("loading data....")
    merged_data = pd.concat([data[year] for year in range(2010,2017)], ignore_index= True)
    city_data = city_level(merged_data)
    
    # rank cities with "application pool" and create a new variable called "approved case"
    city_rank = city_data.newdf.sort_values(by = "application_pool", ascending = False).ix[:20]
    city_rank["unapproved_case"] = city_rank["application_pool"]-city_rank["approved_case"]

    # print rank 
    df = city_rank.ix[:,["application_pool", "approval_rate", "average_wage"]]
    print("The top 20 cities with largest application pools from 2010 to 2016 is ranked below: \n")
    print(df.to_string())
    
    # save PDF file
    with PdfPages('city_exploring.pdf') as pdf:
        
        plt.figure(figsize = (30,20))
        city_rank_by_application_pool = city_rank["approved_case"].sort_values(inplace=False, ascending=True)
        ax1 = city_rank_by_application_pool.plot(kind = "barh", alpha = 0.7, color = ["skyblue", "pink","green"], 
                                       figsize = (20,15))
        ax1.set_title("Top 20 Largest Application Pool Cities",fontsize = "large")
        pdf.savefig()
        plt.close()
        
        plt.figure(figsize = (30,20))
        ax2 = city_rank[["approved_case", "unapproved_case"]].plot(kind = "bar", alpha = 0.7, stacked = True,color = ["skyblue", "pink"], 
                                       figsize = (20,15), title = "Approval Rate for Top 20 Largest Application Pool Cities")
        ax3 = city_rank["approval_rate"].plot(kind = "line", secondary_y=True,  style = 'ko--' )
        ax2.set_xticklabels(city_rank.index,rotation=45)
        ax3.set_xticklabels(city_rank.index,rotation=45)
        pdf.savefig()
        plt.close()
        

        plt.figure(figsize = (30,20))
        ax4 = city_rank["average_wage"].plot(kind = "barh", ylim = [40000,120000], color = "skyblue",figsize = (20,15),
                                             title = "Average Wage for Top 20 Largest Application Pool Cities" )
        pdf.savefig()
        plt.close()
        
        print("Further analysis has been saved in your local folder as PDF, please open your folder to check")
        

    print("please return to the previous dictionary to explore other functions\n") 

    return

if __name__ == '__main__':
    data = {}
    for year in range(2010,2017):
        data[year]= pd.read_csv('/Users/yuweitu/Documents/Programming/DSGA1007_Project/DataBase/H-1B_FY'+str(year)+'_clean.csv',encoding = 'iso-8859-1')
    city_exploring(data)
