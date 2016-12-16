from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import shapefile
from ipywidgets import interact
from matplotlib.collections import LineCollection
from matplotlib import cm,colors
import matplotlib as mpl
import get_heatmap_matrix as mt
import pandas as pd
from object_class import *

disease_list=pd.read_csv('disease_list.csv')
disease_list=[i for i in disease_list.iloc[:,1]]
r = shapefile.Reader("USA_adm1.shp")
shapes = r.shapes()
records = r.records()
state=[i[4] for i in records]

def get_std_data_by_year(year,disease):
    data=mt.heatmap_disease_matrix(disease).ix[year]
    num_records=[data[i.upper()] if i.upper() in data.index else 0 for i in state] # to keep in the form of 
    max_num=np.max(num_records)
    std_num_records=[i/max_num if max_num!=0 else 0 for i in num_records] 
    return std_num_records #so define a exception class here.

def detect_year(input_year,disease):
    data=mt.heatmap_disease_matrix(disease)
    if input_year in data.index:
        return True
    else: return False

def plot_map(year,disease,color_parameter,std_num_records):
    mpl.rcParams['font.size'] = 10.
    mpl.rcParams['font.family'] = 'Comic Sans MS'
    mpl.rcParams['axes.labelsize'] = 8.
    mpl.rcParams['xtick.labelsize'] = 6.
    mpl.rcParams['ytick.labelsize'] = 6.
    fig = plt.figure(figsize=(11.7,8.3))
    plt.style.use('fivethirtyeight')
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
    ax = plt.subplot(111)
    m = Basemap(resolution='i',projection='merc', llcrnrlon=-132,llcrnrlat=22,urcrnrlon=-60,urcrnrlat=50)
    m.etopo()
    m.drawcountries()
    for record, shape,num in zip(records,shapes,std_num_records):
        lons,lats = zip(*shape.points)
        data = np.array(m(lons, lats)).T
 
        if len(shape.parts) == 1:
            segs = [data,]
        else:
            segs = []
            for i in range(1,len(shape.parts)):
                index = shape.parts[i-1]
                index2 = shape.parts[i]
                segs.append(data[index:index2])
            segs.append(data[index2:])
 
        lines = LineCollection(segs,antialiaseds=(1,))
        color=colors.hsv_to_rgb((color_parameter,num,1))
        lines.set_facecolor(color)
        lines.set_edgecolors('k')
        lines.set_linewidth(0.1)
        ax.add_collection(lines)
    m.drawstates(linewidth=0.5)
    m.drawcoastlines(linewidth=0.5)
    plt.title('geo-heatmap for {} in {}'.format(disease,year))
    
    plt.savefig('geo-heatmap for {} in {}.pdf'.format(disease,year))