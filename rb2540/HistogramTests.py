import unittest
import numpy as np
from MonthlyHistogram import *

class HistogramTests(unittest.TestCase) :
    def test_lengthHail(self) :
        """Tests length valid"""
        file = r'./FilteredData/filteredData.csv'
        histogram = MonthlyHistogram(file)
        v = histogram.getYearCounts(2000,['Hail'])
        self.assertEqual(len(v),12)
        self.assertTrue(sum(v)>0)

    def test_lengthMulti(self) :
        """Tests length valid with multiselect"""
        file = r'./FilteredData/filteredData.csv'
        histogram = MonthlyHistogram(file)
        v = histogram.getYearCounts(1992,['Hail','Tornado'])
        self.assertEqual(len(v),12)
        self.assertTrue(sum(v)>0)

if __name__ == '__main__':
    unittest.main()
