import unittest
import numpy as np
from YearlyEventAggregator import *

class AggregatorTests(unittest.TestCase) :
    def test_keysValid(self) :
        """Tests keys valid"""
        keys = ['Injuries','Deaths','Number of Events']
        file = r'./FilteredData/filteredData.csv'
        agg = YearlyEventAggregator(file)
        k = agg.getKeys()
        self.assertEqual(len(keys),len(k))
        self.assertEqual(set(keys),set(k))

    def test_lengthAll(self) :
        """Tests length valid with each key type"""
        file = r'./FilteredData/filteredData.csv'
        agg = YearlyEventAggregator(file)
        for a in agg.getKeys() :
            self.assertTrue(len(agg.getAggregate(a))>0)

if __name__ == '__main__':
    unittest.main()
