import unittest
from function import *
from clean_data import *
from test_data import *
from information_and_plot import *
from main import *

#Get the complete data 
test_data = pd.read_excel(complete_path)
#Generate a data frame that assume all ACT scores (english, math, writing and cumulative) are 36
test_data_ACT1 = search_ACT_test(test_data,'36','36','36','36','36','36','36','36')
#Generate that all ACT scores (english, math, writing and cumulative) are 0 (no school can be choose in this case)
test_data_ACT2 = search_ACT_test(test_data,'0','0','0','0','0','0','0','0')
#Generate a data frame that assume all SAT scores (reading, math, writing) are 800
test_data_SAT1 = search_SAT_test(test_data,'800','800','800','800','800','800')
#Generate that all ACT scores (reading, math, writing ) are 0 (no school can be choose in this case)
test_data_SAT2 = search_SAT_test(test_data,'0','0','0','0','0','0')



class Test(unittest.TestCase):

    #Test the function justify_SAT_score(score), i.e., whether input the correct SAT score
    #non-integer, negative integer or >800, will return 1
    #otherwise, return 0
    def test_justify_SAT_score(self):
        self.assertEqual(justify_SAT_score('10'),0)
        self.assertEqual(justify_SAT_score('800'),0)
        self.assertEqual(justify_SAT_score('a'),1)
        self.assertEqual(justify_SAT_score('*'),1)
        self.assertEqual(justify_SAT_score('a@$'),1)
        self.assertEqual(justify_SAT_score('8.88'),1)
        self.assertEqual(justify_SAT_score('-1'),1)
        self.assertEqual(justify_SAT_score('801'),1)

    #Test the function justify_ACT_score(score), i.e., whether input the correct ACT score
    #non-integer, negative integer or >36, will return 1
    #otherwise, return 0
    def test_justify_ACT_score(self):
        self.assertEqual(justify_ACT_score('0'),0)
        self.assertEqual(justify_ACT_score('36'),0)
        self.assertEqual(justify_ACT_score('036'),0)
        self.assertEqual(justify_ACT_score('37'),1)
        self.assertEqual(justify_ACT_score('a@$'),1)
        self.assertEqual(justify_ACT_score('8.88'),1)
        self.assertEqual(justify_ACT_score('-1'),1)
        self.assertEqual(justify_ACT_score('c'),1)

    #Test the function search_SAT(data) based on the modified function search_SAT_test(data) in test_data.py
    #Based on test_data_SAT1, should get a data frame
    #Based on test_data_SAT2, should return a designed sentence due to no data
    def test_search_SAT(self):
        self.assertEqual(str(type(test_data_SAT1)),"<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(test_data_SAT2,"There is no available world ranking top 1000 collges available for you, please try next year. Fighting!")
        
    #Test the function search_ACT(data) based on the modified function search_ACT_test(data) in test_data.py
    #Based on test_data_ACT1, should get a data frame
    #Based on test_data_ACT2, should return a designed sentence due to no data
    def test_search_ACT(self):
        self.assertEqual(str(type(test_data_ACT1)),"<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(test_data_ACT2,"There is no available world ranking top 1000 collges available for you, please try next year. Fighting!")

    #Test the functions in the class plot_infor()
    #Test function intro()
    def test_class_intro(self):
        self.assertEqual(str(print(plot_infor(test_data_SAT1,1).intro())),"None")
        self.assertEqual(str(print(plot_infor(test_data_ACT1,2).intro())),"None")
    #Test function crime_plot()
    def test_class_cp(self):
        self.assertEqual(str(type(plot_infor(test_data_SAT1,1).crime_plot())),"<class 'matplotlib.collections.PathCollection'>")
        self.assertEqual(str(type(plot_infor(test_data_ACT1,2).crime_plot())),"<class 'matplotlib.collections.PathCollection'>")
    #Test function WR_NR_plot()
    def test_class_WN(self):
        self.assertEqual(str(type(plot_infor(test_data_SAT1,1).WR_NR_plot())),"<class 'list'>")
        self.assertEqual(str(type(plot_infor(test_data_ACT1,2).WR_NR_plot())),"<class 'list'>")
    #Test function Earning_plot()
    def test_class_ep(self):
        self.assertEqual(str(type(plot_infor(test_data_SAT1,1).Earning_plot())),"<class 'matplotlib.lines.Line2D'>")
        self.assertEqual(str(type(plot_infor(test_data_ACT1,2).Earning_plot())),"<class 'matplotlib.lines.Line2D'>")
    #Test function Age_plot()
    def test_class_ap(self):
        self.assertEqual(str(type(plot_infor(test_data_SAT1,1).Age_plot())),"<class 'tuple'>")
        self.assertEqual(str(type(plot_infor(test_data_ACT1,2).Age_plot())),"<class 'tuple'>")

    #Test the function justify_order() in the main.py
    def test_justify_order(self):
        self.assertEqual(justify_order('1',test_data_SAT1),0)
        self.assertEqual(justify_order('10',test_data_SAT1),0)
        self.assertEqual(justify_order('a1',test_data_SAT1),1)
        self.assertEqual(justify_order('-2',test_data_SAT1),1)
        self.assertEqual(justify_order('0',test_data_SAT1),1)
        self.assertEqual(justify_order('1.11',test_data_SAT1),1)

if __name__ == "__main__":
    unittest.main()
