# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import ClinicSearchByAddress as cs
import InputFunctions as ip
import geocoder as geo
from NationalComparissonTime import *
from UserProfile import *
import numpy as np
import ComparissonStateWise2014 as comp


class testyesNoParser(unittest.TestCase):
    
    def test_functions_YES(self):
        self.assertTrue(ip.yesNoParser("yes"))
        self.assertTrue(ip.yesNoParser("y"))
        self.assertTrue(ip.yesNoParser("YES"))
        self.assertTrue(ip.yesNoParser("True"))
    
    def test_functions_No(self):           
        self.assertFalse(ip.yesNoParser("no"))
        self.assertFalse(ip.yesNoParser("No"))
        self.assertFalse(ip.yesNoParser("n"))
        
    def exceptionHandling(self): 
        self.assertRaises(ip.yesNoParser("foo"), ip.yesNoParserException())

class testimportMyCsv(unittest.TestCase):
    
    def testImportCSV(self):
        self.assertEqual(ip.importMyCsv("FIX_Georeferenced07_14", extraFilePath="IVF_Analysis/Data/", encoding="mac_latin2").shape, (362, 13))
        self.assertEqual(ip.importMyCsv("FIX_Georeferenced07_14", extraFilePath="IVF_Analysis/Data/", encoding="mac_latin2").loc[1, "ClinStateCode"], 'CALIFORNIA')

class wholeNumericPositiveInputParserTest(unittest.TestCase):
    
    def testNumbers(self):
        self.assertEqual(ip.wholeNumericPositiveInputParser("78"), 78)
        self.assertEqual(ip.wholeNumericPositiveInputParser("1"), 1)
        
    def exceptionhanler(self): 
        self.assertRaises(ip.wholeNumericPositiveInputParser("foo"), ip.nonNumericInput()) 
        self.assertRaises(ip.wholeNumericPositiveInputParser("1.7"), ip.nonIntegerInput()) 
        self.assertRaises(ip.wholeNumericPositiveInputParser("-1"), ip.negativeInput()) 
        
class testload_data(unittest.TestCase):
    
    def testLoad_data(self):
        self.assertEqual(ip.load_data(False)[2008].shape, (436, 120))
        self.assertEqual(len(ip.load_data(False)), 8)
        self.assertEqual(ip.load_data(False)[2008].loc[1,"ClinCityCode"], "BIRMINGHAM")
        
big_data = ip.load_data(comments= False)

class Test(unittest.TestCase):

        
    def test_identifier1(self):
        '''test the categorizer method of the identifier class'''
        self.assertEqual(identifier(45, False, False, 'Alabama').categorizer()[1], 'Frozen Egg Non-Donor')
        self.assertEqual(identifier(32, True, True, 'California').categorizer()[1], 'Fresh Embryo from Donor Egg')
        self.assertEqual(identifier(32, True, True, 'California').categorizer()[0], 3)

    def test_identifier2(self):
        '''test the age_grouper method of the identifier class'''
        self.assertEqual(identifier(45, False, False, 'Alabama').age_grouper()[1], '45 and older')
        self.assertEqual(identifier(45, False, False, 'Alabama').age_grouper()[0], 6)
        self.assertEqual(identifier(21, True, False, 'New Jersey').age_grouper()[1], 'under 35 years old' )
        self.assertEqual(identifier(39, False, True, 'New Jersey').age_grouper()[1], 'between 38 and 40 years old' )
    
    def test_identifier3(self):
        '''test the main_variable_early method of the identifier class'''
        self.assertEqual(identifier(40, False, True, 'Alabama').main_variable_early(), 'FshNDLvBirthsRate3')
        self.assertEqual(identifier(20, True, True, 'Alabama').main_variable_early(), 'FshDnrLvBirthsRate')

    def test_identifier4(self):
        '''test the main_variable_late method of the identifier class'''
        self.assertEqual(identifier(40, False, True, 'Alabama').main_variable_late(), 'FshNDLvBirths_TransRate3')
        self.assertEqual(identifier(20, True, False, 'Alabama').main_variable_late(), 'ThwDnrLvBirths_TransRate')

    def test_identifier5(self):
        '''test the live_births_transfer_plot method of the identifier class'''
        self.assertEqual(identifier(37, False, True, 'New York').live_births_transfer_plot(), 'FshNDLvBirths_TransRate2')
        self.assertEqual(identifier(29, True, False, 'Alaska').live_births_transfer_plot(), 'ThwDnrLvBirths_TransRate')
        
    def test_mean_finder(self):
        '''Test the mean_finder function'''
        self.assertEqual(np.round(mean_finder(big_data, identifier(34, False, False, "Alabama"))[3]), 35)
        self.assertEqual(np.round(mean_finder(big_data, identifier(39, True, False, "New York"))[4]), 34)
    
    def test_mean_finder2(self):
        '''Test the mean_finder function'''
        self.assertEqual(mean_finder(big_data, identifier(34, False, False, "Alabama")).size , 8)
         
    def test_clinic_finder1(self):
        '''Test clinic_finder1 function'''
        self.assertEqual(clinic_finder('FERTILITY CARE OF ORANGE COUNTY', identifier(39, True, False, "New York"), big_data).name, 
                         'Frozen Embryo from Donor Egg between 38 and 40 years old' )    
     
    def test_clinic_finder2(self):
        '''Test clinic_finder1 function'''
        self.assertEqual(clinic_finder('FERTILITY CARE OF ORANGE COUNTY', identifier(25, True, True, "New York"), big_data).name, 
                         'Fresh Embryo from Donor Egg under 35 years old')     
     
        
    def test_clinic_finder3(self):
        '''Test clinic_finder1 function'''
        self.assertEqual(clinic_finder('FERTILITY CARE OF ORANGE COUNTY', identifier(39, True, False, "New York"), big_data).size, 8 )   

