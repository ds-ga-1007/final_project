# coding: utf-8

# In[6]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class AccidentAnalysis(object):
    
    def __init__(self, df):
        self.df = df
        self.df['YEAR'] = [x[6:] for x in self.df['DATE']]
        self.df['MONTH'] = [x[:2] for x in self.df['DATE']]
    
    def select_year(self, year):
        '''Select dataframe of one year.'''
        df_year = self.df[self.df['YEAR'] == str(year)]
        return df_year
    
    def select_borough(self, borough):
        '''Select dataframe of one borough.'''
        df_borough = self.df[self.df['BOROUGH'] == str(borough).upper()]
        return df_borough
    
    def select_borough_year(self, year, borough):
        '''Select dataframe of one borough in one year.'''
        df_borough_year = self.select_borough(borough)[self.select_borough(borough)['YEAR'] == str(year)]
        return df_borough_year
    
    def group_total(self):
        '''Group by year and borough.'''
        df_total = self.df.groupby(['YEAR','BOROUGH'])['BOROUGH'].count().unstack()
        return df_total
    
    def group_total_injured(self):
        '''Group injured by year and borough.'''
        df_injured = self.df.groupby(['YEAR','BOROUGH'])['NUMBER OF PERSONS INJURED'].sum().unstack()
        return df_injured
    
    def group_total_killed(self):
        '''Group killed by year and borough.'''
        df_killed = self.df.groupby(['YEAR','BOROUGH'])['NUMBER OF PERSONS KILLED'].sum().unstack()
        return df_killed
    
    def count_borough_total(self):
        '''Group by borough across years.'''
        borough_count = self.df.groupby('BOROUGH')['BOROUGH'].count()
        return borough_count
        
    def count_borough_year(self, year):
        '''Group by borough of one year.'''
        borough_count = self.select_year(year).groupby('BOROUGH')['BOROUGH'].count()
        return borough_count
    
    def count_borough_injured(self, year):
        '''Group injured by borough of one year.'''
        borough_count = self.select_year(year).groupby('BOROUGH')['NUMBER OF PERSONS INJURED'].sum()
        return borough_count
    
    def count_borough_killed(self, year):
        '''Group killed by borough of one year.'''
        borough_count = self.select_year(year).groupby('BOROUGH')['NUMBER OF PERSONS KILLED'].sum()
        return borough_count
    
    def count_year_total(self, borough):
        '''Count total collisions in each year of one borough.'''
        year_count = self.select_borough(borough).groupby(['YEAR'])['YEAR'].count()
        return year_count
    
    def count_year_injured(self, borough):
        '''Count injured in each year of one borough.'''
        year_count = self.select_borough(borough).groupby(['YEAR'])['NUMBER OF PERSONS INJURED'].sum()
        return year_count
    
    def count_year_killed(self, borough):
        '''Count killed in each year of one borough.'''
        year_count = self.select_borough(borough).groupby(['YEAR'])['NUMBER OF PERSONS KILLED'].sum()
        return year_count
    
    def sort_zip_total(self, year):
        '''Sort zip codes frequency of one year.'''
        zip_count = self.select_year(year).groupby(['ZIP CODE'])['ZIP CODE'].count()
        zip_count.index = zip_count.index.map(int)
        zip_sort = zip_count.sort_values(ascending=False)
        top20_zip = zip_sort.index[:20]
        return zip_sort[top20_zip]
    
    def sort_zip_borough(self, year, borough):
        '''Sort zip codes frequency of one year in one borough.'''
        zip_count = self.select_borough_year(year, borough).groupby('ZIP CODE')['ZIP CODE'].count()
        zip_count.index = zip_count.index.map(int)
        zip_sort = zip_count.sort_values(ascending=False)
        top20_zip = zip_sort.index[:20]
        return zip_sort[top20_zip]

    def sort_reasons_total(self, year):
        '''Sort reasons frequency of one year.'''
        df_reasons = pd.DataFrame()
        df_year = self.select_year(year)
        for i in range(5):
            df_reasons['VEHICLE ' + str(i+1)] = df_year.groupby('CONTRIBUTING FACTOR VEHICLE ' + str(i+1))['CONTRIBUTING FACTOR VEHICLE ' + str(i+1)].count()
        df_reasons.index.name = None
        sorted_reasons = df_reasons.sum(axis=1).sort_values(ascending=False)
        top20_reasons = sorted_reasons[:20]
        return top20_reasons
    
    def sort_reasons_borough(self, year, borough):
        '''Sort reasons frequency of one year in one borough.'''
        df_reasons = pd.DataFrame()
        df_borough_year = self.select_borough_year(year, borough)
        for i in range(5):
            df_reasons['VEHICLE ' + str(i+1)] = df_borough_year.groupby('CONTRIBUTING FACTOR VEHICLE ' + str(i+1))['CONTRIBUTING FACTOR VEHICLE ' + str(i+1)].count()
        df_reasons.index.name = None
        sorted_reasons = df_reasons.sum(axis=1).sort_values(ascending=False)
        top20_reasons = sorted_reasons[:20]
        return top20_reasons
    
    def sort_types_total(self, year):
        '''Sort vehicle types frequency of one year.'''
        df_types = pd.DataFrame()
        df_year = self.select_year(year)
        for i in range(5):
            df_types['VEHICLE ' + str(i+1)] = df_year.groupby('VEHICLE TYPE CODE ' + str(i+1))['VEHICLE TYPE CODE ' + str(i+1)].count()
        df_types.index.name = None
        sorted_types = df_types.sum(axis=1).sort_values(ascending=False)
        return sorted_types[:20]
    
    def sort_types_borough(self, year, borough):
        '''Sort vehicle types frequency of one year of one borough.'''
        df_types = pd.DataFrame()
        df_borough_year = self.select_borough_year(year, borough)
        for i in range(5):
            df_types['VEHICLE ' + str(i+1)] = df_borough_year.groupby('VEHICLE TYPE CODE ' + str(i+1))['VEHICLE TYPE CODE ' + str(i+1)].count()
        df_types.index.name = None
        sorted_types = df_types.sum(axis=1).sort_values(ascending=False)
        return sorted_types[:20]


