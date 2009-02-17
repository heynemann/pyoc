import unittest
import sys
import os
root_path = os.path.abspath(__file__ + "/../../")
sys.path.insert(0, root_path)
from pyoc.ioc import *

class BaseTest(unittest.TestCase):
    def setUp(self):
        IoC.reset()
