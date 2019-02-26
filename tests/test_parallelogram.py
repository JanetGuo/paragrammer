import os, sys
from unittest import TestCase, TestLoader, TextTestRunner, mock

# imports to test
from src.parallelogram import *

# Test Classes------------------------------------
class TestParallelogram(TestCase):
    def test_init(self):
        x_test = 3
        y_test = 14
        pt = Point(x_test, y_test)
        self.assertEquals(pt.x, x_test)
        self.assertEquals(pt.y, y_test)

# Run Tests--------------------------------------------------
TextTestRunner(verbosity=2).run(TestLoader().loadTestsFromTestCase(TestParallelogram))