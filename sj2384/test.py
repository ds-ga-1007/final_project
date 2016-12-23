'''
Created on Dec 15, 2016

@author: sj238
'''
import unittest
import pandas as pd
import numpy as np
from load_data import  *
from clean_data import  *


class TestInput(unittest.TestCase):

    def setup(self):
        self.df = pd.read.csv('LoanStats3a.csv')
    def test1(self):
        self.assertRaises(IOError, get_input, 'aaaaaaa')
    def test2(self):
        df = get_input('LoanStats3a.csv')
        self.assertEqual(pd.DataFrame, type(df))

class TestClean(unittest.TestCase):
    def setup(self):
        self.df = pd.read.csv('/LoanStats3a.csv')
    def test1(self):
        df = get_input('LoanStats3a.csv')
        df = Clean_df(df)
        self.assertEqual(np.float64, type(df['int_rate'][1]))
        self.assertEqual(np.float64, type(df['revol_util'][1]))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()