# The final project of DS-GA 1007
# NYU Center for Data Science
# Authors: Jiaming Dong (jd3405@nyu.edu)
#          Daniel Amaranto (da1933@nyu.edu)
#          Julie Cachia (jyc436@nyu.edu)
#
# The error file


class AttributeNotFoundException(Exception):
    def __str__(self):
        """return the string"""
        return "attribute not found"

class TokenNumberInvalidException(Exception):
    def __str__(self):
        """return the string"""
        return "token number is invalid"
