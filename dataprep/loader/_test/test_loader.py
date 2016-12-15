
from unittest import TestCase
from dataprep.loader import *


class TestLoader(TestCase):
    def test_constructor(self):
        with self.assertRaises(TypeError):
            CSVLoader(target=2.2)
        with self.assertRaises(TypeError):
            CSVLoader(target=['a', 1])
