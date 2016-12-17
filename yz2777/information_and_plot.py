import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from function import *
import folium #utilize to plot map
from clean_data import *
import os

#data_top_10 is the suitable top 10 US available colleges from "data_top_10=search(data)" and user_order is user input order choice
class plot_infor():
    def __init__(self,data_top_10,user_order):
        # remember the input top 10 suitable colleges and the input user order choice
        self.data_top_10=data_top_10
        self.user_order=user_order
        #Return the order, US rank and name of these 10 available colleges
        data_top_10_sub=data_top_10[['INSTNM','UNITID']]
        data_top_10_sub.index=range(1,len(data_top_10_sub)+1)
        #The user choose the most favorite college among these 10
        self.user_college=data_top_10[data_top_10['UNITID']==data_top_10_sub['UNITID'][user_order]]
    
    def intro(self):
        #A brief introduction for the desirable college
        #Calculate the mean value and std of crime numbers from 2001 to 2014
        user_college=self.user_college
        crime_user_college=np.array(user_college[['CRIME2014','CRIME2013', 'CRIME2012', 'CRIME2011', 'CRIME2010', 'CRIME2009','CRIME2008', 'CRIME2007', 'CRIME2006', 'CRIME2005', 'CRIME2004','CRIME2003', 'CRIME2002', 'CRIME2001']])
        crime_mean=np.mean(crime_user_college)
        crime_std=np.std(crime_user_college)
        #Return the brief introduction of this school
        #First introduce the college name and rank
        string="The college %s"%user_college['INSTNM'].item()
        string=string+" has 2016 US rank %d"%user_college['NR2016'].item()
        string=string+" and 2016 world rank %d."%user_college['WR2016'].item()
        #Second introduce the college location
        string=string+" The college is located in state %s,"%user_college['STABBR'].item()
        string=string+" city %s"%user_college['CITY'].item()
        string=string+" with zip code %s."%user_college['ZIP'].item()
        #Thrid introduce the adimission rate and annal cost
        string=string+" The average admission rate of this college is %f"%user_college['ADM_RATE'].item()
        string=string+" and annal cost for attending is around $%f."%user_college['COSTT4_A'].item()
        #Fourth introduce the mean and std of crime numbers from 2001 to 2014
        string=string+" From 2001 to 2014, the average crime number is %f"%crime_mean
        string=string+" with standard deviation %f."%crime_std
        #Fifth introduce the website
        string=string+" For some further information, please visit the college website %s"%user_college['INSTURL'].item()
        print(string)

    def crime_plot(self):
        #Plot the crime trend from 2001 to 2014
        #Find the crime numbers from 2001 to 2014
        user_college=self.user_college
        crime_user_college=user_college[['CRIME2001','CRIME2002', 'CRIME2003', 'CRIME2004', 'CRIME2005', 'CRIME2006','CRIME2007', 'CRIME2008', 'CRIME2009', 'CRIME2010', 'CRIME2011','CRIME2012', 'CRIME2013', 'CRIME2014']]
        crime_user_college=crime_user_college.transpose()
        #Change the index to year 2001 to 2014
        crime_user_college.index=range(2001,2015)
        crime_user_college.columns=['Crime number trend']
        #Drop the missing value
        crime_user_college_trend=crime_user_college.dropna()
        #Plot the trend by scatter plot and linear regression
        if(len(crime_user_college_trend)>10):
            #Do the linear regression and scatterplot
            Year=list(crime_user_college.index)
            Year=sm.add_constant(Year)  
            Rate=list(crime_user_college['Crime number trend'])
            est=sm.OLS(Rate, Year)
            est=est.fit()
            Rate_hat = est.predict(Year)
            plt.plot(Year[:,1], Rate_hat, 'r', alpha=0.9)
            crime_trend_figure=plt.scatter(Year[:,1], Rate, alpha=0.3)
            plt.xlabel("Year")
            plt.ylabel("Crime number")
            plt.title("The linear regression trend of crime number from 2001 to 2014 for %s"%user_college['INSTNM'].item())
            plt.close
            return crime_trend_figure
        else:
            #If there is not enough avaialable points, a warning will appear
            print("The crime information is not available")
    
    def WR_NR_plot(self):
        #Plot the world and US ranking trend from 2001 to 2014
        #Find the world and US ranking from 2014 to 2016
        user_college=self.user_college
        ranking=user_college[['WR2014','WR2015','WR2016','NR2014','NR2015','NR2016']]
        #Change the data frame from one column to two columns
        ranking_array=np.array(ranking)
        ranking_array_T=ranking_array.reshape(2,3).transpose()
        ranking_frame=pd.DataFrame(ranking_array_T)
        ranking_frame.index=range(2014,2017)
        ranking_frame.columns=['World ranking trend', 'US ranking trend']
        ranking_trend_figure=plt.plot(ranking_frame,'-o')
        #Define the range of y axis for ranking
        plt.ylim([np.min(ranking_array)-1,np.max(ranking_array)+1])
        plt.xlabel("Year")
        plt.ylabel("Rank")
        plt.title("The world and US ranking from 2014 to 2016 for college %s"%user_college['INSTNM'].item())
        plt.close
        return ranking_trend_figure

    def Earning_plot(self):
        #Plot the 10%, 25%, 50%, 75%, 90% earnings 6, 8, 10 years after graduation 
        user_college=self.user_college
        earnings_10=user_college[['PCT10_EARN_WNE_P10','PCT25_EARN_WNE_P10','MD_EARN_WNE_P10','PCT75_EARN_WNE_P10','PCT90_EARN_WNE_P10']].transpose()
        earnings_8=user_college[['PCT10_EARN_WNE_P8','PCT25_EARN_WNE_P8','MD_EARN_WNE_P8','PCT75_EARN_WNE_P8','PCT90_EARN_WNE_P8']].transpose()
        earnings_6=user_college[['PCT10_EARN_WNE_P6','PCT25_EARN_WNE_P6','MD_EARN_WNE_P6','PCT75_EARN_WNE_P6','PCT90_EARN_WNE_P6']].transpose()
        earnings_10.columns=['10 years after graduation']
        earnings_10.index=[10,25,50,75,90]
        earnings_8.columns=['8 years after graduation']
        earnings_8.index=[10,25,50,75,90]
        earnings_6.columns=['6 years after graduation']
        earnings_6.index=[10,25,50,75,90]
        earnings_10=earnings_10.dropna()
        earnings_8=earnings_8.dropna()
        earnings_6=earnings_6.dropna()
        #If there is not enough information for earnings, a warning will appear
        if(len(earnings_6)==5 and len(earnings_8)==5 and len(earnings_10)==5):
            #Plot the linear trend of 10, 25, 50, 75, 90 quantile earnings for 6, 8, 10 years after graduation
            Q=[10,25,50,75,90]
            Q=sm.add_constant(Q)
            Earn6=list(earnings_6['6 years after graduation'])
            est6=sm.OLS(Earn6, Q)
            est6=est6.fit()
            Earn6_hat = est6.predict(Q)
            Earn6_plot,=plt.plot(Q[:,1], Earn6_hat, 'r', alpha=0.9)
            Earn8=list(earnings_8['8 years after graduation'])
            est8=sm.OLS(Earn8, Q)
            est8=est8.fit()
            Earn8_hat = est8.predict(Q)
            Earn8_plot,=plt.plot(Q[:,1], Earn8_hat, 'b', alpha=0.9)
            Earn10=list(earnings_10['10 years after graduation'])
            est10=sm.OLS(Earn10, Q)
            est10=est10.fit()
            Earn10_hat = est10.predict(Q)
            Earn10_plot,=plt.plot(Q[:,1], Earn10_hat, 'g', alpha=0.9)
            plt.legend([Earn6_plot,Earn8_plot,Earn10_plot], ["6 years after graduation", "8 years after graduation", "10 years after graduation"])
            plt.xlabel("Quantile")
            plt.ylabel("Earnings")
            plt.title("linear trend of 10, 25, 50, 75, 90 quantile earnings for college %s"%user_college['INSTNM'].item())       
            return Earn10_plot
        else:
            print("The information for earnings is not available")

    def Age_plot(self):
        #Plot the percentage of students whose age > 25
        user_college=self.user_college
        per=user_college['UG25ABV'].item()
        #If the percentage is available, the pei chart will be shown
        if(isinstance(per, float)):
            labels='Above 25 years old', 'Below or equal to 25 years old'
            size=[100*per,100*(1-per)]
            colors=['red','blue']
            Age_figure=plt.pie(size,colors=colors,labels=labels,autopct='%1.2f%%',shadow=True)
            plt.title("The pie chart for college %s students age"%user_college['INSTNM'].item())
            plt.close
            return Age_figure
        else:
            #If the percentage is NA, the warning will be shown
            print("The percentage of students whose age > 25 is not available")

    def Map_plot(self):
        #Learn from python-visualization/folium (https://github.com/python-visualization/folium/)
        user_college=self.user_college
        #Check whether the latitude amd longitude are missing
        if len(user_college[['LATITUDE']].dropna()) != 1 or len(user_college[['LONGITUDE']].dropna()) != 1:
            print("Detailed location information is not available on map")
        else:
            #Get latitude amd longitude and school name 
            la_user_college=user_college['LATITUDE'].item()
            lo_user_college=user_college['LONGITUDE'].item()
            name_user_college=user_college['INSTNM'].item()
            #Generate location in map, start from zoom 4 which is the whole US map
            map_user_college=folium.Map(location=[la_user_college, lo_user_college],zoom_start=4)
            folium.RegularPolygonMarker(location=[la_user_college, lo_user_college], popup=str(name_user_college), fill_color='#FCE112', number_of_sides=3, radius=9).add_to(map_user_college)
            map_user_college.save(data_path+'/college_map.html')




        
