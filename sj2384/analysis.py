'''
Created on Dec 15, 2016

@author: sj238
'''
import sys
from Exception_list import *
from num_graph import *
from cat_graph import *
from nvc_graph import *
from GBT_model import *
from nvn_graph import *


def num_analysis(df):
    """
    get the option selected by user, and verify it.
    Return
    ======
    return the result if the option is verified
    """
    num_option = df.select_dtypes(exclude=['object']).columns.values
    print(num_option)
    key = input('Please select one feature of above you are interested in, or enter q to quit:')
    if key == 'q':
        print ('program shut down! bye!')
        sys.exit()
    if not(key in num_option):
        raise wrong_option_exception
    if key in num_option:
        num_graphs = num_graph(df,key)
        num_graphs.distribution()
        num_graphs.density()
        
        

def cat_analysis(df):
    """
    get the option selected by user, and verify it.
    Return
    ======
    return the result if the option is verified
    """
    cat_option = df.select_dtypes(include=['object']).columns.values
    print(cat_option)
    key = input('Please select one feature of above you are interested in, or enter q to quit:')
    if key == 'q':
        print ('program shut down! bye!')
        sys.exit()
    if not(key in cat_option):
        raise wrong_option_exception
    if key in cat_option:
        cat_graphs = cat_graph(df,key)
        cat_graphs.make_pie()
        cat_graphs.make_bar()

def nvc_analysis(df):
    """
    get the option selected by user, and verify it.
    Return
    ======
    return the result if the option is verified
    """
    cat_option = df.select_dtypes(include=['object']).columns.values
    num_option = df.select_dtypes(exclude=['object']).columns.values
    print(cat_option)
    cat_key = input('Please select one categorical feature of above you are interested in, or enter q to quit:')
    if cat_key == 'q':
        print ('program shut down! bye!')
        sys.exit()
    if not(cat_key in cat_option):
        raise wrong_option_exception
    print(num_option)
    num_key = input('Please select one numerical feature of above you are interested in, or enter q to quit:')
    if num_key == 'q':
        print ('program shut down! bye!')
        sys.exit()
    if not(num_key in num_option):
        raise wrong_option_exception
    if (cat_key in cat_option) and (num_key in num_option):
        nvc_graphs = nvc_graph(df,cat_key, num_key)
        nvc_graphs.box_plot()
        
def gbt_analysis(df):
    """
    get the option selected by user, and verify it.
    Return
    ======
    return the result if the option is verified
    """
    print('Our major concern would be the interest rate when we borrow money, so we want to know what features will affect interest rate.')
    print('We dropped some features that are more likely post loan attributes not only for the sake of time but also for avoiding leakage.')
    print('')
    print('')
    key = input('Please chose the the number of most important features, no more than 10, you want to learn or enter q to quit:')
    if str(key) == 'q':
        print ('program shut down! bye!')
        sys.exit()
    if not int(key) in np.arange(1,11):
        raise wrong_option_exception
    if int(key) in np.arange(1,11):
        result = GBT_model(df,key)
        result.gbt_model()
        result.gbt_feat_importance()
        result.cust_feat_importance()
        result.partial_dep()

def nvn_analysis(df):
    """
    get the option selected by user, and verify it.
    Return
    ======
    return the result if the option is verified
    """
    num_option = df.select_dtypes(exclude=['object']).columns.values
    print(num_option)
    key1 = input('Please select one feature from above or enter q to quit:')
    if key1 == 'q':
        print ('program shut down! bye!')
        sys.exit()
    if not(key1 in num_option):
        raise wrong_option_exception
    key2 = input('Please select another feature from above or enter q to quit:')
    if key2 == 'q':
        print ('program shut down! bye!')
        sys.exit()
    if not(key2 in num_option):
        raise wrong_option_exception
    if key1 == key2:
        print('Please do not choose the feature that has been chosen previously')
        raise wrong_option_exception
    
    if (key1 in num_option) and (key2 in num_option) and (key1 != key2):
        nvn_graphs = nvn_graph(df,key1,key2)
        nvn_graphs.joint_plot()
        
        
    
    