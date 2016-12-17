'''
Created on Dec 11, 2016

@author: peimengsui
@desc: this is for testing code for ds ga 1007 final project
'''
import unittest
from yeartool import *
from ClubTool import *
from PositionTool import *

dataset = pd.read_csv("finaldata.csv")
data_interested = dataset[dataset['position'] == 'Forward']
class Test(unittest.TestCase):
    def test_yeartool_constructor(self):
        self.assertEqual(yeartool(2014,dataset).year,2014)
    def test_club_investment_max_player(self):
    	self.assertEqual(ClubTool.club_investment_max_player("Arsenal FC", 2015,dataset)["age"],23) 
    	self.assertEqual(ClubTool.club_investment_max_player("Arsenal FC", 2015,dataset)["assists"],1) 
    	self.assertEqual(ClubTool.club_investment_max_player("Arsenal FC", 2015,dataset)["goals"],3) 
    	self.assertEqual(ClubTool.club_investment_max_player("Arsenal FC", 2015,dataset)["matches"],6)   
    def testPositionNumTran(self):
        self.assertTrue(all(map(lambda x: len(x) == 3, PositionTool.num_transfer(data_interested, 'Forward', 'n')))) 

    def testPositionIOR(self):
        self.assertTrue(all(map(lambda x: len(x) == 3, PositionTool.invest_on_return(data_interested, 'Forward', 'n'))))     
if __name__ == "__main__":
    unittest.main()