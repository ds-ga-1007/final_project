"""
Module adding plotting functionality relating to time series for data in Yelp databases.
"""
import os
import json
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.widgets import Slider
import matplotlib
import numpy as np


def filterByCity_mask(business_df, city):
    """
    :param business_df: Dataframe containing business data. Assumes that the dataframe contains city
        information
    :param city: String of one of the 9 cities in the Yelp database
    :return: Boolean mask representing whether each business is in specified city
    """
    # City listed in database are too granular (e.g. Dravosburg and Bethel Park are both suburbs of
    # Pittsburgh), so states are used as a more accurate classifier of city
    states_dict = {'Edinburgh': 'EDH', 'Karlsruhe': 'KHL', 'Montreal': 'QC', 'Waterloo': 'ON',
                   'Pittsburgh': 'PA', 'Urbana-Champaign': 'IL', 'Phoenix': 'AZ', 'Las Vegas': 'NV', 'Madison': 'WI'}
    mask = business_df['state'] == states_dict[city]
    return mask.values
    

def filterByCategory_mask(business_df, category):
    """
    :param business_df: Dataframe containing business data. Assumes that the dataframe contains
        business category information
    :param category: String representing a business category
    :return: Boolean mask representing whether each business is in specified business category
    """
    category_series = business_df['categories']
    mask = []
    for i in range(len(category_series)):
        mask.append(category in category_series.values[i])
    mask = np.array(mask)
    return mask


def filter_by_City_and_Category(business_df, checkin_df, checkin_matrixform, city=None, category=None):
    """
    :param business_df: Dataframe containing business data. Assumes that the dataframe contains
        business city, category and ID information
    :param checkin_df: Dataframe containing checkin data. Assumes that there is some intersection of
        business IDs with business_df
    :checkin_matrixform: 7x24xlen(checkin_df) numpy array corresponding to checkins per hour and day for each business in checkin_df
    :param city: String of one of the 9 cities in the Yelp database; If None then no city filter will
        be applied.
    :param category: String representing a business category; If None then no category filter will be
        applied.
    :return: 7 x 24 x (X) Numpy array containing checkin numbers only for the (X) businesses in specified city/category
    """
    matched_business_df = business_df[business_df['business_id'].isin(checkin_df['business_id'].values)]
        
    if city is None:
        city_mask = [True]*len(checkin_df)
    else:
        city_mask = filterByCity_mask(matched_business_df, city)
        
    if category is None:
        category_mask = [True]*len(checkin_df)
    else:
        category_mask = filterByCategory_mask(matched_business_df, category)
        
    if (city is None) and (category is None):
        filtered_checkin_matrix = checkin_matrixform
    else:
        filtered_checkin_matrix = checkin_matrixform[:,:,(city_mask & category_mask)]
        
    return filtered_checkin_matrix


def check_city(city):
    """
    :param city: String containing the name of a city. Error is raised if not one of 9 cities in the Yelp database.
    """
    cities_list = ['Edinburgh', 'Karlsruhe', 'Montreal', 'Waterloo',
                   'Pittsburgh', 'Urbana-Champaign', 'Phoenix', 'Las Vegas', 'Madison']
        
    if city is None:
        pass
    elif city not in cities_list:
        raise KeyError('No such city within Yelp Dataset')
        return


def check_category(category, category_list):
    """
    :param category: String containing the name of a business category. Error is raised if
        category given is not in category_list.
    :param category_list: Array-like containing all of the names of business categories in the Yelp dataset.
    """
    
    if category is None:
        pass
    elif category not in category_list:
        raise KeyError('No such business category within Yelp Dataset')
    return
    

