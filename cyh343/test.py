import unittest
from Functions.Functions import *
from CheckInput import Check_input
from Main import data

# Since the user input section function main() in main.py is in
# while loop, which difficult to have the test. We split it to just show
# if the input is valid or not.
# Notice that we only test string here because the user only allowed to 
# input string. Also, only allow user input the given option variables. 

def print_singleplayer_result(input_string):
    check = Check_input(input_string)
    if check.singleplayer_input(data) == -9999:
        return('Invalid input')
    else:
        return('Available player name') 

def print_singleteam_result(input_string):
    check = Check_input(input_string)    
    if check.singleteam_input(data) == -9999:
        return('Invalid input')
    else:
        return('Available team name') 
    
def print_multi_result(input_string):
    check = Check_input(input_string)    
    if check.multi_input(data) == -9999:
        return('Invalid input')
    else:
        return('Available input variable') 
 
class Test(unittest.TestCase):
    
    """Unittest for testing whether the user input is correct or not, and the merge function"""
    
    def test_singleplayer_input_invalid(self):
        self.assertEqual(print_singleplayer_result('A1'), 'Invalid input')
        self.assertEqual(print_singleplayer_result('$'), 'Invalid input')
        self.assertEqual(print_singleplayer_result('0'), 'Invalid input')
        self.assertEqual(print_singleplayer_result(' '), 'Invalid input')
        self.assertEqual(print_singleplayer_result('Zebra'), 'Invalid input')
    
    def test_singleplayer_input_valid(self):
        self.assertEqual(print_singleplayer_result('Sloan'), 'Available player name')
        self.assertEqual(print_singleplayer_result('lopez'), 'Available player name')
 
    def test_singleteam_input_invalid(self):
        self.assertEqual(print_singleteam_result('A'), 'Invalid input')
        self.assertEqual(print_singleteam_result('$'), 'Invalid input')
        self.assertEqual(print_singleteam_result('0'), 'Invalid input')
        self.assertEqual(print_singleteam_result(' '), 'Invalid input')
        self.assertEqual(print_singleteam_result('aaa'), 'Invalid input')
    
    def test_singleteam_input_valid(self):
        self.assertEqual(print_singleteam_result('min'), 'Available team name')
        self.assertEqual(print_singleteam_result('BKN'), 'Available team name')
        
    def test_multi_input_invalid(self):
        self.assertEqual(print_multi_result('A'), 'Invalid input')
        self.assertEqual(print_multi_result('$'), 'Invalid input')
        self.assertEqual(print_multi_result('0'), 'Invalid input')
        self.assertEqual(print_multi_result(' '), 'Invalid input')
        self.assertEqual(print_multi_result('Pt'), 'Invalid input')
        self.assertEqual(print_multi_result('fansal'), 'Invalid input')
    
    def test_multi_input_valid(self):
        self.assertEqual(print_multi_result('pt'), 'Available input variable')
        self.assertEqual(print_multi_result('FanSal'), 'Available input variable')
  
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()