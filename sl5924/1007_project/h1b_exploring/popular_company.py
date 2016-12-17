'''

This is module which designed for interactions in company level
This function will automatically return a list of Top 10 Companies ranked by application pool
A pdf file contained graphs of application pools, approve rate, average wage will be automatically saved

Created on Nov 27, 2016

@author: Yovela
'''
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

'''
company_data = company_level(merged_data)
popular_company(company_data) 
'''


def popular_company(data):
    
    company_rank = data.newdf.sort_values(by = "application_pool", ascending = False).ix[:10]
    
    company_rank["unapproved_case"] = company_rank["application_pool"]-company_rank["approved_case"]
    
    df = company_rank.ix[:,["application_pool", "approval_rate", "average_wage"]]
    print("The top 10 companies with largest application pools from 2010 to 2016 is ranked below: \n")
    print(df.to_string())
    
    with PdfPages('popular_company.pdf') as pdf:
        plt.figure(figsize = (30,20))
        company_rank_by_application_pool = company_rank["approved_case"].sort_values(inplace=False, ascending=True)
        ax1 = company_rank_by_application_pool.plot(kind = "barh", alpha = 0.7, color = ["skyblue", "pink","green"], 
                                       figsize = (20,15))
        ax1.set_title("Top 10 Largest Application Pool Companies",fontsize = "large")
        plt.subplots_adjust(bottom = 0.1, left = 0.3)
        pdf.savefig()
        plt.close()
        
        plt.figure(figsize = (30,20))
        ax2 = company_rank[["approved_case", "unapproved_case"]].plot(kind = "bar", alpha = 0.7, stacked = True,color = ["skyblue", "pink"], 
                                       figsize = (20,15), title = "Approval Rate for Top 10 Largest Application Pool Companies")
        ax3 = company_rank["approval_rate"].plot(kind = "line", secondary_y=True,  style = 'ko--' )
        ax2.set_xticklabels(company_rank.index,rotation=45)
        ax3.set_xticklabels(company_rank.index,rotation=45)
        plt.subplots_adjust(bottom = 0.3, left = 0.1)
        pdf.savefig()
        plt.close()
        
        plt.figure(figsize = (30,20))
        ax4 = company_rank["average_wage"].plot(kind = "barh", ylim = [40000,120000], color = "skyblue",figsize = (20,15),
                                             title = "Average Wage for Top 10 Largest Application Pool Companies" )
        plt.subplots_adjust(bottom = 0.1, left = 0.3)
        pdf.savefig()
        plt.close()
        
        print("Further analysis has been saved in your local folder as PDF, please open your folder to check")

    print("please return to the previous dictionary to explore other functions\n")
    
    return

