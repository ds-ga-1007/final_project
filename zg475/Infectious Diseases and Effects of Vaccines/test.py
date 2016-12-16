import unittest
from object_class import *
from exception_class import *
from statistics import *
'''
Test Class for the project

Created on Dec 15, 2016

'''

class Test(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_color_class(self):
        '''
        Test functionality of the color-related error handling
        '''
        self.assertEqual(color_class('0.8').color,0.8)
        
        with self.assertRaises(colorrangeException):
            color_class('8')
        with self.assertRaises(colorrangeException):
            color_class('-1')
        with self.assertRaises(colortypeException):
            color_class('dsfdfe')

        
    def test_year_class(self):
        '''
        Test functionality of year-related error handling 
        '''
        self.assertEqual(year_class('1978','MUMPS').year,1978)
        
        with self.assertRaises(yeartypeException):
            year_class('19fewwv','MUMPS')
        with self.assertRaises(yearrangeException):
            year_class('1900','MEASLES')
        with self.assertRaises(yearrangeException):
            year_class('1960','SMALLPOX')
               
    def test_disease_class(self):
        '''
        Test whether class could catch the right diseases
        '''
        self.assertEqual(disease_class('MUMPS').name,'MUMPS')
        self.assertEqual(disease_class('MUMPS').lower,1968)
        self.assertEqual(disease_class('MUMPS').upper,2014)
        
        with self.assertRaises(diseaseExceptioin):
            disease_class('vfdvfdv')
    
    def test_get_mean(self):
        '''
        Test functionality of the get_mean method from Class statistics
        '''
        self.assertFalse(get_mean('smallpox')[0] > 0)
        self.assertTrue(get_mean('smallpox')[1] > 0) 
        self.assertTrue(get_mean('poliomyelitis')[1] > 0) 
        
        self.assertEqual(len(get_mean('smallpox')),2)  
        self.assertEqual(len(get_mean('rubella')),2) 
        self.assertNotEqual(len(get_mean('rubella')),3)                      
        
        with self.assertRaises(InvalidDisease):
            get_mean('Nonedisease')
        
if __name__ =='__main__':
    unittest.main()