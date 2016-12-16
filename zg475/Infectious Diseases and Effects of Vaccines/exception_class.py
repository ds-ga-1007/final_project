'''
This module contains user defined errors for handling exceptions.
    DigitError
    InvalidDisease
    colorrangeException
    colortypeException
    yeartypeException
    yearrangeException
    diseaseExceptioin
    plottypeException
Created on Nov 21, 2016
'''

class DigitError(Exception):
    '''
    Handling meaningless digit Input
    '''
    def __str__(self):
        return 'Only string disease name are valid for Heatmap!'


class InvalidDisease(Exception):
    '''
    Handling invalid input for Heatmap plot
    '''
    def __str__(self):
        return 'This is not a valid disease for heatmap plot!' 


class colorrangeException(Exception):
    '''
    Handling undefined color HSV
    '''
    def __str__(self):
        return 'The color range is out of bound'

class colortypeException(Exception):
    '''
    Handling undefined color type, only float number should be read from user
    '''
    def __str__(self):
        return 'The color you input is not int'
    
class yeartypeException(Exception):
    '''
    Handling unsupported year type, the year should be an int input
    '''
    def __str__(self):
        return 'The year you input is not int'
    
class yearrangeException(Exception):
    '''
    Handling error for year input which beyond year's range for dataset
    '''
    def __str__(self):
        return 'The year you input is not valid for this disease'
    
class diseaseExceptioin(Exception):
    '''
    Handling error for disease input which is not in the dataset
    '''
    def __str__(self):
        return 'The disease is not valid, please enter another name'
    
class plottypeException(Exception):
    '''
    Handling error for plot-type which is not valid in our program
    '''
    def __str__(self):
        return 'This plot type is not offered'     