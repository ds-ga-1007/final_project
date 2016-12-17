"""
This is module tests the methods for company_level class in class_collections_ranking
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
		self.company = company_level(self.merged_data)	
		pass

   # test company_level class
	def test_company_application_pool(self):

		self.assertEqual(self.company.company_application_pool(self.company, "ACCENTURE LLP"), 33496)
		self.assertEqual(self.company.company_application_pool(self.company, "MICROSOFT CORPORATION"), 28618)
		

	def test_company_approve_rate(self):

		self.assertGreater(self.company.company_approval_rate(self.company, "ACCENTURE LLP"),0.98)
		self.assertLess(self.company.company_approval_rate(self.company, "ACCENTURE LLP"),1)
		
		self.assertGreater(self.company.company_approval_rate(self.company, "MICROSOFT CORPORATION"),0.87)
		self.assertLess(self.company.company_approval_rate(self.company, "MICROSOFT CORPORATION"),1)

	def test_company_average_wage(self):

		self.assertGreater(self.company.company_average_wage(self.company, "ACCENTURE LLP"),73757)
		self.assertGreater(self.company.company_average_wage(self.company, "MICROSOFT CORPORATION"),92574)
if __name__ == '__main__':

	unittest.main()
