# The final project of DS-GA 1007
# NYU Center for Data Science
# Authors: Jiaming Dong (jd3405@nyu.edu)
#          Daniel Amaranto (da1933@nyu.edu)
#          Julie Cachia (jyc436@nyu.edu)
#
# The MyPloter class


import matplotlib.pyplot as plt
import pandas as pd
import seaborn
from errors import *


class MyPloter:
    def __init__(self, business_data, user_data):
        self.business_data = business_data
        self.user_data = user_data
        # the business data attributes which are plotted in pie
        self.business_pie = ["reservations", "delivery", "credit_cards", "states", "cities", "common_categories"]
        # the business data attributes which are plotted in histogram
        self.business_hist = ["review_count", "prices"]
        # the user data attributes which are plotted in histogram
        self.user_hist = ["review_count"]
        # the user data attributes which are plotted in pie
        self.user_pie = ["yelping_since"]
        self.user_box = ["votedFunny", "votedCool", "votedUseful", "fans"]
        self.title = ""

    def plot(self, plot_type, plot_attribute, star_start, star_end=None):
        """given some parameters, plot a graph"""
        self.title = plot_type + " " + plot_attribute
        if star_end is None:
            star_end = star_start
            self.title += " " + str(star_start) + " star"
        else:
            self.title += " " + str(star_start) + " to " + str(star_end) + " star"
        if plot_type == "business":
            if plot_attribute in self.business_hist:
                # for histogram graph, we use list
                data_to_plot = self.business_data.get_data_range(plot_attribute, star_start, star_end)
                self.plot_hist(data_to_plot)
            else:
                if plot_attribute in self.business_pie:
                    # for pie graph, we use series
                    data_to_plot = self.business_data.get_series_range(plot_attribute, star_start, star_end)
                    self.plot_pie(data_to_plot)
                else:
                    raise AttributeNotFoundException

        else:
            if plot_attribute in self.user_hist:
                # for histogram graph, we use list
                data_to_plot = self.user_data.get_data_range(plot_attribute, star_start, star_end)
                self.plot_hist(data_to_plot)
            elif plot_attribute in self.user_box:
                data_to_plot = self.user_data.get_data_range(plot_attribute, star_start, star_end)
                self.plot_box(data_to_plot)
            else:
                if plot_attribute in self.user_pie:
                    # for pie graph, we use series
                    data_to_plot = self.user_data.get_series_range(plot_attribute, star_start, star_end)
                    self.plot_pie(pd.Series(data_to_plot))
                else:
                    raise AttributeNotFoundException

    def plot_hist(self, data):
        """plot a histogram using matplotlib"""
        plt.hist(data)
        plt.title(self.title)
        plt.show()
    
    def plot_box(self,data):
        plt.boxplot(data, showfliers=False)
        plt.title(self.title)
        plt.show()
        
    def plot_pie(self, data):
        """plot a pie graph with pandas.Series"""
        data.plot(kind='pie')
        plt.title(self.title)
        plt.show()
