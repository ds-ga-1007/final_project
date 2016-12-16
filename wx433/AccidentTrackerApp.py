'''Tkinter Python GUI'''
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
''' the backend of matplotlib '''

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import *

from AccidentAnalysis import *

EXTRA_LARGE_FONT = ('Helvatica', 24)
LARGE_FONT = ('Verdana', 16)
NORMAL_FONT = ('Verdana', 12)
style.use('ggplot')


filename = "NYPD_Motor_Vehicle_Collisions.csv"
df = pd.read_csv(filename)
df_1 = df.replace(['Unspecified'], np.nan)
plots = Plots(df_1)

"""
Heatmap of geolocated collisions in New York City area of a selected year. 
This map only plot data with location information, i.e. latitude and longitude. 
Data without location will be ignored.

Baesd on tweets heatmap by Kelsey Jordahl, Enthought in Scipy 2013 geospatial tutorial. 
See more in github page: https://github.com/kjordahl/SciPy2013.

"""

from matplotlib import cm
from AccidentAnalysis import *
from mpl_toolkits.basemap import Basemap
# You should have installed mpl_toolkits.basemap first. If not, try conda install basemap
# or use anaconda prompt 'conda install -c conda-forge basemap-data-hires=1.0.8.dev0'

def heatmap(df,year):
    """
    The function turns input dataframe into heatmap. Input should contain feature
    'LATITUDE' and 'LONGITUDE', otherwise it will not be plotted.
    """
    df = AccidentAnalysis(df).select_year(year)
    
    west, south, east, north = -74.26, 40.50, -73.70, 40.92 # location of NYC
    a = np.array(df['LATITUDE'].dropna())
    b = np.array(df['LONGITUDE'].dropna())
    N = len(a)
    
    fig = plt.figure()
    m = Basemap(projection='merc', llcrnrlat=south, urcrnrlat=north,
                llcrnrlon=west, urcrnrlon=east, lat_ts=south, resolution='i')
    x, y = m(b, a)
    m.hexbin(x, y, gridsize=400, bins='log', cmap=cm.YlOrRd_r)
    plt.title("NYPD Collisions heatmap")
    plt.show()


class AccidentTrackerApp(tk.Tk):

	''' the baseline to build the framework '''

	def __init__(self, *args, **kwargs):
		# *args: you can pass as many as parameters as you want
		# **kwargs: pass dictionary, usually.
		tk.Tk.__init__(self, *args, **kwargs)
		'''initialize the tkinter'''
		
		tk.Tk.wm_title(self, "Accident Tracker")
		''' Change the title of the GUI '''

		container = tk.Frame(self)
		'''make a frame for the GUI'''

		container.pack(side='top', fill = 'both', expand = True)

		container.grid_rowconfigure(0, weight = 1)
		# 0 is minimun size
		container.grid_columnconfigure(0, weight = 1)



		self.frames = {}
		''' the container for all the pages '''

		for page in (Navigation, StartPage, Overview, CasualtyPage, SortPage):
			
			frame = page(container, self)

			self.frames[page] = frame
			frame.grid(row=0, column=0, sticky='nsew')
			'''  "nsew" = "north south east west" --- alignment definition 
			Streth everything to the edge of the window.'''

		self.show_frame(Navigation)


	def show_frame(self, cont):
		# cont, controller, is a key
		'''   function to show a page afront  '''

		frame = self.frames[cont]
			# corresponding to the self.frames in the constructor
		frame.tkraise()
		''' inherited from tk.TK. Used to raise the page to the front '''


class Navigation(tk.Frame):
	''' to add a page, inherit from tk.Frame '''
	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		label1 = tk.Label(self, text = "Welcome", font = EXTRA_LARGE_FONT)
		label1.pack(padx=10, pady=10)

		'''loading data'''
		button = tk.Button(self, text = "Let's Start", 
			command = lambda: controller.show_frame(StartPage), 
			padx=24, pady=9, fg="red")
		button.pack()

		''' navigating button '''

		label2 = tk.Label(self, text = "Click Button to Continue", font = LARGE_FONT, fg='blue')
		label2.pack(padx=10, pady=10)


