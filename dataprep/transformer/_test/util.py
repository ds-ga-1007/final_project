
import numpy as NP
from collections import Iterable
from numbers import Number

def iterable_not_str(a):
    return isinstance(a, Iterable) and not isinstance(a, str)

def generic_array_equal(a, b):
    '''
    Compare the array element-wise, taking NaNs into consideration,
    recursing into sub-arrays.
    '''
    try:
        for _a, _b in zip(a, b):
            if iterable_not_str(_a) and iterable_not_str(_b):
                if not generic_array_equal(_a, _b):
                    return False
                else:
                    continue
            elif (_a is None) and (_b is None):
                continue
            elif _a == _b:
                continue
            elif NP.isnan(_a) and NP.isnan(_b):
                continue
            elif (isinstance(_a, Number) and isinstance(_b, Number) and
                  NP.isclose(_a, _b)):
                continue
            return False
        return True
    except:
        return False
