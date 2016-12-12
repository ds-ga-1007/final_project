import pandas as pd
import numpy as np
import webbrowser #open the college map in browser
import matplotlib.pyplot as plt
from function import *
from information_and_plot import *
from clean_data import *


def justify_order(order,data_top_10):
    #Justify if the input is valid. flag=0 for correct input and 1 indicates wrong input.
    flag=0;
    if(order.isdigit()==False):
        flag=1
    elif(int(order)<1 or int(order)>len(data_top_10)):
        flag=1
    else:
        flag=0
    return flag

def main():
    #Given the data, first let the user to input their SAT or ACT score and find top 10 suitable colleges
    data=pd.read_excel(complete_path,"Sheet1")
    data_top_10=search(data)
    #If no suitable colleges, set flag=1; if user quit, set flag=2; if there are some choices, flag=3
    if(type(data_top_10)==str):
        if(data_top_10=="There is no available world ranking top 1000 collges available for you, please try next year. Fighting!"):
            flag=1 
        else:
            flag=2    
    else:
        flag=3
    #If there are suitable choices, further plot and information will be given
    if(flag==3):
        data_show(data_top_10)
        #If the input order is not valid, the program will ask the user to input again until correct or quit
        user_order=input("Please enter the order of your favorite college. Order from 1 to %d. Finish the program by entering quit.\n"%len(data_top_10))
        flag_sub=justify_order(user_order,data_top_10)
        while(user_order!='quit'):
            while(flag_sub==1):
                user_order=input("The last input is not valid. Please enter the order of your favorite college. Order from 1 to %d. Finish the program by entering quit.\n"%len(data_top_10))
                flag_sub=justify_order(user_order,data_top_10)
                if(user_order=='quit'):
                    break
            if(flag_sub==0):
                #If the input is valid, a brief introduction and some figures will appear.
                inroduction_figure=plot_infor(data_top_10,int(user_order))
                inroduction_figure.Map_plot()
                webbrowser.open("file://"+data_path+'/college_map.html')
                inroduction_figure.Age_plot()
                plt.show()
                inroduction_figure.WR_NR_plot()
                plt.show()
                inroduction_figure.crime_plot()
                plt.show()
                inroduction_figure.Earning_plot()
                plt.show()
                inroduction_figure.intro()
                user_order=input("Please enter the order of your favorite college. Order from 1 to %d. Finish the program by entering quit.\n"%len(data_top_10))
                flag_sub=justify_order(user_order,data_top_10)
        if(user_order=='quit'):
            print("You have already quited the program. Thanks for using!")
    if(flag==1):
        print("There is no available world ranking top 1000 collges available for you, please try next year. Fighting!")
    if(flag==2):
        print("You have already quited the program. Thanks for using!")
        
        
if __name__ == "__main__":
    try:
        main()
    except:
        print("Keyboard Interruption or desirable college information missing") 
