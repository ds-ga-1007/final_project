import unittest
from Sort.sort import *
from Sort.yelp_sort import *
from Data.Read_data import *
from Search.search import *
from Plan.trip_plan import *
import random

class tests_sort(unittest.TestCase):

	"""Unit-testing class that allows us to run tests with expected outcomes
	Run the test in the project's root directory
	with the following command:
		$ python -m unittest discover
	"""
	def test_distance(self):
		"""
		This method tests the function distance in the Sort directory sort.py. 
		"""
		d1 = distance(40.748817, -73.985428, 40.785091, -73.968285)
		d2 = distance(40.785091, -73.968285, 40.730824, -73.997330)
		d3 = distance(40.748817, -73.985428, 40.730824, -73.997330)		

		self.assertEqual(2.659686800500446, d1)
		self.assertEqual(4.042818796866881, d2)
		self.assertEqual(1.3898520048298273, d3)

	def test_read_data_columnnames(self):
		"""
		This method tests the function Read_data in Data directory by tesing the read in dataframe has
		the same columns name as the original dataset.
		"""
		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()

		hotel_columns = ['Unnamed: 0', 'Address', 'Avgscore', 'Cleanliness', 'Comfort', \
				'Facilities', 'Free Wifi', 'Location', 'Price', 'Staff', 'Total_review', \
				'Value for money', 'Lat', 'Lng', 'Name']
		restaurant_columns = ['Address', 'category', 'Lat', 'Lng', 'number_of_price', \
				'Total_review', 'Name', 'Avgscore']

		museum_columns = ['Unnamed: 0', 'Address', 'description', 'detail', 'Lat', 'Lng', 'Name', \
				'Avgscore', 'Total_review']

		attraction_columns = ['Unnamed: 0', 'Address', 'description', 'detail', 'Lat', 'Lng', 'Name', \
				'Avgscore', 'Total_review']
		
		self.assertEqual(hotel_columns, data_hotel.columns.tolist())
		self.assertEqual(restaurant_columns, data_restaurant.columns.tolist())
		self.assertEqual(museum_columns, data_museum.columns.tolist())
		self.assertEqual(attraction_columns, data_attraction.columns.tolist())
	
	def test_sort_within_rows(self):
		"""
		This method tests the return dataframe contains the respected number of rows.
		"""
		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()

		df1 = sort_within(data_hotel, 40.748817, -73.985428, 1.5, 'Price', [1])

		yelp_category(data_restaurant)
		df2 = sort_within(data_restaurant, 40.748817, -73.985428, 1.5, 'ctg', 'Chinese')
		
		self.assertTrue(df1.shape[0] <= 10)
		self.assertTrue(df2.shape[0] <= 10)

	def test_sort_within_sort_algorithm(self):
		"""
		This method tests the sort_winthin method sort correctly. First, sort by 'Avgscore' column.
		If two values in the 'Avgscore' column are same, we compare their 'Total_review' values.
		"""
		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()

		df1 = sort_within(data_hotel, 40.748817, -73.985428, 1.5, 'Price', [1])

		yelp_category(data_restaurant)
		df2 = sort_within(data_restaurant, 40.748817, -73.985428, 1.5, 'ctg', 'Chinese')

		for i in range(df1.shape[0]-1):
			self.assertTrue(df1.iloc[i]['Avgscore'] >= df1.iloc[i+1]['Avgscore'])
			if (df1.iloc[i]['Avgscore'] == df1.iloc[i+1]['Avgscore']):
				self.assertTrue(df1.iloc[i]['Total_review'] >= df1.iloc[i+1]['Total_review'])
			self.assertTrue(df2.iloc[i]['Avgscore'] >= df2.iloc[i+1]['Avgscore'])
			if (df2.iloc[i]['Avgscore'] == df2.iloc[i+1]['Avgscore']):
				self.assertTrue(df2.iloc[i]['Total_review'] >= df2.iloc[i+1]['Total_review'])


	def test_sort_within_distance(self):
		"""
		This method tests the distance between each hotel or restaurant in the return dataframe and the center points
		is less than or equal to the parameter 'distance_within'. In this test, this parameter is 1.5
		"""		
		cordinate_list1 = []
		cordinate_list2 = []

		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()

		df1 = sort_within(data_hotel, 40.748817, -73.985428, 1.5, 'Price', [1])

		yelp_category(data_restaurant)
		df2 = sort_within(data_restaurant, 40.748817, -73.985428, 1.5, 'ctg', 'Chinese')		

		for i in range(df1.shape[0]):
			self.assertTrue(distance(df1.iloc[i]['Lat'], df1.iloc[i]['Lng'], 40.748817, -73.985428) <= 1.5)
			self.assertTrue(distance(df2.iloc[i]['Lat'], df2.iloc[i]['Lng'], 40.748817, -73.985428) <= 1.5)

	def test_sort_within_radar_chart_for_hotel(self):
		"""
		This method test whether we clean hotel data correctly or not, to make sure we can draw the radar chart.
		"""
		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()
		
		for i in range(100):
			value = random.randint(1, 3)
			lat = 40.700 + (40.854 - 40.700) * random.random()
			lng = -74.018 + (-73.929 - (-74.018)) * random.random()

			#To reduce the time to call a function, we keep this code in here without writing a function
			if (value == 1):
				value_list = [1,2]
			elif (value == 2):
				value_list = [3,4]
			elif (value == 3):
				value_list = [5]

			#this method just test this peice of code work well
			columns = ['Avgscore', 'Cleanliness', 'Comfort', 'Facilities', 'Free Wifi', 'Location', 'Staff', "Value for money"]
			for c in columns:
				data_hotel = data_hotel[data_hotel[c] >= 5]
				data_hotel = data_hotel[data_hotel[c] <= 10]
			data_hotel.index = range(data_hotel.shape[0])

			df1 = sort_within(data_hotel, lat, lng, 1.5, 'Price', value_list)
			for c in columns:
				#self.assertTrue(all(i >= 5 for i in df1[c]))
				self.assertTrue((df1[c] >= 5).all() and (df1[c] <= 10).all())

	def test_sort_within_radar_chart_for_restaurant(self):
		"""
		This method test whether we clean restaurant data correctly or not, to make sure we can draw the radar chart.
		"""
		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()

		for i in range(100):
			lat = 40.700 + (40.854 - 40.700) * random.random()
			lng = -74.018 + (-73.929 - (-74.018)) * random.random()

			category = ['Chinese','Japanese','Asian','Italian',
              'French', 'US', 'European', 'LatinAmerican', 'Cafe_bar', 'African', 'MiddleEastern', 'Other']

			n = random.randint(0, 11)
			yelp_category(data_restaurant)
			data_restaurant = data_restaurant[data_restaurant['number_of_price'] >= 1]
			data_restaurant.index = range(data_restaurant.shape[0])
			df = sort_within(data_restaurant, lat, lng, 1.5, 'ctg', category[n])

			self.assertTrue((df['number_of_price'] <= 5).all() and (df['number_of_price'] >= 0).all())
			self.assertTrue((df['Reviews'] <= 5).all() and (df['Reviews'] >= 0).all())
			self.assertTrue((df['Avgscore'] <= 5).all() and (df['Avgscore'] >= 0).all())
			self.assertTrue((df['Distance'] <= 10).all() and (df['Distance'] >= 0).all())

	def test_sort_museums_or_attractions_sort_algorithm(self):
		"""
		This method tests the sort function 'sort_museums_or_attraction' by variaties of perspectives. It tests the return 
		dataframe of the function 'sort_museums_or_attractions' has the following propetis:
		columns 'Avgscore' >= 3.5, column 'Total_review' >= 1000
		"""
		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()

		df1 = sort_museums_or_attractions(data_museum)
		df2 = sort_museums_or_attractions(data_attraction)

		self.assertTrue((df1['Avgscore'] >= 3.5).all())
		self.assertTrue((df1['Total_review'] >= 1000).all())
		self.assertTrue((df2['Avgscore'] >= 3.5).all())
		self.assertTrue((df2['Total_review'] >= 1000).all())

	def test_sort_museums_or_attractions_sort_descending(self):
		"""
		This method tests the function 'sort_museums_or_attractions' sort by rating and total reviews both descending.
		"""

		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()

		df1 = sort_museums_or_attractions(data_museum)
		df2 = sort_museums_or_attractions(data_attraction)
				
		for i in range(df1.shape[0]-1):
			self.assertTrue(df1.iloc[i]['Avgscore'] >= df1.iloc[i+1]['Avgscore'])
			if (df1.iloc[i]['Avgscore'] == df1.iloc[i+1]['Avgscore']):
				self.assertTrue(df1.iloc[i]['Total_review'] >= df1.iloc[i+1]['Total_review'])
			self.assertTrue(df2.iloc[i]['Avgscore'] >= df2.iloc[i+1]['Avgscore'])
			if (df2.iloc[i]['Avgscore'] == df2.iloc[i+1]['Avgscore']):
				self.assertTrue(df2.iloc[i]['Total_review'] >= df2.iloc[i+1]['Total_review'])

