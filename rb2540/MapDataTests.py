import unittest
import numpy as np
from MapDataSelector import *

class MapDataTests(unittest.TestCase) :
    def test_lengthHail(self) :
        """Tests lengths match"""
        file = r'./FilteredData/filteredData.csv'
        mapData = MapDataSelector(file)
        t = mapData.getYearData(2000,['Hail'])
        self.assertEqual(len(t),2)
        self.assertEqual(len(t[0]),len(t[1]))
        self.assertTrue(len(t[0])>0)

    def test_lengthMulti(self) :
        """Tests lengths match with multiselect"""
        file = r'./FilteredData/filteredData.csv'
        mapData = MapDataSelector(file)
        t = mapData.getYearData(2000,['Hail','Tornado'])
        self.assertEqual(len(t),2)
        self.assertEqual(len(t[0]),len(t[1]))

    def test_lonMulti(self) :
        """Tests lons valid"""
        file = r'./FilteredData/filteredData.csv'
        mapData = MapDataSelector(file)
        t = mapData.getYearData(2000,['Hail','Tornado'])
        lons = t[0]
        self.assertEqual(len(lons[lons<-400]),0)
        self.assertEqual(len(lons[lons>-60]),0)

if __name__ == '__main__':
    unittest.main()