def generate_Time_Series(business_df, checkin_df, checkin_matrixform, category_list, city=None, category=None):
    """
    :param business_df: Dataframe containing business data. Assumes that the dataframe contains
        business city, category and ID information
    :param checkin_df: Dataframe containing checkin data. Assumes that there is some intersection of
        business IDs with business_df
    :checkin_matrixform: 7x24xlen(checkin_df) numpy array corresponding to checkins per hour and day for each business in checkin_df
    :param city: String of one of the 9 cities in the Yelp database; If None then no city filter will be applied.
    :param category_list: List containing strings of business categories; If None then no category filter will be
        applied.
    :return: Time series plot of fraction of checkins by hour for businesses in specified city/category. Checkin times
        have been adjusted to each city's local time.
    """
    check_city(city)
    check_category(category, category_list)
                    
    filtered_checkin_matrix = filter_by_City_and_Category(business_df, checkin_df, checkin_matrixform, city, category)
                        
    hours = filtered_checkin_matrix.sum(axis=2).sum(axis=0)
                            
    hours_frac = get_hours_fraction(hours)
                                
    shift = get_timezone_shift(city)
                                    
    city_label, category_label = generate_labels(city, category)
    
    plt.figure(figsize = (12,8))
    plt.plot(range(25), hours_frac[0 + shift:25 + shift], '-o')
    plt.xlabel('Hour', fontsize = 18)
    plt.ylabel('Fraction of checkins', fontsize = 18)
    plt.xlim([0, 24])
    plt.title('Time Series with City = ' + city_label + ', Category = ' + category_label, fontsize = 20)
    plt.show()


def compare_Time_Series(business_df, checkin_df, checkin_matrixform, category_list, city1 = None, category1 = None, city2 = None, category2 = None):
    """
    :param business_df: Dataframe containing business data. Assumes that the dataframe contains business city, category and ID information
    :param checkin_df: Dataframe containing checkin data. Assumes that there is some intersection of
            business IDs with business_df
    :checkin_matrixform: 7x24xlen(checkin_df) numpy array corresponding to checkins per hour and day for each business in checkin_df
    :param city1: String of one of the 9 cities in the Yelp database; If None then no city filter will be applied.
    :param category1: String representing a business category; If None then no category filter will be
            applied.
    :param city2: String of one of the 9 cities in the Yelp database; If None then no city filter will be applied.
    :param category2: String representing a business category; If None then no category filter will be
            applied.
        
    :return: Comparison time series plot of fraction of checkins by hour for businesses in city1/category1 vs. city2/category2. Checkin times have been adjusted to each city's local time.
    """
    check_city(city1)
    check_city(city2)
    check_category(category1, category_list)
    check_category(category2, category_list)
                            
    plt.figure(figsize = (12,8))
                                
    filtered_checkin_matrix1 = filter_by_City_and_Category(business_df, checkin_df, checkin_matrixform, city1, category1)
    filtered_checkin_matrix2 = filter_by_City_and_Category(business_df, checkin_df, checkin_matrixform, city2, category2)
                                        
    hours1 = filtered_checkin_matrix1.sum(axis=2).sum(axis=0)
    hours2 = filtered_checkin_matrix2.sum(axis=2).sum(axis=0)
                                                
    hours_frac1 = get_hours_fraction(hours1)
    hours_frac2 = get_hours_fraction(hours2)
                                                        
    shift1 = get_timezone_shift(city1)
    shift2 = get_timezone_shift(city2)
                                                                
    city_label1, category_label1 = generate_labels(city1, category1)
    city_label2, category_label2 = generate_labels(city2, category2)
                                                                        
    plt.plot(range(25), hours_frac1[0 + shift1:25 + shift1], '-o', label = 'City = ' + city_label1 + ', Category = ' + category_label1)
    plt.plot(range(25), hours_frac2[0 + shift2:25 + shift2], '-o', label = 'City = ' + city_label2 + ', Category = ' + category_label2)
                                                                                
    plt.xlabel('Local Time (Hours)', fontsize = 18)
    plt.ylabel('Fraction of checkins', fontsize = 18)
    plt.title('Comparison of Time Series', fontsize = 20)
    plt.xlim([0, 24])
    plt.legend(loc = 2)
    plt.show()


def get_hours_fraction(hours):
    """
    :hours: 24x1 numpy array of total checkins by hour. to 48x1 array of fraction of checkins by hour
    :return: 48x1 numpy array corresponding to the fraction of total checkins by hour. A periodic extension is used to allow for timezone adjustments.
    """
    hours_frac = hours / np.sum(hours)
    hours_frac = np.append(hours_frac, hours_frac)
    return hours_frac