class StartPage(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text = "Home Page", font = EXTRA_LARGE_FONT, fg = 'red', bg='yellow')
		label.pack(padx=10, pady=10)
		button1 = tk.Button(self,text='Overview Information', 
			command = lambda: controller.show_frame(Overview), padx=24, pady=9)
		button1.pack()
		button2 = tk.Button(self,text='Casualty Analysis', 
			command = lambda: controller.show_frame(CasualtyPage), padx=24, pady=9)
		button2.pack()
		button3 = tk.Button(self,text='Sorting', 
			command = lambda: controller.show_frame(SortPage), padx=24, pady=9)
		button3.pack()

		button4 = tk.Button(self,text='Exit', 
			command = quit, padx=24, pady=9)
		button4.pack(side="bottom")


class Overview(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		label1 = tk.Label(self, text = "Overview", font = EXTRA_LARGE_FONT, fg="red", bg="yellow")
		label1.pack(padx=10, pady=10)
		
		'''Collision Counts from 2012 to 2016'''
		label2 = tk.Label(self, text = "Collision Counts from 2012 to 2016", font = LARGE_FONT, fg="red")
		label2.pack(padx=10, pady=10)

		label3 = tk.Label(self, text = "Choose a Borough", font = LARGE_FONT)
		label3.pack()

		var1 = StringVar(self)
		var1.set("ALL") # default value

		''' dropdown menu to choose the value '''
		boro_opt_1 = OptionMenu(self, var1, "ALL", "MANHATTAN", "BROOKLYN", "QUEENS", "BRONX", "STATEN ISLAND")
		boro_opt_1.pack()
	
		'''get the value user chose as the input and plot '''
		def ok_1(boro):
			''' show the plot '''
			if boro == "ALL":
				plots.plot_lines_total()
			else:
				plots.plot_year_total(boro)


		button1 = Button(self, text="OK", command=lambda: ok_1(var1.get()), padx=16, pady=9, fg="red")
		button1.pack()


		'''Collision Percentage for All Boroughs'''
		label2 = tk.Label(self, text = "Collision Percentage for All Boroughs", font = LARGE_FONT, fg="red")
		label2.pack(padx=10, pady=10)

		label3 = tk.Label(self, text = "Choose a Year", font = LARGE_FONT)
		label3.pack()

		var4 = StringVar(self)
		var4.set("ALL") # default value

		''' dropdown menu to choose the value '''
		year_opt_1 = OptionMenu(self, var4, "ALL", "2012", "2013", "2014", "2015", "2016")
		year_opt_1.pack()

		def ok_2(year):
			if year == "ALL":
				plots.plot_pie_total()
			else:
				plots.plot_pie_year(year)
			
		button1 = Button(self, text="OK", command=lambda: ok_2(var4.get()), padx=16, pady=9, fg="red")
		button1.pack()		


		'''Heat Map'''
		label4 = tk.Label(self, text = "Heat Map", font = LARGE_FONT, fg="red")
		label4.pack(padx=10, pady=10)


		label6 = tk.Label(self, text = "Choose a Year", font = LARGE_FONT)
		label6.pack()

		var100 = StringVar(self)
		var100.set("2012") # default value

		''' dropdown menu to choose the value '''
		boro_opt = OptionMenu(self, var100, "2012", "2013", "2014", "2015", "2016")
		boro_opt.pack()

		'''get the value user chose as the input and plot '''
		# def ok_3(df, year):
		# 	''' show the plot '''
		# 	heatmap(df, year)

		button2 = Button(self, text="OK", command=lambda: heatmap(df, var100.get()), padx=16, pady=9, fg="red")
		button2.pack()

		# button1 = tk.Button(self,text='Go to Page 1', 
		# 	command = lambda: controller.show_frame(PageOne))
		# button1.pack()
		button3 = tk.Button(self,text='Back to Home', 
			command = lambda: controller.show_frame(StartPage))
		button3.pack(side="bottom", fill='x', pady=10)

class CasualtyPage(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		label1 = tk.Label(self, text = "Casualty Analysis", font = EXTRA_LARGE_FONT, fg="red", bg="yellow")
		label1.pack(padx=10, pady=10)


		label2 = tk.Label(self, text = "Choose a Borough", font = LARGE_FONT)
		label2.pack()

		var5 = StringVar(self)
		var5.set("MANHATTAN") # default value

		''' dropdown menu to choose the value '''
		boro_opt = OptionMenu(self, var5, "MANHATTAN", "BROOKLYN", "QUEENS", "BRONX", "STATEN ISLAND")
		boro_opt.pack()


		label4 = tk.Label(self, text = "Casualty", font = LARGE_FONT)
		label4.pack()

		var7 = StringVar(self)
		var7.set("Injured") # default value

		''' dropdown menu to choose the value '''
		boro_opt = OptionMenu(self, var7, "Injured", "Dead")
		boro_opt.pack()
	
	
		'''get the value user chose as the input and plot '''
		def ok_4(boro, casualty):
			if casualty == 'Injured':
				plots.plot_year_injured(boro)
			else:
				plots.plot_year_killed(boro)


		button1 = Button(self, text="OK", command=lambda: ok_4(var5.get(), var7.get()),padx=16, pady=9, fg="red")
		button1.pack()

		button3 = tk.Button(self,text='Back to Home', 
			command = lambda: controller.show_frame(StartPage))
		button3.pack(side="bottom", fill='x', pady=10)


class SortPage(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		label1 = tk.Label(self, text = "Sorting", font = EXTRA_LARGE_FONT, fg="red", bg="yellow")
		label1.pack(padx=10, pady=10)


		label2 = tk.Label(self, text = "Choose a Borough", font = LARGE_FONT)
		label2.pack()

		var8 = StringVar(self)
		var8.set("ALL") # default value

		''' dropdown menu to choose the value '''
		boro_opt = OptionMenu(self, var8, "ALL", "MANHATTAN", "BROOKLYN", "QUEENS", "BRONX", "STATEN ISLAND")
		boro_opt.pack()

		label3 = tk.Label(self, text = "Choose a Year", font = LARGE_FONT)
		label3.pack()

		var9 = StringVar(self)
		var9.set("2012") # default value

		''' dropdown menu to choose the value '''
		boro_opt = OptionMenu(self, var9, "2012", "2013", "2014", "2015", "2016")
		boro_opt.pack()

		label4 = tk.Label(self, text = "Sorted by", font = LARGE_FONT)
		label4.pack()

		var10 = StringVar(self)
		var10.set("Zip Code") # default value

		''' dropdown menu to choose the value '''
		boro_opt = OptionMenu(self, var10, "Zip Code", "Reason", "Vehicle Type")
		boro_opt.pack()
	
	
		'''get the value user chose as the input and plot '''
		def ok_5(boro, year, sortby):
			''' show the plot '''
			if sortby == 'Zip Code':
				if boro == 'ALL':
					plots.plot_zip_total(year)
				else:
					plots.plot_zip_borough(year, boro)
			elif sortby == 'Reason':
				if boro == 'ALL':
					plots.plot_reasons_total(year)
				else:
					plots.plot_reasons_borough(year, boro)
			else:
				if boro == "ALL":
					plots.plot_types_total(year)
				else:
					plots.plot_types_borough(year, boro)


		button1 = Button(self, text="OK", command=lambda: ok_5(var8.get(), var9.get(), var10.get()), padx=16, pady=9, fg="red")
		button1.pack()

		button3 = tk.Button(self,text='Back to Home', 
			command = lambda: controller.show_frame(StartPage))
		button3.pack(side="bottom", fill='x', pady=10)

app = AccidentTrackerApp()
app.geometry("480x560")
app.mainloop()




if __name__ == '__main__':
    pass

