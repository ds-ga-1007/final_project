"""
    Date: 12/10/2016
    
    Author: Lingzhi Meng(lm3226)
    Yifu Sun(ys1700)
    Yanan Shi(ys2506)
    
    Description: This file provides unittest for user_interaction.py.
    """

import unittest
from user_interaction import validType, InvalidInputException
#Unit tests are provided with the solution code
#The unit tests pass correctly
class Test(unittest.TestCase):
    
    #test function validType
    def test_validType(self):
        self.assertEqual(validType('Language'), 'language')
        self.assertEqual(validType('language'), 'language')
        self.assertEqual(validType('A'),'language')
        self.assertEqual(validType('B'),'country')
        self.assertEqual(validType('C'),'city')
        self.assertEqual(validType('D'),'hashtag')
        self.assertEqual(validType('city'),'city')
        self.assertEqual(validType('City'),'city')
        self.assertEqual(validType('country'),'country')
        self.assertEqual(validType('hashtag'),'hashtag')
        
        with self.assertRaises(InvalidInputException):
            validType('AB')
                validType('E')
                    validType('Aity')
                        validType('$s')
                            validType('1')
                                validType('A ')



if __name__ == "__main__":
    unittest.main()