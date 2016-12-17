'''
Created on  Nov 20th 2016
@Project Name:World bank data explorer
@Author:Liwei Song, Zoe Ma, Yichao Chen
'''

from class_function import *
from country_input import *
from year_input import *
from feature_input import *
from db_input import *
import unittest


'''
This module is for testing classes and functions
plot class is hard to test. We test them by looking at the output figures
'''

class Test(unittest.TestCase):
    #test sub_input function
    def test_subinput(self):
        ls2=[]
        self.assertEqual(sub_input(ls2),1 )
        print('interval function is good')
    #test country_input is correct or not
    def test_country(self):
        country1='[USA]'
        country2='[CHN]'
        country3='[USA,CHN]'
        country4='[USA)'
        country5='[US'
        country6='[AFG,ALB,DOM,CHN,EAS]'
        country7='SB'
        self.assertEqual(country_interval(country1).names,['USA'])
        self.assertEqual(country_interval(country2).names,['CHN'])
        self.assertEqual(country_interval(country3).names,['USA','CHN'])
        self.assertEqual(country_interval(country6).names,['AFG','ALB','DOM','CHN','EAS'])
        with self.assertRaises(CountryError):
             country_interval(country4)
        with self.assertRaises(CountryError):
             country_interval(country5)
        with self.assertRaises(CountryError):
             country_interval(country7)
    #test year input is correct or not
    def test_year(self):
        y1='(1,2)'
        y2='[1992,1995]'
        y3='(1990,2000]'
        y4='[1987,1989]'
        y5='[hjbg,hjjk]'
        y6='svbgkokihji'
        y7='[1992,2016]'
        self.assertEqual(year_interval(y2).names,['1992','1995'])
        self.assertEqual(year_interval(y7).names,['1992','2016'])
        with self.assertRaises(YearError):
             year_interval(y1)
        with self.assertRaises(YearError):
             year_interval(y3)
        with self.assertRaises(YearError):
             year_interval(y4)
        with self.assertRaises(YearError):
             year_interval(y5)
        with self.assertRaises(YearError):
             year_interval(y6)
    #test feature input is correct or not
    def test_feature(self):
        f1='[core_cpi_n,core_cpi_s,cpi_growth_n]'
        f2='[credit_card_f,credit_card_m,debit_card_f,debit_card_m]'
        f3=['giuh']
        f4='(bkjbghk])'
        f5='core_cpi_n', 'core_cpi_s', 'cpi_growth_n'
        f6='(bgbhnhiihni,core_cpi_s]'
        self.assertEqual(feature_interval(f1).names,['core_cpi_n', 'core_cpi_s', 'cpi_growth_n'])
        self.assertEqual(feature_interval(f2).names,['credit_card_f', 'credit_card_m', 'debit_card_f', 'debit_card_m'])
        with self.assertRaises(FeatureError):
            feature_interval(f3)
        with self.assertRaises(FeatureError):
            feature_interval(f4)
        with self.assertRaises(FeatureError):
            feature_interval(f5)
        with self.assertRaises(FeatureError):
            feature_interval(f6)
        
    
        
        
        
        
    


if __name__ == '__main__':
    unittest.main()
        