import os
import pandas as pd

def Read_data():
	"""
	This function Read_data read all four csv files: bookingNYC.csv, yelp_data.csv, museum.csv, attraction.csv, and
	return four dataframe as: data_hotel, data_restaurant, data_museum, data_attraction
	
	Exceptions:
		handle IOError exceptions
	"""
	try:
		path = os.getcwd() + '/Data/booking.csv'
		data_hotel = pd.read_csv(path, thousands = ',', encoding = 'latin1',  index_col = 0)
		data_hotel = clean_hotel_data(data_hotel)

		path = os.getcwd() + '/Data/yelp_data.csv'
		data_restaurant = pd.read_csv(path, encoding = 'latin1')
		data_restaurant = clean_restaurant_data(data_restaurant)

		path = os.getcwd() + '/Data/museum.csv'
		data_museum = pd.read_csv(path, encoding = 'latin1',  index_col = 0)

		path = os.getcwd() + '/Data/attraction.csv'
		data_attraction = pd.read_csv(path, encoding = 'latin1',  index_col = 0)

		return data_hotel, data_restaurant, data_museum, data_attraction
	except IOError:
		print("Error: can\'t find file or read data")

def clean_hotel_data(df):
	"""
	This function clean hotel data, get all hotel information such that the following scores are larger or equal to 5
	Parameters:
		df: Dataframe
	Return:
		df: Dataframe
	"""
	columns = ['Avgscore', 'Cleanliness', 'Comfort', 'Facilities', 'Free Wifi', 'Location', 'Staff', "Value for money"]
	for c in columns:
		df = df[df[c] >= 5]
		df = df[df[c] <= 10]
	df.index = range(df.shape[0])
	return df


def clean_restaurant_data(df):
	"""
	This function clean restaurant data, get all restaurant information such that the number of price is larger than 1, 
	and delete all the 
	Parameters:
		df: Dataframe
	Return:
		df: Dataframe
	"""
	df = df[df['number_of_price'] >= 1]
	
	"""
	drop the restaurant in NJ
	"""
	delete_index_list = []
	for i, item in enumerate(df['Address']):
		if (item.find('NJ') != -1):
			delete_index_list.append(i)
	df = df.drop(df.index[delete_index_list])
	df.index = range(df.shape[0])
	return df


