class Test2(unittest.TestCase):
    
    
    def test_variables_to_plot(self):
        """ Check whether correct variables are plotter per specified user profile"""
        self.assertEqual(comp.embryo_cat_variables(identifier(33,False,True,'NY'))[0], 'FshNDCycle')
        self.assertEqual(comp.embryo_cat_variables(identifier(33,False,True,'NY'))[6], 'FshNDLvBirths_TransRate')
        
        self.assertEqual(comp.embryo_cat_variables(identifier(25,True,True,'NY'))[0], 'FshDnrTotCycles')
        self.assertEqual(comp.embryo_cat_variables(identifier(25,True,True,'NY'))[4], 'FshDnrTransPregRate')

        self.assertEqual(comp.embryo_cat_variables(identifier(18,False,False,'NJ'))[1], 'ThwNDEmbryosRate')
        self.assertEqual(comp.embryo_cat_variables(identifier(25,False,False,'NY'))[2], 'ThwNDTransfers')

        self.assertEqual(comp.embryo_cat_variables(identifier(18,True,False,'AL'))[3], 'ThwDnrLvBirths_TransRate')
        self.assertEqual(comp.embryo_cat_variables(identifier(25,True,False,'CA'))[1], 'ThwDnrEmbryosRate')

    def test_other_clinics_set1(self):
        """ Check whether correct set of clinics gets selected by other_clinics_set function"""

        self.assertTrue("WEILL MEDICAL COLLEGE OF CORNELL UNIVERSITY" in comp.other_clinics_set("COLUMBIA UNIVERSITY CENTER FOR WOMEN'S REPRODUCTIVE CARE", 'NEW YORK', big_data[2014]).PrevClinName1.values)
        self.assertTrue("THE FERTILITY INSTITUTE AT NEW YORK METHODIST HOSPITAL" in comp.other_clinics_set("COLUMBIA UNIVERSITY CENTER FOR WOMEN'S REPRODUCTIVE CARE", 'NEW YORK',big_data[2014]).PrevClinName1.values)
        self.assertFalse("COLUMBIA UNIVERSITY CENTER FOR WOMEN'S REPRODUCTIVE CARE" in comp.other_clinics_set("COLUMBIA UNIVERSITY CENTER FOR WOMEN'S REPRODUCTIVE CARE", 'NEW YORK',big_data[2014]).PrevClinName1.values)

        
    def test_other_clinics_set2(self):
        """ Check whether correct set of clinics gets selected by other_clinics_set function"""     
        
        self.assertTrue("FERTILITY CENTER OF DALLAS" in comp.other_clinics_set("SHER INSTITUTE FOR REPRODUCTIVE MEDICINE-DALLAS", 'TEXAS', big_data[2014]).PrevClinName1.values)
        self.assertTrue("DR. JEFFREY YOUNGKIN" in comp.other_clinics_set("SHER INSTITUTE FOR REPRODUCTIVE MEDICINE-DALLAS", 'TEXAS', big_data[2014]).PrevClinName1.values)
        self.assertFalse("SHER INSTITUTE FOR REPRODUCTIVE MEDICINE-DALLAS" in comp.other_clinics_set("SHER INSTITUTE FOR REPRODUCTIVE MEDICINE-DALLAS", 'TEXAS', big_data[2014]).PrevClinName1.values)
        
    
    def test_plot(self):
        """ Check whether plot function produces correct output """

        self.assertEqual(comp.plot(1, identifier(33,False,True,'CALIFORNIA'))[0], "FshNDCycle1")
        self.assertEqual(comp.plot(1, identifier(35,False,True,'CALIFORNIA'))[0], "FshNDCycle2")
        self.assertEqual(comp.plot(1, identifier(33,False,True,'NEW YORK'))[1], "Number of Cycles")
        self.assertEqual(comp.plot(2, identifier(33,False,True,'NEW YORK'))[1], "Live Births per 100 Transfers")
        
            
if __name__ == '__main__':
    unittest.main()