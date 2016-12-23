'''
Created on Dec 15, 2016

@author: sj238
'''
from matplotlib import pyplot as plt
import seaborn as sns

class nvn_graph(object):
    '''
    This is the class for visulization methods of numerical feature vs. another numerical feature
    '''


    def __init__(self, data, attr1, attr2):
        '''
        Constructor
        '''
        self.df = data
        self.attr1 = attr1
        self.attr2 = attr2
    
    def joint_plot(self):
        '''
        get the dataframe and desired attributions.
        Return
        ======
        return jointplot of attributions 
        '''
        sns.jointplot(x=self.attr1, y=self.attr2, data=self.df)
        plt.savefig('graphs/'+'Jointplot of ' + str(self.attr1) + ' and ' + str(self.attr2) + '.pdf', format='pdf')
        plt.show()
        