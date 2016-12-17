'''
Created on Dec 12, 2016

@author: felix
'''

import statsmodels.formula.api as smf
import numpy as np
import pandas
import matplotlib.pyplot as plt
# http://statsmodels.sourceforge.net/stable/example_formulas.html

class Correlation:
    '''
    Creates a class for correlations based on a dataframe
    The first column will be treated as outcome and others predictors
    '''
    def get_str(self):
        df = self.data
        outcome = df.dtypes.index[0]
        predictors = df.dtypes.index[1:]

        predictors_str = ''
        for str1 in predictors:
            predictors_str = predictors_str + str1 + ' * '
        predictors_str = predictors_str[0:-3]

        formula_str = outcome + ' ~ ' + predictors_str
        return formula_str
    
    def __init__(self, df):
        self.data = df
        self.formula = self.get_str() 
        self.model = smf.ols(formula = self.formula, data=df, missing='drop')
        self.result = self.model.fit()
        self.summary = self.result.summary()
        
        if len(self.data.columns) == 2:
            def plot(self):
                pass
    
    def save_summary(self):
        filename ='./Results/' + self.formula + '.txt'
        filename = filename.replace("*", "")
        result_file = open(filename, 'w')
        print(self.summary, file=result_file)
        print('Results saved.')
        result_file.close()
        
    def plot_regression(self):
        y = list(self.data.ix[:,0])
        x = list(self.data.ix[:,1])
        max_x = max(x) + 0.05 * (max(x) - min(x))
        min_x = min(x) - 0.05 * (max(x) - min(x))
        x_line = np.linspace(min_x,max_x,100)
        y_line = self.result.params[0] + self.result.params[1] * x_line
        
        fig = plt.figure(figsize=(8, 6))
        plt.scatter(x,y)
        plt.plot(x_line,y_line, color = 'red')
        
        plt.xlabel(list(self.data.columns)[1])
        plt.ylabel('Income')
        
        this_filename ='./Results/Plots/' + self.formula + '.pdf'
        this_filename = this_filename.replace("*", "")
        
        plt.savefig(this_filename)
        print(this_filename[10:] + ' saved.')
        plt.show()
        plt.close()