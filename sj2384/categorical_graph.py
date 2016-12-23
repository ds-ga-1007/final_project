'''
Created on Dec 15, 2016

@author: sj238
'''
import matplotlib.pyplot as plt
import numpy as np
from clean_data import *
from load_data import *

raw_data = safely_input()
df = Clean_df(raw_data)

def make_bar(attr, title, ylabel):
    heights = df[attr].value_counts().tolist()
    names = []
    for k, v in df[attr].value_counts().items():
        names.append(k)
        
    for ii, height in enumerate(heights):
        color = np.random.random_sample(3)
        plt.bar(ii, height, color=color)
        
    plt.title(title)
    plt.ylabel(ylabel)
    plt.gca().set_xticklabels(names)
    plt.gca().set_xticks(np.arange(len(names)) + .9)
    if len(names) > 5:
        plt.xticks(rotation=90)
    plt.savefig('Barplot of ' + str(attr) + '.pdf', format='pdf')
    plt.show()
    

def make_pie(attr,title):
    df[attr].value_counts().plot.pie(autopct='%1.0f%%',figsize=(10,10))
    plt.title(title)
    plt.savefig('Piechart of ' + str(attr) + '.pdf', format='pdf')
    plt.show()
    
                
