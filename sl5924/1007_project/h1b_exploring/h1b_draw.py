"""
This is module contains two main methods of plotting
plot_cloropleth_map was designed for plot cloropleth maps with given data
plot_line_chart was designed for plot line charts with given data
All plots based on data from module h1bdata

Created on 2016/12/01
Version: 1.0
@author: Sheng Liu
ShengLiu Copyright 2016-2017

"""


from chorogrid import Colorbin, Chorogrid
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd


states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', \
         'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', \
         'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', \
         'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',\
         'VA', 'WA', 'WV', 'WI', 'WY']
def plot_cloropleth_map(ls,interest,leg,year):

	mycolors = ['#b35806', '#f1a340', '#fee0b6', '#d8daeb', '#998ec3', '#542788']
	mybin = Colorbin(ls, mycolors, proportional=True, decimals=None)
	state_info = pd.read_csv('chorogrid/databases/usa_states.csv')
	colors_by_state = mybin.colors_out
	font_colors_by_state = mybin.complements
	legend_colors = mybin.colors_in
	legend_labels = mybin.labels
	
	cg = Chorogrid('chorogrid/databases/usa_states.csv', states, colors_by_state)
	cg.set_title(str(year)+' H1b '+str(interest), font_dict={'font-size': 19})
	cg.set_legend(legend_colors, legend_labels, title=leg)
	cg.draw_map(spacing_dict={'legend_offset': [-150,-25]})
	cg.done(show=False, save_filename = str(year)+' H1b '+str(interest))

	

def plot_line_chart(ls,y_label,title):
    year = ['2010','2011','2012','2013','2014','2015','2016']
    x = [dt.datetime.strptime(d,'%Y').date() for d in year]
    plt.figure()
    plt.plot(x,ls,lw=1, ls="dashed", markeredgewidth = 0,color = 'Green',
                 marker="o", markersize=8, markerfacecolor = 'Green')
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
    return 


	









