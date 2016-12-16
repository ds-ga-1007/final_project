'''
Module for plot Heatmaps.

When the method is called, it will plot the number of infected people, measured over 70-somes years and
across all states. In some cases, several picked states are removed since the missing data. 

Generally the plot will show a distinctive declined density after vaccines were introduced.
'''


import get_heatmap_matrix
from get_heatmap_matrix import heatmap_disease_matrix
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
from matplotlib.colors import ListedColormap
import matplotlib.pylab as pylab
import warnings
warnings.filterwarnings('ignore')

plt.style.use('fivethirtyeight')

def heatmap_Measles():
    Measles = heatmap_disease_matrix('Measles') 
    Measles = Measles.loc[1928:] #drop rows before 1928 for measles, since missing data
    Measles = Measles.drop(['GUAM','PAC TRUST TERR','AMERICAN SAMOA','NORTHERN MARIANA ISLANDS'],axis=1) #drop those states with no recording numbers
    
    fig, ax = plt.subplots(figsize=(15,15)) 
    flatui = ['#ecf0f1', '#bdc3c7','#95a5a6', '#7f8c8d','#f1c40f','#f39c12','#d35400','#e74c3c']
    sns.set_palette(flatui)
    my_cmap = ListedColormap(flatui)

    sns.set(font_scale=1.2)
    sns.set_style({"savefig.dpi": 100}) 
    ax = sns.heatmap(Measles.T, 
                     linewidths=.20,
                     cmap=my_cmap,
                     ax=ax,
                     vmin=0, 
                     vmax=3000,
                     xticklabels = 5 )
    ax.set_title('Measles',fontsize=18, fontweight='bold') 
    ax.axvline(x=36,color='k',linewidth=2.5) 
    ax.text(36,0.1,' Vaccine introduced', fontsize=10,fontweight='bold')
    plt.yticks(rotation ='horizontal')
    fig.tight_layout()
    fig.savefig('Heatmap of Measles.pdf')
    
def heatmap_Hepatitis_A():
    Hepatitis_A = heatmap_disease_matrix('Hepatitis A') 
    Hepatitis_A = Hepatitis_A.drop(['GUAM','PAC TRUST TERR','AMERICAN SAMOA','NORTHERN MARIANA ISLANDS'],axis=1)
    
    fig, ax = plt.subplots(figsize=(15,15)) 

    flatui = ['#ecf0f1', '#bdc3c7','#95a5a6', '#7f8c8d','#f1c40f','#f39c12','#d35400','#e74c3c']
    sns.set_palette(flatui)
    my_cmap = ListedColormap(flatui)

    sns.set(font_scale=1.2)
    sns.set_style({"savefig.dpi": 500}) 
    ax = sns.heatmap(Hepatitis_A.T,
                     linewidths=.20,
                     cmap=my_cmap,
                     ax=ax,
                     vmin=0, 
                     vmax=500,
                     xticklabels = 5 )

    ax.set_title('Hepatitis A',fontsize=18, fontweight='bold') 
    ax.axvline(x=22,color='k',linewidth=2.5) 
    ax.text(22,0.5,' Vaccine introduced', fontsize=10,fontweight='bold')
    plt.yticks(rotation ='horizontal')
    fig.tight_layout()
    fig.savefig('Heatmap of Hepatitis_A.pdf')
    
def heatmap_Mumps():
    Mumps = heatmap_disease_matrix('Mumps') 
    
    fig, ax = plt.subplots(figsize=(15,15)) 
    flatui = ['#ecf0f1', '#bdc3c7','#95a5a6', '#7f8c8d','#f1c40f','#f39c12','#d35400','#e74c3c']
    sns.set_palette(flatui)
    my_cmap = ListedColormap(flatui)

    sns.set(font_scale=1.2)
    sns.set_style({"savefig.dpi": 500}) 
    ax = sns.heatmap(Mumps.T,
                     linewidths=.20,
                     cmap=my_cmap,
                     ax=ax,
                     vmin=0, 
                     vmax=2500,
                     xticklabels = 5 )

    ax.set_title('Mumps',fontsize=18, fontweight='bold') 
    ax.axvline(x=10,color='k',linewidth=3)  
    ax.text(10.3,0.5,' Vaccine introduced', fontsize=10,fontweight='bold')
    plt.yticks(rotation ='horizontal')
    fig.tight_layout()
    fig.savefig('Heatmap of Mumps.pdf')
    
