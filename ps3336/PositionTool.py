import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PositionTool:

	def age_distribution(data_interested, input_position, save):
		plt.hist(data_interested['age'])
		plt.title('Age Distribution of ' + input_position + ' in Transfer Players of Year 2014, 2015, 2016')
		plt.xlabel('Age')
		plt.ylabel('Count')
		if save == 'y':
			plt.savefig('Age_Distribution_of_' + input_position + '.pdf')
		plt.show()

	def transfer_fee_box(data_interested, input_position, save):
		data_interested.boxplot('transfer_fee_pounds_int', by = 'year')
		plt.title('Box plot of Transfer Fee of ' + input_position + ' in Year 2014, 2015, 2016')
		plt.xlabel('Year')
		plt.ylabel('Transfer Fee')
		if save == 'y':
			plt.savefig('Transfer Fee of ' + input_position +'.pdf')
		plt.show()

	def num_transfer(data_interested, input_position, save):
		grouped_data = data_interested.groupby(['club', 'year'])['position'].count()
		clubs = grouped_data.index.get_level_values('club').unique()
		years = [2014, 2015, 2016]
		count = np.zeros((len(clubs), len(years)))
		for i in range(len(clubs)):
			for j in range(len(years)):
				if years[j] in grouped_data[clubs[i]].index:
					count[i][j] = grouped_data[clubs[i]][years[j]]
		fig, ax = plt.subplots()
		fig.set_size_inches(15, 10)
		bar1 = ax.bar(np.arange(len(clubs)) * 3, count.T[0], 0.5, color = 'r')
		bar2 = ax.bar(np.arange(len(clubs)) * 3 + 0.5, count.T[1], 0.5, color = 'g')
		bar3 = ax.bar(np.arange(len(clubs)) * 3 + 1, count.T[2], 0.5, color = 'b')
		ax.set_ylabel('Number of Transfer Players')
		ax.set_title('Number of Transfer Players of ' + input_position + ' by Club')
		plt.xticks(np.arange(len(clubs)) * 3 + 0.75, clubs, rotation = 90)
		ax.legend((bar1[0], bar2[0], bar3[0]), ('2014', '2015', '2016'))
		if save == 'y':
			fig.savefig('Number of Transfers of ' + input_position +' by clubs.pdf')
		plt.show()
		return count 

	def invest_on_return(data_interested, input_position, save):
		grouped_data_goal = data_interested[data_interested['transfer_status'] == 'in'].groupby(['club', 'year'])['goals'].sum()
		grouped_data_invest = data_interested[data_interested['transfer_status'] == 'in'].groupby(['club', 'year'])['transfer_fee_pounds_int'].sum()
		clubs = grouped_data_goal.index.get_level_values('club').unique()
		years = [2014, 2015, 2016]
		ior = np.zeros((len(clubs), len(years)))
		for i in range(len(clubs)):
			for j in range(len(years)):
				if years[j] in grouped_data_goal[clubs[i]].index:
					ior[i][j] = grouped_data_invest[clubs[i]][years[j]] / grouped_data_goal[clubs[i]][years[j]]
		fig, ax = plt.subplots()
		fig.set_size_inches(15, 10)
		bar1 = ax.bar(np.arange(len(clubs)) * 3, ior.T[0], 0.5, color = 'r')
		bar2 = ax.bar(np.arange(len(clubs)) * 3 + 0.5, ior.T[1], 0.5, color = 'g')
		bar3 = ax.bar(np.arange(len(clubs)) * 3 + 1, ior.T[2], 0.5, color = 'b')
		ax.set_ylabel('Transfer Fee / Goals')
		ax.set_title('Club Investment on return in ' + input_position)
		plt.xticks(np.arange(len(clubs)) * 3 + 0.75, clubs, rotation = 90)
		ax.legend((bar1[0], bar2[0], bar3[0]), ('2014', '2015', '2016'))
		if save == 'y':
			fig.savefig('Investment on Return of ' + input_position +' by clubs.pdf')
		plt.show()
		return ior 
