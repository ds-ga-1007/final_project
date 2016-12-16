"""
This is module tests the methods in class h1b_data

Created on 2016/12/01
Version: 1.0
@author: Sheng Liu
ShengLiu Copyright 2016-2017
"""

from h1b_data import *
import unittest

class utest(unittest.TestCase):
	def setUp(self):
		data = {}
		for year in range(2010,2017):
			data[year]= pd.read_csv('../DataBase/H-1B_FY'+str(year)+'_clean.csv',encoding = 'iso-8859-1')
		self.data = h1b_data(data)

	def test_calc_application_pool(self):
		self.assertGreater(self.data.calc_application_pool('Overview',2016)[2],0)
		self.assertGreater(self.data.calc_application_pool('Country',2016)[3],0)
		self.assertGreater(self.data.calc_application_pool('State','NY')[5],0)
	def test_calc_approve_rate(self):
		self.assertLess(self.data.calc_approve_rate('Overview')[0],100)
		self.assertLess(self.data.calc_approve_rate('Overview')[1],100)
		self.assertLess(self.data.calc_approve_rate('Overview')[5],100)
		self.assertLess(self.data.calc_approve_rate('Country')[5],100)
		self.assertLess(self.data.calc_approve_rate('State')[6],100)
	def test_calc_average_wage(self):
		self.assertGreater(self.data.calc_average_wage('Overview',2016)[2],0)
		self.assertGreater(self.data.calc_average_wage('Country',2016)[2],0)
		self.assertGreater(self.data.calc_average_wage('State')[2],0)
		self.assertGreater(self.data.calc_average_wage('State')[5],0)


if __name__ == '__main__':

	unittest.main()