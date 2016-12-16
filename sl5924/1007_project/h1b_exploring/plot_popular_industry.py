'''
Created on Dec 9, 2016

@author: yuweitu
'''
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_popular_industry(industry_data, number, indicator):
         
    occupation_rank = industry_data.newdf.sort_values(by = indicator, ascending = False).ix[:number]
    occupation_rank["unapproved_case"] = occupation_rank["application_pool"]-occupation_rank["approved_case"]
    
    with PdfPages('popular occupation groups ranked by ' + indicator + '.pdf') as pdf:
        plt.figure(figsize = (30,20))
        ax1 = occupation_rank["approved_case"].plot(kind = "barh", alpha = 0.7, color = ["skyblue", "pink","green"], 
                                       figsize = (20,15))
        ax1.set_title('Application pool for top ' + str(number) + ' ' + indicator + ' occupation groups')
        plt.subplots_adjust(bottom = 0.1, left = 0.3)
        pdf.savefig()
        plt.close()
        
        plt.figure(figsize = (30,20))
        ax2 = occupation_rank[["approved_case", "unapproved_case"]].plot(kind = "bar", alpha = 0.7, stacked = True,color = ["skyblue", "pink"], 
                                       figsize = (20,15))
        ax3 = occupation_rank["approval_rate"].plot(kind = "line", secondary_y=True,  style = 'ko--' )
        ax2.set_xticklabels(occupation_rank.index,rotation=45)
        ax3.set_xticklabels(occupation_rank.index,rotation=45)
        ax2.set_title('Approval rate for for top ' + str(number) + ' ' + indicator + ' occupation groups')
        plt.subplots_adjust(bottom = 0.3, left = 0.1)
        pdf.savefig()
        plt.close()
        
        plt.figure(figsize = (30,20))
        ax4 = occupation_rank["average_wage"].plot(kind = "barh", ylim = [40000,120000], color = "skyblue",figsize = (20,15),
                                             title = "Average Wage for Top 10 Largest Application Pool Companies" )
  
        ax4.set_title('Average wage for top for top ' + str(number) + ' ' + indicator + ' occupation groups')
        plt.subplots_adjust(bottom = 0.1, left = 0.3)
        pdf.savefig()
        plt.close()
        
        print("Further analysis has been saved in your local folder as PDF, please open your folder to check")

    print("please return to the previous dictionary to explore other functions\n")
    
    return


def confirm_answer_ploting(industry_data, number, indicator):
    
    user_input = input("are you interested in further analysis for this rank? please input yes or no\n")
    if user_input == 'yes':
        plot_popular_industry(industry_data, number, indicator)
    elif user_input == 'no':
        pass
    
    return