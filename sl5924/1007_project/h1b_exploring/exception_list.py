'''
Created on Dec 4, 2016

User Self-defined Exception

@author: yuweitu
'''


# Exception when inputing wrong option
class wrong_option_exception(NameError):
    pass

# Exception when inputing wrong state abbreviation
class invalid_state_name(Exception):
    pass

# Exception when inputing unlisted company
class invalid_company_name(Exception):
    pass

# Exception when inputing unlisted industry
class invalid_industry_name(Exception):
    pass

#Exception when entering a wrong integer
class wrong_int_exception(Exception):
    pass


class wrong_dataset_exception(Exception):
    pass