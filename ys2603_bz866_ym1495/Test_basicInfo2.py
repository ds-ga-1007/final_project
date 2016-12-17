'''
Created on Dec 3, 2016

@author: muriel820
'''
import unittest
from basicInfo2 import *
import pandas as pd
import numpy as np

'''
This unittest tests the basic information of Pokemons, including methods of demonstration 
requested by users of when and where one appeared, the freqencies of appearance of a 
given pokemon in different cities etc. 
Note: the data used in this test is from practiceData.csv in this unittest folder.
'''
df = pd.read_csv('practiceData.csv')

class test(unittest.TestCase):

    def test_listPokemonIdsAppeared(self):
        arr = listPokemonIdsAppeared(df)
        self.assertIn(16, arr)
        self.assertNotIn(1, arr)
        self.assertEqual(len(arr),35)

    def test_getContinentNames(self):
        cont = getContinentNames(df)
        self.assertEqual(len(cont),4)
        self.assertIn('Asia', cont)

    def test_getCityNames(self):
        city = getCityNames(df)
        self.assertNotIn('Jersey City', city)
        self.assertIn('New_York', city)

    def test_pokemonwideDataframe(self):
        records1 = pokemonwideDataframe(df,16)
        records2 = pokemonwideDataframe(df,17)
        self.assertEqual(records1.shape[0],30)
        self.assertEqual(records2.shape, (3,203))

    def test_citywideDataFrame(self):
        citydf = citywideDataframe(df, 'Mexico_City')
        self.assertEqual(citydf.shape, (12,203))
        self.assertNotIn(17, citydf.ix[:,1])

    def test_hasItAppearedGlobally(self):
        glob = hasItAppearedGlobally(df,16)
        self.assertTrue(glob)


    def test_appeared_time(self):
        time =  appeared_time(df,16)
        timedf = pd.DataFrame(time)
        self.assertEqual(timedf.shape[0], 3)
        self.assertNotIn(16,timedf['time'])

    def test_co_occurance(self):
        co_occur1 = co_occurance(df,16)
        co_occur2 = np.asarray(co_occurance(df,100))
        self.assertNotIn(10,co_occur1)
        self.assertTrue(co_occur2.max,42)

if __name__ == "__main__":
    unittest.main()