def get_timezone_shift(city = None):
    """
    :param city: String of one of the 9 cities in the Yelp database; If None then no timezone shift will be applied.
    :return: Int indicating how many hours to shift each time series to convert it from San Francisco time to local time.
    """
    timezone_dict = {'Edinburgh': -8, 'Karlsruhe': -9, 'Montreal': -3, 'Waterloo': -3,
        'Pittsburgh': -3, 'Urbana-Champaign': -2, 'Phoenix': -1, 'Las Vegas': 0, 'Madison': -2}
        
    if city is None:
        shift = 0
    else:
        shift = np.mod(timezone_dict[city],24)
        
    return shift
    

def generate_labels(city = None, category = None):
    """
    :param city: String of one of the 9 cities in the Yelp database; If None then city label will be 'Any'.
    :param category: String representing a business category; If None then category label will be 'All'.
    :return: Strings containing city and category labels for plotting time series.
    """
    if city is None:
        city_label = 'All'
    else:
        city_label = city
        
    if category is None:
        category_label = 'All'
    else:
        category_label = category
    return city_label, category_label
    

def get_checkins_9cities(business_df, checkin_df, checkin_matrixform):
    """
    :param business_df: Dataframe containing business data. Assumes that the dataframe contains business city and ID information
    :param checkin_df: Dataframe containing checkin data. Assumes that there is some intersection of business IDs with business_df
    :checkin_matrixform: 7x24xlen(checkin_df) numpy array corresponding to checkins per hour and day for each business in checkin_df
    :return: Dataframe containing total checkins per hour for each of the 9 cities in the Yelp dataset.
    """
    cities_list = ['Edinburgh', 'Karlsruhe', 'Montreal', 'Waterloo',
                   'Pittsburgh', 'Urbana-Champaign', 'Phoenix', 'Las Vegas', 'Madison']
    matrix = np.zeros((24, len(cities_list)))
                       
    for i, city in enumerate(cities_list):
        hourly_checkins = filter_by_City_and_Category(business_df, checkin_df, checkin_matrixform, city).sum(axis=2).sum(axis=0)
        hourly_checkins_frac = get_hours_fraction(hourly_checkins)
        shift = get_timezone_shift(city)
        matrix[:,i] = hourly_checkins_frac[0+shift:24+shift]
                           
    city_checkin_df = pd.DataFrame(matrix, columns=cities_list)
                               
    return city_checkin_df
                           

def plot_total_checkins_9cities(business_df,checkin_df, checkin_matrixform, start_hour = 12):
    """
    :param business_df: Dataframe containing business data. Assumes that the dataframe contains business city and ID information
    :param checkin_df: Dataframe containing checkin data. Assumes that there is some intersection of business IDs with business_df
    :checkin_matrixform: 7x24xlen(checkin_df) numpy array corresponding to checkins per hour and day for each business in checkin_df
    :start_hour: int between 0 and 23 corresponding to initial hour shown.
    :return: Barplot containing total checkins per hour for each of the 9 cities in the Yelp dataset. Plot slider allows for adjustment specified hour to compare.
    """
    city_checkin_df = get_checkins_9cities(business_df, checkin_df, checkin_matrixform)
    fig, ax = plt.subplots(figsize = (14,9))
    plt.subplots_adjust(left=0.25, bottom=0.25)
        
    hour = start_hour
    barplt = city_checkin_df.ix[hour].plot(kind = 'bar', ax = ax)
    plt.ylabel("Fraction of City's Checkins", fontsize = 15)
    fig.suptitle('Checkin distribution when hour = ' + str(hour), fontsize=20)
    plt.xticks(rotation = 30)
        
    axcolor = 'lightgoldenrodyellow'
    axhour = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
        
    shour = Slider(axhour, 'Hour', 0, 23, valinit=start_hour)
    
    def slider_update(val):
        """
        Update function for slider, shifts the specified hour to the truncation of current slider value.
        """
        ax.clear()
        hour = int(val)
        barplt = city_checkin_df.ix[hour].plot(kind='bar', ax = ax)
        ax.set_ylabel("Fraction of City's Checkins", fontsize = 15)
        fig.suptitle('Checkin distribution when hour = ' + str(hour), fontsize=20)
        ax.set_xticklabels(city_checkin_df.columns, rotation=30)
    
    shour.on_changed(slider_update)
    plt.show()
    


