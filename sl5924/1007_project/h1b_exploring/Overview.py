"""
This is the Overall module of the project, in this module, we focus on which topic a customer interested in.

Author: ShengLiu (sl5924)
"""

import sys
from h1b_exploring.h1b_draw import *
from h1b_exploring.exception_list import *
from h1b_exploring.All_about_input import option_input

from h1b_exploring.h1b_data import h1b_data


def overview(data):
	
	data = h1b_data(data)
	
	print ("================================ H1b Visa Approve Rate Exploring ================================")
	print ("")
	print ("                             Please choose one topic you interested in                           ")
	print ("                              <a>  : Application Pool                                            ")
	print ("                              <b>  : Approval Rate                                               ")
	print ("                              <c>  : Average Wage                                                ")
	print ("                              <r>  : Go back to previous directory                               ")  
	print ("")
	print ("=================================================================================================")
	
	Flag = True
	while Flag:
		try:
			key = option_input()
			if key == 'a':
				application_pool = data.calc_application_pool('Overview')
				plot_line_chart(application_pool,'Application Pool Size','Overview of Application Pool')
				
			if key == 'b':
				APPROVE_RATE_LIST = data.calc_approve_rate('Overview')
				plot_line_chart(APPROVE_RATE_LIST,'Approve Rate (%)','Overview of Approve Rate')
			
			if key == 'c':
				AVERAGE_WAGE_LIST = data.calc_average_wage('Overview')
				plot_line_chart(AVERAGE_WAGE_LIST,'Average Wage', 'Overview of Average Wage')
				
			if key == 'r':
				Flag = False
		
		except KeyboardInterrupt:
			sys.exit(1)
		except wrong_option_exception:
			print ("Invalid option, please reselect.")




if __name__ == '__main__':
	data = {}
	for year in range(2010,2017):
		data[year]= pd.read_csv('/Users/yuweitu/Documents/Programming/DSGA1007_Project/DataBase/H-1B_FY'+str(year)+'_clean.csv',encoding = 'iso-8859-1')
	overview(data)

