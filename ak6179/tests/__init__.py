"""
Unit Tests for mapping-yelp module. For running the unit tests use the command 'python -m unittest discover'.
The command needs to be run from just outside the tests folder
(i.e. just inside the outtermost directory of mapping-yelp).
The command will automatically discover unit tests and will run them.
'main' function is not provided for running the tests because of problem with relative imports.
Eg: The statement from ..yelp_data import * would be invalid. There is a workaround to this
problem as indicated by this answer: http://stackoverflow.com/questions/16981921/relative-imports-in-python-3 .
I went through a number of online resources and unit tests implementation in python (eg: sklearn) and
the standard way to run tests is using the command 'python -m unittest discover'.
"""