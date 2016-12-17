'''
Created on Dec 16, 2016

@author: muriel820
'''

class InputNotString(Exception):
    '''This exception handles the situation when input expects a string, but didn't get a string'''
    def __str__(self):
        return 'Please input a string'

class InputNotInt(Exception):
    '''This exception handles the situation when input expects an integer, but didn't get a string'''
    def __init__(self):
        return 0