def heatmap_Rubella():
    Rubella = heatmap_disease_matrix('Rubella') 
    Rubella = Rubella.drop(['GUAM','PAC TRUST TERR','AMERICAN SAMOA'],axis=1)
    
    fig, ax = plt.subplots(figsize=(15,15)) 

    flatui = ['#ecf0f1', '#bdc3c7','#95a5a6', '#7f8c8d','#f1c40f','#f39c12','#d35400','#e74c3c']
    sns.set_palette(flatui)
    my_cmap = ListedColormap(flatui)

    sns.set(font_scale=1.2)
    sns.set_style({"savefig.dpi": 500}) 
    ax = sns.heatmap(Rubella.T,
                     linewidths=.20,
                     cmap=my_cmap,
                     ax=ax,
                     vmin=0, 
                     vmax=1500,
                     xticklabels = 5 )

    ax.set_title('Rubella',fontsize=18, fontweight='bold') 
    ax.axvline(x=4,color='k',linewidth=3)  
    ax.text(4,0.3,' Vaccine introduced', fontsize=10,fontweight='bold')
    plt.yticks(rotation ='horizontal')
    fig.tight_layout()
    fig.savefig('Heatmap of Rubella.pdf')
    
def heatmap_Poliomyelitis():
    Poliomyelitis = heatmap_disease_matrix('Poliomyelitis') 
    Poliomyelitis = Poliomyelitis.drop(Poliomyelitis.index[[0,1,2,3,4,5]]) 
    
    fig, ax = plt.subplots(figsize=(15,15)) 

    flatui = ['#ecf0f1', '#bdc3c7','#95a5a6', '#7f8c8d','#f1c40f','#f39c12','#d35400','#e74c3c']
    sns.set_palette(flatui)
    my_cmap = ListedColormap(flatui)

    sns.set(font_scale=1.2)
    sns.set_style({"savefig.dpi": 500}) 
    ax = sns.heatmap(Poliomyelitis.T,
                     linewidths=.20,
                     cmap=my_cmap,
                     ax=ax,
                     vmin=0, 
                     vmax=500,
                     xticklabels = 5 )

    ax.set_title('Poliomyelitis',fontsize=18, fontweight='bold') 
    ax.axvline(x=29,color='k',linewidth=3)  
    ax.text(29,2.3,' Vaccine introduced', fontsize=10,fontweight='bold')
    plt.yticks(rotation ='horizontal')
    fig.tight_layout()
    fig.savefig('Heatmap of Poliomyelitis.pdf')

def heatmap_Smallpox():
    Smallpox = heatmap_disease_matrix('Smallpox') 
    Smallpox = Smallpox.drop(Smallpox.index[list(range(27))])
    
    fig, ax = plt.subplots(figsize=(15,15)) 

    flatui = ['#ecf0f1', '#bdc3c7','#95a5a6', '#7f8c8d','#f1c40f','#f39c12','#d35400','#e74c3c']
    sns.set_palette(flatui)
    my_cmap = ListedColormap(flatui)

    sns.set(font_scale=1.2)
    sns.set_style({"savefig.dpi": 500}) 
    ax = sns.heatmap(Smallpox.T,
                     linewidths=.20,
                     cmap=my_cmap,
                     ax=ax,
                     vmin=0, 
                     vmax=500,
                     xticklabels = 2 )

    ax.set_title('Smallpox',fontsize=18, fontweight='bold') 
    ax.axvline(x=12,color='k',linewidth=3)  
    ax.text(12,0.3,' Vaccine introduced', fontsize=10,fontweight='bold')
    plt.yticks(rotation ='horizontal')
    fig.tight_layout()
    fig.savefig('Heatmap of Smallpox.pdf')