# In[19]:

class Plots(AccidentAnalysis):
    '''This class is used to plot all the figures.'''
    
    def plot_lines_total(self):
        '''Plot the lines of total number of collisions in different boroughs each year.'''
        plt.clf()
        self.group_total().plot()
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.ylabel('Number of Collisions')
        plt.xlabel('Year')
        plt.title('Number of Collisions in Different Boroughs Each Year')
        plt.grid()
        plt.show()

    def plot_lines_injured(self):
        '''Plot the lines of number of persons injured in different boroughs each year.'''
        plt.clf()
        self.group_total_injured().plot()
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.ylabel('Number of Persons Injured')
        plt.xlabel('Year')
        plt.title('Number of Persons Injured in Different Boroughs Each Year')
        plt.grid()
        plt.show()

    def plot_lines_killed(self):
        '''Plot the lines of number of persons killed in different boroughs each year.'''
        plt.clf()
        self.group_total_killed().plot()
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.ylabel('Number of Persons Killed')
        plt.xlabel('Year')
        plt.title('Number of Persons Killed in Different Boroughs Each Year')
        plt.grid()
        plt.show()

    def plot_pie_total(self):
        '''Plot the pie chart of collisions in different areas across years.'''
        plt.clf()
        self.count_borough_total().plot.pie(colors=['plum', 'lightgreen', 'lightcoral', 'lightskyblue', 'rosybrown'], figsize=(6,6), autopct='%1.1f%%', shadow=True)
        plt.ylabel('')
        plt.title('Pie Chart of Collisions in Different Areas')
        plt.show()

    def plot_pie_year(self, year):
        '''Plot the pie chart of collisions in different areas in one year.'''
        plt.clf()
        self.count_borough_year(year).plot.pie(colors=['plum', 'lightgreen', 'lightcoral', 'lightskyblue', 'rosybrown'], figsize=(6,6), autopct='%1.1f%%', shadow=True)
        plt.ylabel('')
        plt.title('Pie Chart of Collisions in Different Areas in ' + str(year))
        plt.show()

    def plot_year_total(self, borough):
        '''Plot the lines of collisions of a borough.'''
        plt.clf()
        self.count_year_total(borough).plot()
        plt.ylabel('Number of Collisions')
        plt.xlabel('Year')
        plt.grid()
        plt.title('The Number of Collisions for ' + str(borough).title())
        plt.show()

    def plot_year_injured(self, borough):
        '''Plot the lines of number of persons injured of a borough.'''
        plt.clf()
        self.count_year_injured(borough).plot()
        plt.ylabel('Number of Persons Injured')
        plt.xlabel('Year')
        plt.grid()
        plt.title('The Number of Persons Injured for ' + str(borough).title())
        plt.show()

    def plot_year_killed(self, borough):
        '''Plot the lines of number of persons killed of a borough.'''
        plt.clf()
        self.count_year_killed(borough).plot()
        plt.ylabel('Number of Persons Killed')
        plt.xlabel('Year')
        plt.grid()
        plt.title('The Number of Persons Killed for ' + str(borough).title())
        plt.show()

    def plot_zip_total(self, year):
        '''Plot collisions of sorted zip codes in one year.'''
        plt.clf()
        self.sort_zip_total(year).plot.bar(alpha=0.5)
        plt.title('Number of Collisions in Top 20 Zip Codes in ' + str(year))
        plt.xlabel('Zip Codes')
        plt.ylabel('Number of Collisions')
        plt.show()

    def plot_zip_borough(self, year, borough):
        '''Plot collisions of sorted zip codes of different boroughs in one year.'''
        plt.clf()
        self.sort_zip_borough(year, borough).plot.bar(alpha=0.5)
        plt.title('Number of Collisions of Top 20 Zip Codes in ' + str(borough).title() + ' in ' + str(year), fontsize=11)
        plt.xlabel('Zip Codes')
        plt.ylabel('Number of Collisions')
        plt.show()

    def plot_reasons_total(self, year):
        '''Plot collisions of sorted reasons in one year.'''
        plt.clf()
        self.sort_reasons_total(year).plot.bar(alpha=0.5)
        plt.title('Top 20 Reasons for Collisions in ' + str(year))
        plt.xlabel('Reasons')
        plt.ylabel('Number of Collisions')
        plt.show()

    def plot_reasons_borough(self, year, borough):
        '''Plot collisions of sorted reasons of different boroughs in one year.'''
        plt.clf()
        self.sort_reasons_borough(year, borough).plot.bar(alpha=0.5)
        plt.title('Top 20 Reasons for Collisions in ' + str(borough).title() + ' in '  + str(year), fontsize=11)
        plt.xlabel('Reasons')
        plt.ylabel('Number of Collisions')
        plt.show()
        
    def plot_types_total(self, year):
        plt.clf()
        self.sort_types_total(year).plot.bar(alpha=0.5)
        plt.title('Number of Collisions per Vehicle Type in ' + str(year))
        plt.xlabel('Types')
        plt.ylabel('Number of Collisions')
        plt.show()
        
    def plot_types_borough(self, year, borough):
        plt.clf()
        self.sort_types_borough(year, borough).plot.bar(alpha=0.5)
        plt.title('Number of Collisions per Vehicle Type in ' + str(borough).title() + ' in '  + str(year), fontsize=11)
        plt.xlabel('Types')
        plt.ylabel('Number of Collisions')
        plt.show()


# In[ ]:

