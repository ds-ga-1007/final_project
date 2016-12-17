"""
This is module tests the methods for city_level class in class_collections_ranking
The whole test will take at around one minute

Created on 2016/12/01
Version: 1.0
@author: yuwei tu
ShengLiu Copyright 2016-2017
"""


import unittest
import pandas as pd

class utest(unittest.TestCase):
	def setUp(self):
		from class_collections_ranking import city_level
		data = {}
		for year in range(2010,2017):
			data[year]= pd.read_csv('../DataBase/H-1B_FY'+str(year)+'_clean.csv',encoding = 'iso-8859-1')
		self.data = data
		self.merged_data = pd.concat([data[year] for year in range(2010,2017)], ignore_index= True)
		self.city = city_level(self.merged_data)
	
		pass
    # test city_level class
	def test_city_application_pool(self):
		
		self.assertEqual(self.city.city_application_pool(self.city, "JERSEY CITY"), 16743)
		self.assertEqual(self.city.city_application_pool(self.city, "NEW YORK"), 155609)
		self.assertEqual(self.city.city_application_pool(self.city, "LOS ANGELES"),15109 )
		self.assertEqual(self.city.city_application_pool(self.city, "SEATTLE"),20662 )
		
		
	def test_city_approve_rate(self):
		
		self.assertGreater(self.city.city_approval_rate(self.city, "JERSEY CITY"),0.86)
		self.assertLess(self.city.city_approval_rate(self.city, "JERSEY CITY"),1)
		
		self.assertGreater(self.city.city_approval_rate(self.city, "NEW YORK"),0.83)
		self.assertLess(self.city.city_approval_rate(self.city, "NEW YORK"),1)
		
		self.assertGreater(self.city.city_approval_rate(self.city, "LOS ANGELES"),0.82)
		self.assertLess(self.city.city_approval_rate(self.city, "LOS ANGELES"),1)
		
		self.assertGreater(self.city.city_approval_rate(self.city, "SEATTLE"),0.87)
		self.assertLess(self.city.city_approval_rate(self.city, "SEATTLE"),1)
		

	def test_city_average_wage(self):

		self.assertGreater(self.city.city_average_wage(self.city, "JERSEY CITY"),73158)
		self.assertGreater(self.city.city_average_wage(self.city, "NEW YORK"),81179)
		self.assertGreater(self.city.city_average_wage(self.city, "LOS ANGELES"),68409)
		self.assertGreater(self.city.city_average_wage(self.city, "SEATTLE"),85383)

if __name__ == '__main__':

	unittest.main()
