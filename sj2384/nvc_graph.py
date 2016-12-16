'''
Created on Dec 15, 2016

@author: sj238
'''
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


class nvc_graph(object):
    '''
    This is the class for visulization methods of categorical feature vs. numerical feature 
    '''
    def __init__(self, data, cat_attr, num_attr):
        '''
        Constructor
        '''
        self.df = data
        self.cat_attr = cat_attr
        self.num_attr = num_attr
    def box_plot(self):
        '''
        get the dataframe and desired attributions.
        Return
        ======
        return boxplot of attributions 
        '''
        ax = sns.boxplot(x=self.cat_attr, y=self.num_attr, data=self.df)
        plt.xticks(rotation=90)
        plt.savefig('graphs/'+'Boxplot of ' + str(self.cat_attr) + ' and ' + str(self.cat_attr) + '.pdf', format='pdf')
        plt.show()
        