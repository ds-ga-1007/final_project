'''
This module defines errors
@author: ShashaLin
'''
class Errors(Exception):
    pass

class InputError(Errors):
    def __init__(self, message1):
        self.message = message1
    

class FileError(Errors):
    def __init__(self, message1):
        self.message = message1

