'''
Created on Dec 15, 2016

@author: sj238
'''
from sklearn import ensemble
import pandas as pd
#from sklearn import datasets
from sklearn.utils import shuffle
#from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt
import numpy as np
from sklearn.ensemble.partial_dependence import plot_partial_dependence

class GBT_model(object):
    '''
    
    This is the class for visulization methods of GBT 
    
    '''


    def __init__(self, data, feats):
        '''
        Constructor
        '''
        self.df = data
        self.feats = feats
    #def data_prep(self):
        self.df.drop(['addr_state','installment','purpose'],1, inplace=True)
        self.df = pd.get_dummies(self.df)
        y = self.df.int_rate.values
        self.df.drop('int_rate',axis = 1, inplace=True)
        X, y = shuffle(self.df.values, y, random_state=30)
        X = X.astype(np.float32)
        offset = int(X.shape[0] * 0.75)
        X_train, y_train = X[:offset], y[:offset]
        X_test, y_test = X[offset:], y[offset:]
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
    
    def gbt_model(self):
        '''
        get the dataframe, test and training data
        Return
        ======
        return accuracy of GBT regression
        '''
        gbt = ensemble.GradientBoostingRegressor(n_estimators=100,max_depth=3,
                                                 max_features=0.5,min_samples_leaf=2,learning_rate=0.1)
        gbt.fit(self.X_train, self.y_train)
        print('The accuracy of GBT model is:')
        print(gbt.score(self.X_test,self.y_test))
        self.gbt = gbt
    
    def gbt_feat_importance(self):
        '''
        get the dataframe.
        Return
        ======
        return feature importance chart 
        '''
        fig, ax = plt.subplots()
        width=0.5
        ax.bar(np.arange(len(self.df.columns)), self.gbt.feature_importances_, width, color='r')
        ax.set_xticks(np.arange(len(self.gbt.feature_importances_)))
        ax.set_xticklabels(self.df.columns.values,rotation=90)
        plt.title('Feature Importance from GBT')
        ax.set_ylabel('Normalized Feature Importance')
        plt.savefig('graphs/'+'Feature Importance from GBT.pdf', format='pdf')
        plt.show()
        
    def cust_feat_importance(self):
        '''
        get the dataframe.
        Return
        ======
        return top K features relative importance chart
        '''
        feature_importance = self.gbt.feature_importances_
        feature_importance = 100.0 * (feature_importance / feature_importance.max())

        indices = np.argsort(feature_importance)[-int(self.feats):]
        plt.barh(np.arange(int(self.feats)), feature_importance[indices],color='dodgerblue',alpha=.4)
        plt.yticks(np.arange(int(self.feats) + 0.25), np.array(self.df.columns)[indices])
        plt.xlabel('Relative importance')
        plt.title('Top ' + str(self.feats) + ' Important Variables')
        plt.savefig('graphs/'+'Top ' + str(self.feats) + ' Important Variables.pdf', format='pdf')
        plt.show()
        
    def partial_dep(self):
        '''
        get the dataframe.
        Return
        ======
        return top K features partial dependence chart
        '''

        feature_importance = self.gbt.feature_importances_
        feature_importance = 100.0 * (feature_importance / feature_importance.max())
        indices = np.argsort(feature_importance)[-int(self.feats):]
        comp_features = np.array(self.df.columns)[indices]
        fig, axs = plot_partial_dependence(self.gbt, self.X_train, comp_features, feature_names=list(self.df.columns), 
                                           figsize=(14, 14), n_jobs=-1)
        plt.savefig('graphs/'+'Partial Dependence of ' + str(self.feats) + ' Important Variables.pdf', format='pdf')
        plt.show()