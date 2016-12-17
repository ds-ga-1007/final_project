"""
Unittest of class AccidentAnalysis.
"""
import unittest
from AccidentAnalysis import *

filename = "NYPD_Motor_Vehicle_Collisions.csv"
df = pd.read_csv(filename)
# df_1 = df.replace(['Unspecified'], np.nan)

class TestAnalysis(unittest.TestCase):
    
    def test_select_year(self): 
        self.assertEqual(len(AccidentAnalysis(df).select_year(2015)),217539)
        self.assertEqual(len(AccidentAnalysis(df).select_year(2014)),205929)
        
    def test_select_borough(self):
        self.assertEqual(len(AccidentAnalysis(df).select_borough('manhattan')),180735)
        self.assertEqual(len(AccidentAnalysis(df).select_borough('brooklyn')),213651)
        
    def test_group_total(self):
        self.assertEqual(AccidentAnalysis(df).group_total()['MANHATTAN'].iloc[1], 41577)
        self.assertEqual(AccidentAnalysis(df).group_total()['MANHATTAN'].iloc[4], 34698)
        
    def test_group_total_injured(self):
        self.assertEqual(AccidentAnalysis(df).group_total_injured()['MANHATTAN'].iloc[1],7584)
        self.assertEqual(AccidentAnalysis(df).group_total_injured()['MANHATTAN'].iloc[4],5814)
        
    def test_group_total_killed(self):
        self.assertEqual(AccidentAnalysis(df).group_total_killed()['MANHATTAN'].iloc[1],39)
        self.assertEqual(AccidentAnalysis(df).group_total_killed()['MANHATTAN'].iloc[4],30)
        
    def test_count_year_total(self):
        self.assertEqual(AccidentAnalysis(df).count_year_total('MANHATTAN')['2015'], 42497)
        self.assertEqual(AccidentAnalysis(df).count_year_total('BROOKLYN')['2015'], 50819)
        
    def test_sort_zip_total(self):
        self.assertEqual(AccidentAnalysis(df).sort_zip_total(2014).iloc[0], 2798)
        self.assertEqual(AccidentAnalysis(df).sort_zip_total(2014).iloc[1], 2440)
        
    def test_sort_zip_borough(self):
        self.assertEqual(AccidentAnalysis(df).sort_zip_borough(2015,'MANHATTAN').iloc[1],2285)
        self.assertEqual(AccidentAnalysis(df).sort_zip_borough(2015,'MANHATTAN').iloc[0], 2432)
        
    def test_sort_reasons_total(self):
        self.assertEqual(AccidentAnalysis(df).sort_reasons_total(2015).iloc[0], 270216)
        self.assertEqual(AccidentAnalysis(df).sort_reasons_total(2015).iloc[1], 41790)

    def test_sort_types_total(self):
        self.assertEqual(AccidentAnalysis(df).sort_types_total(2015).iloc[0], 208424)
        self.assertEqual(AccidentAnalysis(df).sort_types_total(2015).iloc[1], 102844)
       
        
if __name__ == "__main__":
    unittest.main()