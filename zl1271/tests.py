'''
Created on Dec 13, 2016

@author: felix
'''
import unittest
from main_funcs import *

class Test(unittest.TestCase):


    def test_valid_input(self):
        corr_list = ['all', 'quit', 'ALL', ' quit']
        for this_str in corr_list:
            self.assertEqual(valid_input(this_str), True)

        wrong_list = ['dfksdaf','123','lalala','$%^&*(']
        for this_str in wrong_list:
            self.assertEqual(valid_input(this_str), False)

    def test_clean_str(self):
        list = ['Quit ', 'q uiT' , ' quit']
        for this_str in list:
            self.assertEqual(clean_str(this_str), 'quit')
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_valid_input']
    unittest.main()