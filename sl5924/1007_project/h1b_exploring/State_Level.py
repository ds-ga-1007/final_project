"""
This is module which designed for interactions in state level
Customs may input the abbreviaton of the state name they interested in
They will get line charts of application pools, approve rate, average Wage
and (.    ) in that state

Created on 2016/12/01
Version: 1.0
@author: liusheng, Yuwei Tu
ShengLiu Copyright 2016-2017
"""


import sys
from h1b_exploring.h1b_data import *
from h1b_exploring.h1b_draw import *
from h1b_exploring.exception_list import invalid_state_name

def state_level(states,h1b_data):
	
	while True:
		try:
			print ("================================ H1b Visa Approve Rate Exploring =================================")
			print ("")
			print ("          Please Input a state ABBREVIATION you interested in (NY, CA, MI, etc.)                  ")
			print ("		             You may input return to go back to Location menu                             ")			
			print ("==================================================================================================")

			state_name = input('Please input here: ') 
			if state_name in states:
				application_pool = h1b_data.calc_application_pool('State',state_name)
				APPROVE_RATE = h1b_data.calc_approve_rate('State', state_name)
				AVERAGE_WAGE = h1b_data.calc_average_wage('State', state_name)
				plot_line_chart(application_pool, 'Application Pool Size','State Level Application Pool')
				plot_line_chart(APPROVE_RATE, 'Approve Rate (%)','State Level Approve Rate')
				plot_line_chart(AVERAGE_WAGE, 'Average Wage','State Level Average Wage')
				break
				#How do we show the rank if the rank is actually a data frame
			elif state_name == 'quit':
				sys.exit(1)
			elif state_name == 'return':
				break
			else:
				raise invalid_state_name
		
		except invalid_state_name:
			print ("Invalid state abbreviation, please input again")
		except KeyboardInterrupt:
			sys.exit(1)

if __name__ == '__main__':
	data = {}
	for year in range(2010,2017):
		data[year]= pd.read_csv('DataBase/H-1B_FY'+str(year)+'_clean.csv',encoding = 'iso-8859-1')
	states = h1b_data(data).states
	state_level(states,h1b_data(data))







