'''
Created on Dec 15, 2016

@author: sj238
'''
import matplotlib.pyplot as plt
import numpy as np

class cat_graph(object):
    '''
    classdocs
    '''


    def __init__(self, data, attr):
        '''
        Constructor
        '''
        self.df = data
        self.attr = attr
    
    def make_bar(self):
        heights = self.df[self.attr].value_counts().tolist()
        names = []
        for k, v in self.df[self.attr].value_counts().items():
            names.append(k)
        
        for ii, height in enumerate(heights):
            color = np.random.random_sample(3)
            plt.bar(ii, height, color=color)
            
        plt.title(self.attr)
        plt.ylabel('loans')
        plt.gca().set_xticklabels(names)
        plt.gca().set_xticks(np.arange(len(names)) + .9)
        if len(names) > 5:
            plt.xticks(rotation=90)
        plt.savefig('graphs/'+'Barplot of ' + str(self.attr) + '.pdf', format='pdf')
        plt.show()
        
    def make_pie(self):
        self.df[self.attr].value_counts().plot.pie(autopct='%1.0f%%',figsize=(10,10))
        plt.title(self.attr)
        plt.savefig('graphs/'+'Piechart of ' + str(self.attr) + '.pdf', format='pdf')
        plt.show()