'''
Created on Dec 11, 2016

@author: peimengsui
@desc: this is for testing code for ds ga 1007 final project
'''
import unittest
from yeartool import *

dataset = pd.read_csv("finaldata.csv")
class Test(unittest.TestCase):
    def test_yeartool_constructor(self):
        self.assertEqual(yeartool(2014,dataset).year,2014)
        
if __name__ == "__main__":
    unittest.main()