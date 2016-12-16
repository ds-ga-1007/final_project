"""
This is module tests the methods for indusrty_level class in class_collections_ranking
The whole test will take at around one minute

Created on 2016/12/01
Version: 1.0
@author: yuwei tu
ShengLiu Copyright 2016-2017
"""

from class_collections_ranking import *
import unittest

class utest(unittest.TestCase):
	def setUp(self):
		data = {}
		for year in range(2010,2017):
			data[year]= pd.read_csv('../DataBase/H-1B_FY'+str(year)+'_clean.csv',encoding = 'iso-8859-1')
		self.data = data
		self.merged_data = pd.concat([data[year] for year in range(2010,2017)], ignore_index= True)
		self.industry = industry_level(self.merged_data)

		pass
  
    # test industry_level class
	def test_industry_application_pool(self):

		self.assertEqual(self.industry.industry_application_pool(self.industry, "Computer and Mathematical Occupations"), 2216205)
		self.assertEqual(self.industry.industry_application_pool(self.industry, "Legal Occupations"), 6958)
		self.assertEqual(self.industry.industry_application_pool(self.industry, "Business and Financial Operations Occupations"),200770 )
	
		

	def test_industry_approve_rate(self):

		self.assertGreater(self.industry.industry_approval_rate(self.industry, "Computer and Mathematical Occupations"),0.87)
		self.assertLess(self.industry.industry_approval_rate(self.industry, "Computer and Mathematical Occupations"),1)
		
		self.assertGreater(self.industry.industry_approval_rate(self.industry, "Legal Occupations"),0.82)
		self.assertLess(self.industry.industry_approval_rate(self.industry, "Legal Occupations"),1)
		
		self.assertGreater(self.industry.industry_approval_rate(self.industry, "Business and Financial Operations Occupations"),0.87)
		self.assertLess(self.industry.industry_approval_rate(self.industry, "Business and Financial Operations Occupations"),1)
		
	

	def test_industry_average_wage(self):

		self.assertGreater(self.industry.industry_average_wage(self.industry, "Computer and Mathematical Occupations"),73854)
		self.assertGreater(self.industry.industry_average_wage(self.industry, "Legal Occupations"),81179)
		self.assertGreater(self.industry.industry_average_wage(self.industry, "Business and Financial Operations Occupations"),65750)
if __name__ == '__main__':

	unittest.main()
  