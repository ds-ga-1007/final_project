import unittest
import ExpenseAnalyzer.DataHandler as DH
import ExpenseAnalyzer.utiltools as ut
from datetime import datetime

expensedata = ut.load_expense_data('all_house_senate_2010.csv')
resultdata = ut.load_result_data('result_2010.csv')
mergeddata = ut.merge_expense_result(expensedata, resultdata)
mergeddata.RESULT.fillna('L', inplace=True)

class UtilTest(unittest.TestCase):
    '''Unit Test for functions in utiltools.py'''
    
    def test_format_number(self):
        ''' Test format_number function'''
        self.assertEqual(ut.format_number('$100'), 100)
        self.assertEqual(ut.format_number('$100,000'), 100000)
        self.assertEqual(ut.format_number('($100,000)'), -100000)
    
    def test_format_date(self):
        ''' Test format_date function'''
        self.assertEqual(ut.format_date('12/31/2016'), datetime.strptime('12/31/2016','%m/%d/%Y').date())
        self.assertEqual(ut.format_date('07/31/2016'), datetime.strptime('07/31/2016','%m/%d/%Y').date())
        self.assertNotEqual(ut.format_date('12/30/2016'), datetime.strptime('12/31/2016','%m/%d/%Y').date())
    
    def test_load_expense(self):

        #Test loading expense data
        self.assertEqual(len(expensedata),865178)
        self.assertEqual(expensedata.ele_yea.unique(),[2010])
    def test_load_result(self):        
        
        #Test loading result data
        self.assertEqual(len(resultdata),480)
        self.assertEqual(resultdata.RESULT.unique(),['W'])

    def test_merging_data(self):        

        #Test Merging data
        self.assertEqual(len(mergeddata), 869034)
        self.assertCountEqual(mergeddata.RESULT.unique(),['W','L'])
    

class DataHandlerTest(unittest.TestCase):
     '''Unit Test for DataHandlers in DataHandler.py'''
     
     def test_StateAnalyzer(self):
         '''This tests StateAnalyzer class'''
         stateanalyzer = DH.StateAnalyzer(mergeddata)
         VALID_STATES = stateanalyzer.get_state_list()
         self.assertEqual(len(VALID_STATES), 55)
         stateanalyzer.set_state_data('NY') #Check state set method with NY
         self.assertEqual(stateanalyzer.filtered_data.can_off_sta.unique(), ['NY'])
         stateanalyzer.set_state_data('CA') #Check state set method with CA
         self.assertEqual(stateanalyzer.filtered_data.can_off_sta.unique(), ['CA'])
         
     def test_YearAnalyzer(self):
         '''This tests YearAnalyzer class'''
         yearanalyzer = DH.YearAnalyzer(mergeddata)
         yearanalyzer.set_year_data([2012]) #Check year set method with invalid year
         self.assertEqual(len(yearanalyzer.filtered_data), 0)
         yearanalyzer.set_year_data([2010]) #Check year set method with valid year
         self.assertNotEqual(len(yearanalyzer.filtered_data), 0)
         self.assertEqual(yearanalyzer.filtered_data.ele_yea.unique(), [2010])
     
if __name__ == '__main__':
    unittest.main()