class test_yelp_sort(unittest.TestCase):

	def test_yelp_category(self):
		"""
		This method tests the 'yelp_category' function in the Sort directory.
		"""
		data_hotel, data_restaurant, data_museum, data_attraction = Read_data()
		yelp_category(data_restaurant)

		restaurant_data_columns = ['Address', 'category', 'Lat', 'Lng', 'number_of_price', 
							'Total_review', 'Name', 'Avgscore', 'first_category', 'ctg']

		Category = ['Chinese','Japanese','Asian','Italian', 'French', 'US', \
					'European', 'LatinAmerican', 'Cafe_bar', 'African', 'MiddleEastern', 'Other']
		self.assertEqual(restaurant_data_columns, data_restaurant.columns.tolist())

		self.assertEqual(len(data_restaurant['ctg'].value_counts().index.tolist()), len(Category))

		
class test_trip_plan(unittest.TestCase):

	def test_revised_kmeans(self):
		"""
		This method test our trip planer method in the trip_plan.py in Plan directory by testing we recommented the expected number
		of attractions. Wanning: when implement this text, it will automatically open the result rtf file.
		"""
		t = trip_plan(4, 2, 2)
		index_list, center_points, cordinate_data = t.trip_planer()
		self.assertEqual(len(index_list), 4)
		self.assertEqual(len(center_points), 4)
		self.assertEqual(len(cordinate_data), 4*4)

		t1 = trip_plan(5, 2, 1)
		index_list, center_points, cordinate_data = t1.trip_planer()
		self.assertEqual(len(index_list), 5)
		self.assertEqual(len(center_points), 5)
		self.assertEqual(len(cordinate_data), 5*2)

if __name__ == "__main__":
    unittest.main()

