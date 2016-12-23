'''
Created on Dec 15, 2016

@author: sj238
'''
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


class num_graph(object):
    '''
    This is the class for visulization methods of numerical features 
    '''


    def __init__(self, data, attr):
        '''
        Constructor
        '''
        self.df = data
        self.attr = attr
        
    def distribution(self):
        '''
        get the dataframe and desired attribution.
        Return
        ======
        return distribution chart of that attribution 
        '''
        plt.hist(self.df[self.attr], bins=20)
        plt.title('Distribution of '+ str(self.attr))
        plt.xlabel(self.attr)
        plt.savefig('graphs/'+'Distribution of ' + str(self.attr) + '.pdf', format='pdf')
        plt.show()
        
    def density(self):
        '''
        get the dataframe and desired attribution.
        Return
        ======
        return density chart of that attribution 
        '''
        sns.set_style("whitegrid")
        ax=sns.distplot(self.df[self.attr], color="r")
        ax.set(xlabel=self.attr +' %', ylabel='% Distribution',title='Density Plot of' + str(self.attr))
        warnings.simplefilter('default')
        plt.savefig('graphs/'+'Density of ' + str(self.attr) + '.pdf', format='pdf')
        plt.show()
        
    
        
  
        
